import sqlite3
import json

def create_db():
    """
    Creates the SQLite database and the 'videos' table if it doesn't exist.
    """
    conn = sqlite3.connect('bitchute.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS videos (
                        video_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        video_title TEXT,
                        video_url TEXT UNIQUE,
                        video_views INTEGER,
                        video_likes INTEGER,
                        video_dislikes INTEGER,
                        video_channel_url TEXT,
                        video_channel_name TEXT,
                        video_comments_count INTEGER,
                        video_upload_date TEXT,
                        video_hashtags TEXT,
                        video_info_integrity_score INTEGER,
                        video_comments_trend TEXT,
                        video_views_trend TEXT,
                        video_likes_trend TEXT,
                        video_dislikes_trend TEXT)''')

    conn.commit()
    conn.close()

def insert_video_data(video_data):
    """
    Inserts new video data into the database.

    Parameters:
        video_data (dict): A dictionary containing video details.
    """
    conn = sqlite3.connect('bitchute.db')
    cursor = conn.cursor()

    video_views_trend = json.dumps(video_data['video_views_trend'])
    video_likes_trend = json.dumps(video_data['video_likes_trend'])
    video_dislikes_trend = json.dumps(video_data['video_dislikes_trend'])
    video_comments_trend = json.dumps(video_data['video_comments_trend'])
    video_hashtags = json.dumps(video_data['video_hashtags'])

    cursor.execute('''INSERT OR IGNORE INTO videos (video_title, video_url, video_views, video_likes, video_dislikes, video_channel_url, video_channel_name, video_comments_count, video_upload_date, video_hashtags, video_info_integrity_score, video_comments_trend, video_views_trend, video_likes_trend, video_dislikes_trend)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (video_data["video_title"], video_data["video_url"], video_data["video_views"], video_data["video_likes"], 
                    video_data["video_dislikes"], video_data["video_channel_url"], video_data["video_channel_name"], video_data["video_comments_count"], video_data["video_upload_date"],
                    video_hashtags, video_data['video_info_integrity_score'], video_comments_trend, video_views_trend, video_likes_trend, video_dislikes_trend))

    conn.commit()
    conn.close()

def update_video_data(video_data):
    """
    Updates existing video data in the database.

    Parameters:
        video_data (dict): A dictionary containing updated video details.
    """
    conn = sqlite3.connect('bitchute.db')
    cursor = conn.cursor()

    video_views_trend = json.dumps(video_data['video_views_trend'])
    video_likes_trend = json.dumps(video_data['video_likes_trend'])
    video_dislikes_trend = json.dumps(video_data['video_dislikes_trend'])
    video_comments_trend = json.dumps(video_data['video_comments_trend'])
    video_hashtags = json.dumps(video_data['video_hashtags'])

    cursor.execute('''UPDATE videos SET video_title=?, video_views=?, video_likes=?, video_dislikes=?, video_channel_name=?, video_comments_count=?, video_hashtags=?, video_comments_trend=?, video_views_trend=?, video_likes_trend=?, video_dislikes_trend=? 
                      WHERE video_url=?''', 
                   (video_data["video_title"], video_data["video_views"], video_data["video_likes"], 
                    video_data["video_dislikes"], video_data["video_channel_name"], video_data["video_comments_count"],
                    video_hashtags, video_comments_trend, video_views_trend, video_likes_trend, video_dislikes_trend, video_data["video_url"]))
    
    conn.commit()
    conn.close()

def fetch_video_data(video_url):
    """
    Fetches video data from the database based on the video URL.

    Parameters:
        video_url (str): The URL of the video.

    Returns:
        dict or None: A dictionary of video data or None if not found.
    """
    conn = sqlite3.connect('bitchute.db')
    cursor = conn.cursor()
    
    query = """
    SELECT video_id, 
           video_title, 
           video_url, 
           video_views, 
           video_likes, 
           video_dislikes, 
           video_channel_url, 
           video_channel_name, 
           video_comments_count, 
           video_upload_date, 
           video_hashtags, 
           video_info_integrity_score, 
           video_comments_trend, 
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

def fetch_video_url_list():
    """
    Fetches a list of all video URLs from the database.

    Returns:
        list: A list of video URLs.
    """
    conn = sqlite3.connect('bitchute.db')
    cursor = conn.cursor()

    query = "SELECT video_url FROM videos"

    video_list = []

    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        video_list.append(row[0])

    conn.close()

    return video_list