import streamlit as st
import sqlite3
import json
import pandas as pd
from collections import defaultdict
import datetime

def fetch_channel_data(video_channel_url):
    """
    Fetches channel data from the SQLite database for the specified channel URL.

    Parameters:
        video_channel_url (str): The URL of the video channel.

    Returns:
        list: A list of dictionaries containing channel trend data.
    """
    conn = sqlite3.connect('bitchute.db')
    cursor = conn.cursor()
    
    query = """
    SELECT video_comments_trend, 
           video_views_trend, 
           video_likes_trend, 
           video_dislikes_trend
    FROM videos
    WHERE video_channel_url = ?;
    """
    
    cursor.execute(query, (video_channel_url,))
    rows = cursor.fetchall()
    channel_data = []
    for row in rows:
        columns = [desc[0] for desc in cursor.description]
        record_dict = dict(zip(columns, row))
        channel_data.append(record_dict)
    
    conn.close()
    return channel_data

def clear_duplicates(item):
    """
    Cleans duplicate entries from the trend data.

    Parameters:
        item (dict): A dictionary containing trend data.

    Returns:
        dict: A dictionary with cleaned trend data.
    """
    keys = ['video_comments_trend', 'video_views_trend', 'video_likes_trend', 'video_dislikes_trend']
    cleaned_data = {}
    for key in keys:
        df = pd.DataFrame(json.loads(item[key]))
        df = df.drop_duplicates(subset='t', keep='last')
        cleaned_data[key] = df.to_dict(orient='records')
    return cleaned_data

def process_channel_data(channel_data):
    """
    Processes the raw channel data to aggregate trends.

    Parameters:
        channel_data (list): A list of dictionaries containing channel trend data.

    Returns:
        dict: A dictionary with aggregated trend data for each metric.
    """
    temp = {}
    temp['video_comments_trend'] = []
    temp['video_views_trend'] = []
    temp['video_dislikes_trend'] = []
    temp['video_likes_trend'] = []

    for item in channel_data:
        cleaned_data = clear_duplicates(item)
        temp['video_comments_trend'].append(cleaned_data['video_comments_trend'])
        temp['video_views_trend'].append(cleaned_data['video_views_trend'])
        temp['video_dislikes_trend'].append(cleaned_data['video_dislikes_trend'])
        temp['video_likes_trend'].append(cleaned_data['video_likes_trend'])
    
    flattened_data ={}
    result = {}
    keys = ['video_comments_trend', 'video_views_trend', 'video_likes_trend', 'video_dislikes_trend']
    for key in keys:
        flattened_data[key] = [item for sublist in temp[key] for item in sublist]

    for key in keys:
        aggregated_data = defaultdict(int)
        for entry in flattened_data[key]:
            aggregated_data[entry['t']] += entry['c']
        result[key] = [{'t': timestamp, 'c': value} for timestamp, value in aggregated_data.items()]

    return result

def channel_trend(trend, start_date, end_date, label):
    """
    Visualizes the trend data as a scatter chart.

    Parameters:
        trend (list): A list of dictionaries containing trend data.
        start_date (datetime.date): The start date for filtering data.
        end_date (datetime.date): The end date for filtering data.
        label (str): The label for the y-axis.
    """
    df = pd.DataFrame(trend)
    df['t'] = pd.to_datetime(df['t'])
    filtered_df = df[(df['t'].dt.date >= start_date) & (df['t'].dt.date <= end_date)]
    st.scatter_chart(filtered_df, x = "t", y = "c", x_label = "Time", y_label = label)

def page_layout():
    """
    Sets up the layout for the Streamlit application, including sidebar navigation and main content.
    """
    st.set_page_config(page_title="Channel Analytics Dashboard", layout="wide")

    st.sidebar.write("Home")
    st.sidebar.page_link("app.py", label="Home", icon=":material/home:", use_container_width=True)
    st.sidebar.write("Dashboard")
    st.sidebar.page_link("pages/dashboard.py", label="Dashboard", icon=":material/dashboard:", use_container_width=True)

    st.title("Channel Analytics Dashboard")
    st.subheader("Channel Details")
    st.markdown(f"Channel: [ {st.session_state['channel_data']['Channel']} ]({st.session_state['channel_data']['Url']})", unsafe_allow_html=True)
    st.write("Integrity Score:", f"{st.session_state['channel_data']['Integrity_Score']}/100")

    st.header("Analytics Overview")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Total Views", st.session_state['channel_data']['Views'])
    metric_col2.metric("Total Likes", st.session_state['channel_data']['Likes'])
    metric_col3.metric("Total Dislikes", st.session_state['channel_data']['Dislikes'])
    metric_col4.metric("Total Comments", st.session_state['channel_data']['Comments'])

    st.header("Visualization")
    try:
        channel_data = fetch_channel_data(st.session_state['channel_data']['Url'])
        data = process_channel_data(channel_data)
        start_date, end_date = st.date_input('Select Date Range', value=(datetime.date.today() - datetime.timedelta(days=1) , datetime.date.today()))
        st.subheader("Views Over Time")
        channel_trend(data["video_views_trend"], start_date, end_date, "Views")
        st.subheader("Likes Over Time")
        channel_trend(data["video_likes_trend"], start_date, end_date, "Likes")
        st.subheader("Dislikes Over Time")
        channel_trend(data["video_dislikes_trend"], start_date, end_date, "Dislikes")
        st.subheader("Comments Over Time")
        channel_trend(data["video_comments_trend"], start_date, end_date, "Comments")
    except:
        st.write("Select a Date Range")

page_layout()