import streamlit as st
import pandas as pd

# Mock data based on your screenshot
data = {
    "Manager": ["Alexis", "Dean", "Ray", "Jenna", "Chris"],
    "Total": [-3, -1, 0, 2, 5],
    "Roster": [
        ["Hatton (+4 F)", "Lowry (+4 Thru 13)", "Fitzpatrick (-3 Thru 14)", "Matsuyama (+2 Thru 14)", "Rahm (-2 Thru 12)"],
        ["Burns (+1 F)", "Scheffler (+2 F)", "Clark (-4 Thru 13)", "Bhatia (+2 Thru 13)", "Bridgeman (+3 F)"],
        ["Åberg (-1 F)", "McIlroy (-1 F)", "Koepka (+3 F)", "Morikawa (+2 Thru 14)", "Cantlay (+4 Thru 12)"],
        ["Young (+2 F)", "Spaun (+7 F)", "Rose (+3 Thru 12)", "DeChambeau (-2 Thru 14)", "Henley (+2 Thru 13)"],
        ["Gotterup (+5 F)", "Fleetwood (E F)", "Scott (+3 F)", "Kim (+7 F)", "Schauffele (+2 Thru 14)"],
    ],
}

df = pd.DataFrame(data)

st.title("⛳ Live Major Pool Leaderboard")

if st.button("Refresh Data"):
    st.rerun()

# Display main leaderboard table
st.subheader("Current Standings")
# We only show Manager and Total in the main, clean table
st.table(df[["Manager", "Total"]].sort_values("Total"))

# Use an expander for each manager to view their roster cleanly
st.subheader("Roster Details")
for index, row in df.iterrows():
    with st.expander(f"{row['Manager']} (Score: {row['Total']})"):
        # Display roster as a nice bulleted list
        for player in row['Roster']:
            st.write(f"- {player}")