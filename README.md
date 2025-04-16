# Mood of the Queue

A simple Streamlit app that allows support agents to track the mood of the support ticket queue throughout the day.

Click here to try the app: https://moodtracker-ccgvu4ewagff3m33bynsuk.streamlit.app/

# For Users: How to use the app

## Features

This app lets you:
- **Log a mood**: Select a mood that reflects the current vibe of the support queue and (optionally) add a note.
- **Visualize mood trends**: Instantly see a bar chart showing how moods have trended today.

How to use it:
1. Go to the "Log a new mood" section.
2. Choose one of the mood emojis:
3. (Optional) Write a short note. Don't exceed 200 chars
4. Click Submit Mood to save it
5. Scroll down to see today’s mood trends. Click "Refresh Data Manually" if others have logged new moods

# For Developers: How is this app built and how to play with it

High level ideas:
- Minimal UI friction: Just a dropdown and a note field to log the mood
- Lightweight backend: Google Sheets avoids spinning up a full database. Also connection is cached so that if the tab reopens, it doesn't require another connection 
- Fast feedback loop: Visuals update instantly (plus button to refresh manually) to give a sense of progress
- Separation of concerns: one section for input, one for visualization.

UX Touches:
- Success/warning messages
- Manual refresh button
- Emoji + label formatting for clarity
- Raw data view for transparency

## Tech stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Storage**: Google Sheets
- **Visualization**: Matplotlib

See requirements.txt for list of pip-installable packages needed

## Setup Instructions

- Set up st.secrets with the service account credentials under `/streamlit/secrets.toml`, in this format

```
[gcp_service_account]
type = "just an example"
project_id = "just am exmaple"
# list goes on
```
- Google Sheet is identified using SHEET_ID.