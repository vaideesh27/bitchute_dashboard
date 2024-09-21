import streamlit as st
import sqlite3
import pandas as pd
import json
import datetime

def fetch_video_data(video_url):
    """
    Fetches video trend data from the SQLite database for the specified video URL.

    Parameters:
        video_url (str): The URL of the video.

    Returns:
        dict: A dictionary containing the video trend data or None if not found.
    """
    conn = sqlite3.connect('bitchute.db')  # Connect to your SQLite database
    cursor = conn.cursor()
    
    query = """
    SELECT video_comments_trend, 
           video_views_trend, 
           video_likes_trend, 
           video_dislikes_trend
    FROM videos
    WHERE video_url = ?;
    """
    
    cursor.execute(query, (video_url,))
    row = cursor.fetchone()
    
    if row:
        columns = [desc[0] for desc in cursor.description]
        record_dict = dict(zip(columns, row))
    else:
        record_dict = None
    
    conn.close()
    return record_dict

def video_trend(trend_string, start_date, end_date, label):
    """
    Visualizes the trend data as a scatter chart.

    Parameters:
        trend_string (str): JSON string containing trend data.
        start_date (datetime.date): The start date for filtering data.
        end_date (datetime.date): The end date for filtering data.
        label (str): The label for the y-axis.
    """
    trend = json.loads(trend_string)
    df = pd.DataFrame(trend)
    df['t'] = pd.to_datetime(df['t'])
    df = df.drop_duplicates(subset='t', keep='last')
    filtered_df = df[(df['t'].dt.date >= start_date) & (df['t'].dt.date <= end_date)]
    st.scatter_chart(filtered_df, x = "t", y = "c", x_label = "Time", y_label = label)

def page_layout():
    """
    Sets up the layout for the Streamlit application, including sidebar navigation and main content.
    """
    st.set_page_config(page_title="Video Analytics Dashboard", layout="wide")
    
    st.sidebar.write("Home")
    st.sidebar.page_link("app.py", label="Home", icon=":material/home:", use_container_width=True)
    st.sidebar.write("Dashboard")
    st.sidebar.page_link("pages/dashboard.py", label="Dashboard", icon=":material/dashboard:", use_container_width=True)
    
    st.title("Video Analytics Dashboard")
    st.header("Video Display")
    video_url = st.session_state['video_data']['Url']
    st.components.v1.iframe(video_url.replace("video", "embed"), height = 360)

    st.subheader("Video Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Title:", st.session_state['video_data']['Title'])

    with col2:
        st.markdown(f"Channel: [ {st.session_state['video_data']['Channel']} ]({st.session_state['video_data']['Channel_Url']})", unsafe_allow_html=True)

    with col3:
        st.write("Upload Date:", st.session_state['video_data']['Upload_Date'])
    
    st.write("Hashtags:", st.session_state['video_data']['Hashtags'])
    st.write("Integrity Score:", f"{st.session_state['video_data']['Integrity_Score']}/100")

    st.header("Analytics Overview")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Total Views", st.session_state['video_data']['Views'])
    metric_col2.metric("Total Likes", st.session_state['video_data']['Likes'])
    metric_col3.metric("Total Dislikes", st.session_state['video_data']['Dislikes'])
    metric_col4.metric("Total Comments", st.session_state['video_data']['Comments'])

    st.header("Visualization")
    try:
        video_data = fetch_video_data(st.session_state['video_data']['Url'])
        start_date, end_date = st.date_input('Select Date Range', value=(datetime.date.today() - datetime.timedelta(days=1) , datetime.date.today()))
        st.subheader("Views Over Time")
        video_trend(video_data['video_views_trend'], start_date, end_date, "Views")
        st.subheader("Likes Over Time")
        video_trend(video_data['video_likes_trend'], start_date, end_date, "Likes")
        st.subheader("Dislikes Over Time")
        video_trend(video_data['video_dislikes_trend'], start_date, end_date, "Dislikes")
        st.subheader("Comments Over Time")
        video_trend(video_data['video_comments_trend'], start_date, end_date, "Comments")
    except:
        st.write("Select a Date Range")

page_layout()