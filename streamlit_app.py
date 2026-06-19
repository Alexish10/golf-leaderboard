import streamlit as st
import requests
import pandas as pd

# This decorator forces a refresh every 60 seconds
@st.cache_data(ttl=60)
def get_data():
    url = "https://site.api.espn.com/apis/site/v2/sports/golf/leaderboard"
    # The 'params' argument helps prevent the server from sending cached responses
    response = requests.get(url, params={"timestamp": pd.Timestamp.now().timestamp()}).json()
    entries = response['events'][0]['competitions'][0]['competitors']
    
    live_map = {}
    for c in entries:
        name = c['athlete']['displayName']
        stats = c.get('statistics', [])
        score_val, display = None, "NS"
        for s in stats:
            if s.get('name') == 'scoreToPar':
                val_str = s.get('displayValue')
                if val_str in ['E', 'EVEN']: score_val, display = 0, 'E'
                elif val_str and val_str not in ['-', '--']:
                    score_val = int(val_str.replace('+', ''))
                    display = val_str
                break
        thru = c.get('status', {}).get('displayValue', '')
        live_map[name] = {"val": score_val, "disp": display, "thru": thru}
    return live_map
