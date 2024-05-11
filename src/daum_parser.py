import requests
import time
import random
import re 

from bs4 import BeautifulSoup

max_delay = 5

def set_max_delay(delay : float):
    global max_delay
    if delay < 0:
        delay = 0
    max_delay = delay
    

def __random_delay():
    global max_delay
    min_delay = 1
    if max_delay <= min_delay:
        min_delay = 0
    time.sleep(random.random() * (max_delay - min_delay) + min_delay)

def __remove_number_prefix(input_string):
    return re.sub(r'^\d+\.\s*', '', input_string)

def get_definition_lists(keyword : str):
    __random_delay()
    url = f'https://dic.daum.net/search.do?q={keyword}&dic=jp'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        ul_tags = soup.find_all('ul', class_='list_search')
        result = []
        
        for ul in ul_tags:
            ul_group = []
            li_tags = ul.find_all('li')
            for li in li_tags:
                content = ''.join(li.find_all(string=True, recursive=True))
                ul_group.append(__remove_number_prefix(content))
            result.append(ul_group)
        return result
    
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return None

