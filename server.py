from flask import Flask, jsonify, request
from flask_cors import CORS  # Import the CORS package
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import os
import requests
import html2text

# Constants
CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'
CHROME_BINARY_PATH = '/Users/jchen/chrome/mac_arm-116.0.5793.0/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
NEWS_URL = "https://www.ibm.com/new"
DEFAULT_NEWS_SIZE = 10

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

def setup_driver():
    chrome_options = Options()
    chrome_options.binary_location = CHROME_BINARY_PATH
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    service = Service(CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

def fetch_news_items(driver, size):
    driver.get(f"{NEWS_URL}?size={size}")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ibm--horizontal-media-row"))
    )
    return driver.find_elements(By.CLASS_NAME, 'ibm--horizontal-media-row')

def extract_news_details(item):
    def safe_find_element(by, value):
        try:
            return item.find_element(by, value).text.strip()
        except NoSuchElementException:
            return ''

    news_url = item.get_attribute('href')
    date = safe_find_element(By.CLASS_NAME, 'ibm--horizontal-media-row__date')
    news_type = safe_find_element(By.CLASS_NAME, 'ibm--horizontal-media-row__format')
    heading = safe_find_element(By.CLASS_NAME, 'ibm--horizontal-media-row__heading')
    content_summary = safe_find_element(By.TAG_NAME, 'p')
    try:
        image = item.find_element(By.CLASS_NAME, 'ibm--horizontal-media-row__media').find_element(By.TAG_NAME, 'img').get_attribute('src')
    except NoSuchElementException:
        image = ''
    
    return {
        "url": news_url,
        "date": date,
        "type": news_type,
        "title": heading,
        "summary": content_summary,
        "image": image
    }

@app.route('/news', methods=['GET'])
def get_news():
    size = request.args.get('size', default=DEFAULT_NEWS_SIZE, type=int)
    driver = setup_driver()
    try:
        news_items = fetch_news_items(driver, size)
        news_details = [extract_news_details(item) for item in news_items]
        return jsonify(news_details)
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
