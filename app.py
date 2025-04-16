import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

# Define constants
EMOJI_TO_WORDS = {
    "😊": "Happy",
    "😕": "Confused",
    "😠": "Angry",
    "🎉": "Celebratory"
}
APP_TITLE = "Mood of the Queue"
SHEET_ID = '1c0xNjBGPyUMv9rJ1SecPDLQ13L_OrrNxREMw-SZ-O9A'
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configure page and set up title
st.set_page_config(page_title=APP_TITLE, page_icon="🧪")
st.title(APP_TITLE)

# Connect to google sheet
@st.cache_resource
def connect_to_gsheet():
    """Connect to google sheet with st.secrets.
    """
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    # NOTE: make sure to set up service account and save the credential information to streamlit (cloud) or /streamlit/secrets.toml
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], 
        scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    
    return sheet

sheet = connect_to_gsheet()
_ = sheet.get_all_values() # Test to get data
st.success("Connected to Google Sheet!")

# Section 1: Log Mood
st.header("Log a new mood", divider="gray")

selected_mood = st.selectbox(
    "Select the current queue mood:",
    options=list(EMOJI_TO_WORDS.keys()), # Remember keys of EMOJI_TO_WORDS are the emojis
    format_func=lambda x: f"{x} - {EMOJI_TO_WORDS[x]}"
)
note = st.text_area("Add a short note (optional, no more than 200 char):", max_chars=200)

## Submit button
if st.button("Submit Mood"):
    if not selected_mood:
        st.warning("Please select a mood before submitting")
    timestamp = datetime.now().strftime(DATETIME_FORMAT)
    sheet.append_row([timestamp, selected_mood, note])
    st.success("Mood logged successfully!")
    # Real time update
    st.rerun()

# Section 2: Visualize the mood for today
st.header("Today's Queue Mood", divider="gray")

## Add refresh button to manually refresh the data
if st.button("🔄 Refresh Data Manually"):
    st.rerun()

# Get data
data = sheet.get_all_records()  # Automatically uses first row as headers
df = pd.DataFrame(data)

if not df.empty:
    # Convert timestamp string to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format=DATETIME_FORMAT)
    # Filter for today's data
    today = datetime.now().date()
    today_str = today.strftime("%Y-%m-%d")
    today_df = df[df['Timestamp'].dt.date == today]
    
    if not today_df.empty:
        # Count moods
        mood_counts = today_df['Mood'].value_counts()
        # Avoid using emoji as bar label
        mood_counts_readable = pd.Series(
            index=[EMOJI_TO_WORDS.get(emoji) for emoji in mood_counts.index],
            data=mood_counts.values
        )
        # Plot bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        mood_counts_readable.plot(kind='bar', ax=ax)
        plt.title(f"Queue Mood for: {today_str}")
        plt.xlabel("Mood")
        plt.ylabel("Count")
        plt.xticks(rotation=0)
        # Display chart
        st.pyplot(fig)
        
        # Display raw data for reference
        st.subheader("Raw Data")
        st.dataframe(today_df)
    else: # empty today_df
        st.info("No moods logged today yet.")
else: # empty df
    st.info("No data in the Google Sheet yet.")