from datetime import datetime
import random

def preprocess_date_string(date_string):
    """
    Cleans up a date string by removing ordinal suffixes and extra punctuation.
    
    Parameters:
        date_string (str): The raw date string.
    
    Returns:
        str: A cleaned date string.
    """
    date_string = date_string.replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
    date_string = date_string.strip().rstrip('.')
    return date_string

def convert_to_datetime(date_string):
    """
    Converts a cleaned date string into a standardized datetime format.
    
    Parameters:
        date_string (str): The raw date string.
    
    Returns:
        str: A formatted date string in 'YYYY-MM-DD HH:MM:SS' format.
    """
    clean_date_string = preprocess_date_string(date_string)
    format_str = 'Fir published at %H:%M UTC on %B %d, %Y'
    return datetime.strptime(clean_date_string, format_str).strftime('%Y-%m-%d %H:%M:%S')

def extract_views(view_string):
    """
    Extracts the view count from a string representation of views.
    
    Parameters:
        view_string (str): The string containing view information.
    
    Returns:
        int: The numeric view count.
    """
    parts = view_string.split()
    return int(parts[0])

def info_integrity_score():
    """
    Generates a mock integrity score for a video based on hypothetical AI analysis.
    
    This function simulates the process of capturing video data and analyzing audio to text 
    for calculating an integrity score. Currently, it returns a random integer between 1 and 100.
    
    Returns:
        int: A random integrity score between 1 and 100, representing the videos integrity.
    """
    return random.randint(1, 100)