import sys
sys.stdout.reconfigure(encoding='utf-8')

import time
import re
import os
import re
import unicodedata
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


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
        cleaned_text = cleaned_text.replace('(','').replace(')','').replace('-','')
        cleaned_text = cleaned_text.replace('∙','·') # these two are different
        split_texts = cleaned_text.split('·')
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
    korean_pattern = re.compile("[가-힣]+")
    return bool(korean_pattern.search(text))

def has_japanese_characters(text):
    japanese_pattern = re.compile('[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]+')
    return bool(japanese_pattern.search(text))

def remove_parentheses_content(s: str, predicate) -> str:
    stack = []
    content = ''

    # Collect positions of parentheses
    for i, char in enumerate(s):
        content += char
        if char == '(':
            stack.append(len(content))
        elif char == ')':
            if stack:
                start = stack.pop()

def remove_parentheses_content(s: str, predicate) -> str:
    stack = []
    content = ''

    # Collect positions of parentheses
    for i, char in enumerate(s):
        if char == '(':
            content += char
            stack.append(len(content)-1)
        elif char == ')':
            if stack:
                start = stack.pop()
                if predicate(content[start:]):
                    content = content[:start]
                else:
                    content+=')'
        else:
            content += char
    return content.strip()


def slice_until(input_string, delimiter, N):
    parts = input_string.split(delimiter)
    if len(parts) < N:
        return input_string
    
    chuncks = []
    for chunck in parts:
        if contains_korean(chunck):
            chuncks.append(chunck)
        if len(chuncks) >= N:
            break
    result = delimiter.join(chuncks)
    
    return result

def is_only_hiragana(s):
    # Define the regular expression for Hiragana characters
    hiragana_regex = re.compile(r'^[\u3040-\u309F]+$')
    
    # Use the regex to check if the string matches the pattern
    return bool(hiragana_regex.match(s))

def search_definitions_and_pron_and_level(driver, query, N):
    url = f'https://ja.dict.naver.com/#/search?range=word&query={query}'
    definitions = []
    level = -1
    pron = ""
    driver.get(url)

    # wait until loaded
    try:
        element = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.origin"))
        )
    except TimeoutException:
        return definitions, pron, level

    # scroll to bottom 
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        count = 0
        while count <= 4:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.25)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            count += 1

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
                if pron == "":
                    for candidate_word in texts:
                        if is_only_hiragana(candidate_word):
                            pron = candidate_word
                            break
                # Find 'p.mean' within the same row if the origin is valid
                mean_elements = row.find_elements(By.CSS_SELECTOR, "p.mean")
                for element in mean_elements:
                    cleared_string = remove_span_mark_content(element.get_attribute('innerHTML'))
                    if cleared_string in definitions:
                        continue
                    if not contains_korean(cleared_string):
                        continue

                    def pred(text):
                        if len(text) == 0 or len(text) > 7 or has_japanese_characters(text) or not contains_korean(text):
                            return True
                        return False

                    cleared_string = remove_parentheses_content(cleared_string.strip(), pred)
                    cleared_string = slice_until(cleared_string, ';', 2)
                    cleared_string = slice_until(cleared_string, ',', 2)
                    cleared_string = cleared_string.replace('\'','\\\'')
                    cleared_string = cleared_string.split(':')[-1].strip()
                    cleared_string = cleared_string.split('：')[-1].strip()

                    #print(cleared_string, (cleared_string not in definitions) and contains_korean(cleared_string))
                    if (cleared_string not in definitions) and contains_korean(cleared_string):
                        definitions.append(cleared_string)

                    if len(definitions) >= N:
                        break
                
    except TimeoutException:
        print("Timed out waiting for page to load")

    if pron == "":
        pron = query
    return definitions, pron, level


def search(driver, word, N):
    definitions, pron, level = search_definitions_and_pron_and_level(driver, word, N)
    return {'word': word, 'definitions': definitions, 'pronounciation':pron, 'level':level}
