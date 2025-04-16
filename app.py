import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

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

# configure page
st.set_page_config(page_title=APP_TITLE, page_icon="🧪")
st.title(APP_TITLE)

# Define functions
@st.cache_resource
def connect_to_gsheet():
    """Connect to google sheet
    """
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    # NOTE: make sure to set up service account and download the credentials to the same directory
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    
    return sheet

# Connect to google sheet
sheet = connect_to_gsheet()
_ = sheet.get_all_values() # Test to get data
st.success("Connected to Google Sheet!")

# The site has two tabs.
## Tab 1 for logging the mod
## Tab 2 for visualize the mood for today
tab1, tab2 = st.tabs(["Log Mood", "View Moods"])

# Log Mood tab
with tab1:
    st.header("Log a new mood")
    
    # NOTE: Keys of EMOJI_TO_WORDS are the emojis
    selected_mood = st.selectbox(
        "Select the current queue mood:",
        options=list(EMOJI_TO_WORDS.keys()),
        format_func=lambda x: f"{x} - {EMOJI_TO_WORDS[x]}"
    )
    
    # Optional note
    note = st.text_area("Add a short note (optional, no more than 200 char):", max_chars=200)
    
    # Submit button
    if st.button("Submit Mood"):
        if not selected_mood:
            st.warning("Please select a mood before submitting")
        # Get current timestamp
        timestamp = datetime.now().strftime(DATETIME_FORMAT)
        
        # Append to Google Sheet
        sheet.append_row([timestamp, selected_mood, note])
        
        st.success("Mood logged successfully!")
        st.rerun()

with tab2:
    st.header("Today's Queue Mood")
    
    # Add refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    # Get data from Google Sheet with headers
    data = sheet.get_all_records()  # Automatically uses first row as headers
    df = pd.DataFrame(data)
    
    if not df.empty:
        # Convert timestamp string to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format=DATETIME_FORMAT)
        
        # Filter for today's data
        today = datetime.now().date()
        today_df = df[df['Timestamp'].dt.date == today]
        
        if not today_df.empty:
            # Count moods
            mood_counts = today_df['Mood'].value_counts()
            
            # Avoid using emoji as headers
            mood_counts_readable = pd.Series(
                index=[EMOJI_TO_WORDS.get(emoji) for emoji in mood_counts.index],
                data=mood_counts.values
            )
            
            # Create bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            mood_counts_readable.plot(kind='bar', ax=ax)
            plt.title("Today's Queue Mood")
            plt.xlabel("Mood")
            plt.ylabel("Count")
            plt.xticks(rotation=0)
            
            # Display chart
            st.pyplot(fig)
            
            # Display raw data
            st.subheader("Raw Data")
            st.dataframe(today_df)
        else:
            st.info("No moods logged today yet.")
    else:
        st.info("No data in the Google Sheet yet.")