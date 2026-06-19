import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Major Pool Leaderboard", page_icon="⛳️")
st.title("⛳ Live Major Pool Leaderboard")

@st.cache_data(ttl=60)
def get_data():
    url = "https://site.api.espn.com/apis/site/v2/sports/golf/leaderboard"
    response = requests.get(url, timeout=10)
    data = response.json()
    entries = data['events'][0]['competitions'][0]['competitors']
    
    live_map = {}
    for c in entries:
        name = c['athlete']['displayName']
        # Safely get stats
        stats = c.get('statistics', [])
        score_val, display = None, "NS"
        for s in stats:
            if s.get('name') == 'scoreToPar':
                val_str = s.get('displayValue')
                if val_str in ['E', 'EVEN']: score_val, display = 0, 'E'
                elif val_str and val_str not in ['-', '--']:
                    try:
                        score_val = int(val_str.replace('+', ''))
                        display = val_str
                    except: pass
                break
        thru = c.get('status', {}).get('displayValue', '')
        live_map[name] = {"val": score_val, "disp": display, "thru": thru}
    return live_map

# Load Data
try:
    live_map = get_data()
    rosters = {
        "Ray": ["Ludvig Åberg", "Rory McIlroy", "Brooks Koepka", "Collin Morikawa", "Patrick Cantlay"],
        "Dean": ["Sam Burns", "Scottie Scheffler", "Wyndham Clark", "Akshay Bhatia", "Jacob Bridgeman"],
        "Chris": ["Chris Gotterup", "Tommy Fleetwood", "Adam Scott", "Si Woo Kim", "Xander Schauffele"],
        "Alexis": ["Tyrrell Hatton", "Shane Lowry", "Matt Fitzpatrick", "Hideki Matsuyama", "Jon Rahm"],
        "Jenna": ["Cameron Young", "J.J. Spaun", "Justin Rose", "Bryson DeChambeau", "Russell Henley"]
    }

    results = []
    for mgr, roster in rosters.items():
        scores = []
        player_display = []
        for player in roster:
            match = next((name for name in live_map if player.lower() in name.lower()), None)
            if match and live_map[match]['val'] is not None:
                data = live_map[match]
                player_display.append(f"{match.split()[-1]} ({data['disp']} {data['thru']})")
                scores.append(data['val'])
            else:
                player_display.append(f"{player.split()[-1]} (-)")
        
        scores.sort()
        total = sum(scores[:3]) if len(scores) >= 3 else 999
        display = f"{total:+}" if total != 0 and total < 999 else ("E" if total == 0 else "Pending")
        results.append({"Manager": mgr, "Total": display, "Roster": " | ".join(player_display), "_val": total})

    df = pd.DataFrame(results).sort_values("_val")

    # Display Table and Expanders
    st.table(df[["Manager", "Total"]])
    for _, row in df.iterrows():
        with st.expander(f"{row['Manager']} - Score: {row['Total']}"):
            st.write(row['Roster'])

    if st.button("Refresh Data"):
        st.rerun()

except Exception as e:
    st.error(f"Data processing error: {e}")
