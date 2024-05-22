from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import re
import os
from subprocess import CREATE_NO_WINDOW
import re
import unicodedata
from bs4 import BeautifulSoup


def initialize_browser():
    # Path to chromedriver executable
    service = Service('chromedriver-win64/chromedriver.exe')
    service.creation_flags = CREATE_NO_WINDOW
    
    options = webdriver.ChromeOptions()
    # Optional: options for headless mode (no GUI window)
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(service=service, options=options)
    return driver

def remove_span_mark_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    for span in soup.find_all('span', class_='mark'):
        span.decompose()  # Removes the tag and its content
    return soup.get_text()

def process_texts(texts):
    result = []
    for text in texts:
        # Remove brackets
        cleaned_text = text.replace('[', '').replace(']', '')
        # Split by '&'
        split_texts = cleaned_text.split('·')
        # Trim spaces and collect both original cleaned text and splits
        #result.append(cleaned_text)
        result.extend([item.strip() for item in split_texts])
    return result

def find_jlpt(text):
    for string in text:
        if 'JLPT' in string:
            parts = string.split()
            return int(parts[1]) if len(parts) > 1 else -1
    return -1

def contains_korean(text):
    # Regular expression to match Korean characters
    korean_pattern = re.compile("[\u3131-\u3163\uac00-\ud7a3]+")
    return bool(korean_pattern.search(text))

def has_japanese_characters(text):
    for char in text:
        if 'CJK UNIFIED IDEOGRAPH' in unicodedata.name(char, ''):
            return True
    return False

def remove_specific_parentheses_content(text):
    text = re.sub(r'\(\(', '(', text)
    text = re.sub(r'\)\)', ')', text)

    pattern = re.compile(r'\((.*?)\)')
    matches = pattern.findall(text)

    for match in matches:
        clean_match = ''.join(match.split())
        if len(clean_match) == 0 or len(clean_match) > 5 or has_japanese_characters(match) or not contains_korean(match):
            text = text.replace(f'({match})', '')
    return text.strip()

def slice_until(input_string, delimiter, N):
    parts = input_string.split(delimiter)
    if len(parts) < N:
        return input_string
    result = delimiter.join(parts[:N]) + delimiter
    
    return result
def search_definitions_and_level(driver, query, N):
    url = f'https://ja.dict.naver.com/#/search?range=word&query={query}'
    definitions = []
    level = -1
    driver.get(url)
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while len(definitions) < N:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load more items
            time.sleep(0.5)
            
            # Attempt to find the container rows that include the origin and definitions
            rows = driver.find_elements(By.CSS_SELECTOR, "div.row")
            for row in rows:
                origin_div = row.find_element(By.CSS_SELECTOR, "div.origin")
                # Check for the existence of 'a' tag or 'span' with class 'text._kanji'
                origin_texts = origin_div.find_elements(By.CSS_SELECTOR, "a, span.text._kanji")
                # Extract text and check if it matches the query
                texts = process_texts([origin_text.text for origin_text in origin_texts])
                valid = any(text == query for text in texts)
                if valid:
                    if level < 0:
                        level = find_jlpt(texts)
                    # Find 'p.mean' within the same row if the origin is valid
                    mean_elements = row.find_elements(By.CSS_SELECTOR, "p.mean")
                    for element in mean_elements:
                        cleaned_text = remove_span_mark_content(element.get_attribute('innerHTML'))
                        if cleaned_text in definitions:
                            continue
                        if not contains_korean(cleaned_text):
                            continue
                        
                        cleared_string = remove_specific_parentheses_content(element.text)
                        cleared_string = slice_until(cleared_string, ';', 3)
                        cleared_string = slice_until(cleared_string, ',', 3)
                        cleared_string = cleared_string.replace('\'','\\\'')
                        cleared_string = cleared_string.split(':')[-1].strip()

                        definitions.append(cleared_string)
                        if len(definitions) >= N:
                            break
                
                if len(definitions) >= N:
                    break
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    except TimeoutException:
        print("Timed out waiting for page to load")

    return definitions, level

driver = initialize_browser()

def search(word, N):
    definitions, level = search_definitions_and_level(driver, word, N)
    return {'word': word, 'definitions': definitions, 'level':level}

def quit():
    driver.quit()