from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from utils import convert_to_datetime, extract_views
import urllib.parse

def search_videos(driver, query):
    """
    Searches for videos on Bitchute using a specified query.

    Parameters:
        driver (webdriver): The Selenium WebDriver instance.
        query (str): The search term to query Bitchute.

    Returns:
        list: A list of video URLs matching the search query.
    """
    search = urllib.parse.quote(query)
    url = f"https://www.bitchute.com/search?query={search}&kind=video&sensitivity_id=normal&duration=all&sort=new"
    driver.get(url)
    time.sleep(10)
    
    videos_link_list = []
    videos_links = driver.find_elements(By.XPATH, '//*[@id="video-card"]/div[2]/div/div[2]/a[1]')
    
    for video in videos_links:
        link = video.get_attribute("href")
        videos_link_list.append(link)
    
    return videos_link_list

def get_video_data(driver, video_url):
    """
    Retrieves video data from a given video URL.

    Parameters:
        driver (webdriver): The Selenium WebDriver instance.
        video_url (str): The URL of the video to scrape data from.

    Returns:
        dict: A dictionary containing the video data.
    """
    driver.get(video_url)
    time.sleep(10)

    upload_exact = driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div/span')
    actions = ActionChains(driver)
    actions.move_to_element(upload_exact).perform()
    upload_exact.click()
    time.sleep(3)

    parent_hashtag_element = driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[2]')
    anchor_tags = parent_hashtag_element.find_elements(By.XPATH, './/a')
    hashtags = [anchor.find_element(By.XPATH, './div/div[2]').text for anchor in anchor_tags]

    video_title = driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div').text
    views = driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div').text
    likes = driver.find_element(By.XPATH, '//*[@id="responsive_menu"]/div[1]/button[1]/span[2]/span').text
    dislikes = driver.find_element(By.XPATH, '//*[@id="responsive_menu"]/div[1]/button[2]/span[2]/span').text
    channel_url = driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div/div[2]/a').get_attribute("href")
    channel_name = driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div/div[2]/a/div').text
    upload_date = driver.find_element(By.XPATH, '//*[@id="q-portal--tooltip--1"]/div').text
    comment_count = driver.find_element(By.XPATH, '//*[@id="comments-container"]/ul/div[1]/li[1]/span[1]').text

    video_data = {
        "video_title": video_title,
        "video_url": video_url,
        "video_views": extract_views(views),
        "video_likes": int(likes) if likes != '' else 0,
        "video_dislikes": int(dislikes) if dislikes != '' else 0,
        "video_channel_url": channel_url,
        "video_channel_name": channel_name,
        "video_comments_count": int(comment_count) if comment_count != '' else 0,
        "video_upload_date": convert_to_datetime(upload_date),
        "video_hashtags": hashtags
    }
    
    return video_data

def search_hashtag_videos(driver, hashtag):
    """
    Searches for videos under a specific hashtag on Bitchute.

    Parameters:
        driver (webdriver): The Selenium WebDriver instance.
        hashtag (str): The hashtag to search for.

    Returns:
        list: A list of video URLs associated with the hashtag.
    """
    search = urllib.parse.quote(hashtag)
    url = f"https://www.bitchute.com/hashtag/{search}"
    driver.get(url)
    time.sleep(10)
    
    videos_link_list = []
    videos_links = driver.find_elements(By.XPATH, '//*[@id="video-card"]/div[2]/div/div[2]/a[1]')
    
    for video in videos_links:
        link = video.get_attribute("href")
        videos_link_list.append(link)
    
    return videos_link_list