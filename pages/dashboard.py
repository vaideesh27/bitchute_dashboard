import streamlit as st

def video_table(query=""):
    """
    Displays a summary table of videos filtered by the search query.

    Parameters:
        query (str): A string to filter video titles.
    """
    conn = st.connection('bitchute_db', type='sql')
    videos = conn.query(f'SELECT video_title AS Title, video_upload_date AS Upload_Date, video_info_integrity_score AS Integrity_Score, video_url AS Url, video_channel_url AS Channel_Url, video_views AS Views, video_likes AS Likes, video_dislikes AS Dislikes, video_comments_count AS Comments, video_channel_name AS Channel, CASE WHEN video_hashtags = "[]" THEN "None" ELSE video_hashtags END AS Hashtags FROM videos WHERE video_title LIKE "%{query}%"')
    event = st.dataframe(videos, on_select='rerun',selection_mode='single-row', column_config = {'Url': None, 'Channel_Url': None, 'Upload_Date': None})

    if len(event.selection['rows']):
        selected_row = event.selection['rows'][0]
        video_data = videos.iloc[selected_row].to_dict()
        st.session_state['video_data'] = video_data
        st.page_link('pages/video.py', label = 'More Details')

def channel_table(query=""):
    """
    Displays a summary table of channels associated with the videos filtered by the search query.

    Parameters:
        query (str): A string to filter video titles.
    """
    conn = st.connection('bitchute_db', type='sql')
    channels = conn.query(f'SELECT video_channel_name AS Channel, AVG(video_info_integrity_score) AS Integrity_Score, SUM(video_views) AS Views, SUM(video_likes) AS Likes, SUM(video_dislikes) AS Dislikes, SUM(video_comments_count) AS Comments, video_channel_url AS Url FROM videos WHERE video_title LIKE "%{query}%" GROUP BY video_channel_name, video_channel_url')
    event = st.dataframe(channels, on_select='rerun',selection_mode='single-row',column_config = {'Url': st.column_config.LinkColumn(display_text="Open Channel Url")})
    
    if len(event.selection['rows']):
        selected_row = event.selection['rows'][0]
        channel_data = channels.iloc[selected_row].to_dict()
        st.session_state['channel_data'] = channel_data
        st.page_link('pages/channel.py', label = 'More Details')

def video_data_vs_score(label, query=""):
    """
    Generates a scatter chart comparing video metrics against the integrity score.

    Parameters:
        label (str): The metric to plot on the x-axis (e.g., "Views", "Likes").
        query (str): A string to filter video titles.
    """
    conn = st.connection('bitchute_db', type='sql')
    data = conn.query(f'SELECT video_views AS Views, video_likes AS Likes, video_dislikes AS Dislikes, video_comments_count AS Comments, video_info_integrity_score AS Integrity_Score FROM videos WHERE video_title LIKE "%{query}%"')
    st.scatter_chart(data, x=label, y="Integrity_Score")

def videos_vs_integrity(query=""):
    """
    Displays a bar chart showing the count of videos in different integrity score ranges.

    Parameters:
        query (str): A string to filter video titles.
    """
    conn = st.connection('bitchute_db', type='sql')
    data = conn.query(f'SELECT CASE WHEN video_info_integrity_score BETWEEN 1 AND 25 THEN "1-25" WHEN video_info_integrity_score BETWEEN 26 AND 50 THEN "26-50" WHEN video_info_integrity_score BETWEEN 51 AND 75 THEN "51-75" WHEN video_info_integrity_score BETWEEN 76 AND 100 THEN "76-100" END AS Integrity_Score, COUNT(*) AS Videos_Count FROM videos WHERE video_title LIKE "%{query}%" GROUP BY Integrity_Score ORDER BY Integrity_Score;')
    st.bar_chart(data, x = "Integrity_Score", y="Videos_Count")

