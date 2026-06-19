import streamlit as st
import requests
import pandas as pd

st.title("⛳ Debug Golf App")

@st.cache_data(ttl=60)
def get_data():
    url = "https://site.api.espn.com/apis/site/v2/sports/golf/leaderboard"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    # Let's inspect the data structure
    events = data.get('events', [])
    if not events:
        return "No events found"
    
    competitors = events[0].get('competitions', [{}])[0].get('competitors', [])
    return f"Successfully retrieved {len(competitors)} players."

try:
    message = get_data()
    st.write(message)
except Exception as e:
    st.error(f"Critical Error: {e}")
