from config import setup_browser
from scraper import get_video_data, search_hashtag_videos, search_videos
from process_data import process_video_data
from sql_operations import create_db, fetch_video_data, fetch_video_url_list
import time

def main():
    """
    Main function to manage the video data scraping and database updates.

    This function creates the database, enters a loop to periodically scrape 
    video data, and update the database with new entries. It sleeps for 1 hour 
    between iterations.
    """
    create_db()
    while True:
        driver = setup_browser()
        video_list = fetch_video_url_list() # Fetch current video URLs from the database

        # Update existing video data in the database
        update_data_in_db(driver)

        # If there are less than 41 videos, add new data
        if len(video_list) < 41:
            add_data_in_db(driver)
        
        driver.quit()
        time.sleep(3600)

def update_data_in_db(driver):
    """
    Update video data in the database for existing videos.

    Parameters:
        driver (webdriver.Chrome): The Selenium WebDriver instance to use for scraping.
    """
    video_list = fetch_video_url_list() # Fetch current video URLs from the database
    for video_url in video_list:
        video_info = get_video_data(driver, video_url) # Get updated video data
        process_video_data(video_info) # Process and save the video data

def add_data_in_db(driver):
    """
    Add new video data to the database based on search queries.

    Parameters:
        driver (webdriver.Chrome): The Selenium WebDriver instance to use for scraping.
    """
    search_list = ["biden", "trump", "us elections", "kamala"]
    for query in search_list:
        video_list = search_videos(driver, query) # Search for videos based on the query
        for video_url in video_list[:5]:
            video_in_db = fetch_video_data(video_url) # Check if the video is already in the database
            if video_in_db == None: # Only add if it's not already there
                video_info = get_video_data(driver, video_url)
                process_video_data(video_info)

if __name__ == "__main__":
    main()