def channels_vs_integrity(query=""):
    """
    Displays a bar chart showing the count of channels in different integrity score ranges.

    Parameters:
        query (str): A string to filter video titles.
    """
    conn = st.connection('bitchute_db', type='sql')
    data = conn.query(f'SELECT Integrity_Score, COUNT(*) AS Channels_Count FROM (SELECT CASE WHEN Integrity_Score BETWEEN 1 AND 25 THEN "1-25" WHEN Integrity_Score BETWEEN 26 AND 50 THEN "26-50" WHEN Integrity_Score BETWEEN 51 AND 75 THEN "51-75" WHEN Integrity_Score BETWEEN 76 AND 100 THEN "76-100" END AS Integrity_Score, COUNT(*) AS Channels_Count FROM (SELECT video_channel_name AS Channel, AVG(video_info_integrity_score) AS Integrity_Score, SUM(video_views) AS Views, SUM(video_likes) AS Likes, SUM(video_dislikes) AS Dislikes, SUM(video_comments_count) AS Comments, video_channel_url AS Url FROM videos WHERE video_title LIKE "%{query}%" GROUP BY video_channel_name, video_channel_url) GROUP BY Integrity_Score ORDER BY Integrity_Score) GROUP BY Integrity_Score;')
    st.bar_chart(data, x = "Integrity_Score", y="Channels_Count")

def views_vs_likes_vs_integrity(query=""):
    """
    Generates a scatter chart comparing total views against total likes, colored by integrity score.

    Parameters:
        query (str): A string to filter video titles.
    """
    conn = st.connection('bitchute_db', type='sql')
    data = conn.query(f'SELECT CASE WHEN video_info_integrity_score BETWEEN 1 AND 25 THEN "1-25" WHEN video_info_integrity_score BETWEEN 26 AND 50 THEN "26-50" WHEN video_info_integrity_score BETWEEN 51 AND 75 THEN "51-75" WHEN video_info_integrity_score BETWEEN 76 AND 100 THEN "76-100" END AS Integrity_Score, SUM(video_views) AS Total_Views, SUM(video_likes) AS Total_Likes FROM videos WHERE video_title LIKE "%{query}%" GROUP BY Integrity_Score ORDER BY Integrity_Score;')
    st.scatter_chart(data, x = "Total_Likes", y="Total_Views", color = "Integrity_Score")

def render_search(query=""):
    """
    Renders the main search interface, including video and channel summary tables and various visualizations.

    Parameters:
        query (str): A string to filter video titles.
    """
    st.subheader("Video Data Summary Table")
    video_table(query)
    st.subheader("Channel Data Summary Table")
    channel_table(query)
    st.header("Data Visualizations")
    tab1, tab2, tab3, tab4 = st.tabs(["Views", "Likes", "Dislikes", "Comments"])
    with tab1:
        st.subheader("Views Over Integrity Score")
        video_data_vs_score("Views", query)
    with tab2:
        st.subheader("Likes Over Integrity Score")
        video_data_vs_score("Likes", query)
    with tab3:
        st.subheader("Dislikes Over Integrity Score")
        video_data_vs_score("Dislikes", query)
    with tab4:
        st.subheader("Comments Over Integrity Score")
        video_data_vs_score("Comments", query)
    st.header("Additional Insights")
    st.subheader("Video Count - Integrity Score Histogram")
    videos_vs_integrity(query)
    st.subheader("Channel Count - Integrity Score Histogram")
    channels_vs_integrity(query)
    st.subheader("Views Over Likes Over Integrity Score")
    views_vs_likes_vs_integrity(query)

def page_layout():
    """
    Sets up the overall layout of the Streamlit application.
    """
    st.set_page_config(page_title="Bitchute Analytics Dashboard", layout="wide")
    st.sidebar.write("Home")
    st.sidebar.page_link("app.py", label="Home", icon=":material/home:", use_container_width=True)
    st.sidebar.write("Dashboard")
    st.sidebar.page_link("pages/dashboard.py", label="Dashboard", icon=":material/dashboard:", use_container_width=True)
    st.title("Bitchute Analytics Dashboard")
    st.subheader("Filter Videos")
    query = st.text_input("Search by Video Title:")
    render_search(query)

page_layout()