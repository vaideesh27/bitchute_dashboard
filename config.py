from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_browser():
    """
    Sets up a headless Chrome WebDriver with specified options.

    Returns:
        webdriver.Chrome: An instance of the Chrome WebDriver with configured options.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')
    options.add_argument("window-size=1920,1080")
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
