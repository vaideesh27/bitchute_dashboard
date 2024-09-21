from datetime import datetime
from utils import info_integrity_score
import json
from sql_operations import insert_video_data, update_video_data, fetch_video_data

def process_video_data(video_data):
    """
    Process and store video data in the database.

    Parameters:
        video_data (dict): A dictionary containing video information and metrics.
    """
    # Initialize growth metrics
    video_data['views_growth'] = {'t': datetime.utcnow().strftime('%Y-%m-%d %H:00:00'), 'c': video_data['video_views']}
    video_data['likes_growth'] = {'t': datetime.utcnow().strftime('%Y-%m-%d %H:00:00'), 'c': video_data['video_likes']}
    video_data['dislikes_growth'] = {'t': datetime.utcnow().strftime('%Y-%m-%d %H:00:00'), 'c': video_data['video_dislikes']}
    video_data['comments_growth'] = {'t': datetime.utcnow().strftime('%Y-%m-%d %H:00:00'), 'c': video_data['video_comments_count']}

    # Check if the video already exists in the database
    video_data_in_db = fetch_video_data(video_data['video_url'])
    
    if video_data_in_db == None:
        # If video is new, initialize trend lists
        video_data['video_views_trend'] = [video_data['views_growth']]
        video_data['video_likes_trend'] = [video_data['likes_growth']]
        video_data['video_dislikes_trend'] = [video_data['dislikes_growth']]
        video_data['video_comments_trend'] = [video_data['comments_growth']]

        # Calculate the integrity score for the new video
        video_data['video_info_integrity_score'] = info_integrity_score()

        # Insert the new video data into the database
        insert_video_data(video_data)
    else:
        # If video already exists, update the trend data
        video_views_trend = json.loads(video_data_in_db['video_views_trend'])
        video_likes_trend = json.loads(video_data_in_db['video_likes_trend'])
        video_dislikes_trend = json.loads(video_data_in_db['video_dislikes_trend'])
        video_comments_trend = json.loads(video_data_in_db['video_comments_trend'])

        # Append the new growth metrics to the existing trends
        video_views_trend.append(video_data['views_growth'])
        video_likes_trend.append(video_data['likes_growth'])
        video_dislikes_trend.append(video_data['dislikes_growth'])
        video_comments_trend.append(video_data['comments_growth'])

        # Update video data trends
        video_data['video_views_trend'] = video_views_trend
        video_data['video_likes_trend'] = video_likes_trend
        video_data['video_dislikes_trend'] = video_dislikes_trend
        video_data['video_comments_trend'] = video_comments_trend

        # Update the existing video data in the database
        update_video_data(video_data)