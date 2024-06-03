import argparse
import json
import os

#import src.daum_parser as parser
import src.naver_parser as searcher


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from subprocess import CREATE_NO_WINDOW

from threading import Thread

from src.timer import Timer

verbose = False


def initialize_browser():
    headless = True
    # Path to chromedriver executable
    service = Service('chromedriver-win64/chromedriver.exe')
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")

    if headless:
        service.creation_flags = CREATE_NO_WINDOW
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def split_words(words, thread_count):
    chuncks=[]
    size = len(words) // thread_count
    for i in range(thread_count):
        if i < thread_count-1:
            chuncks.append(words[i * size : (i+1) * size])
        else:
            chuncks.append(words[i * size:])
    return chuncks

thread_results = []
def get_word_definitions_job(words, index):
    driver = initialize_browser()

    global thread_results
    results = []
    for word in words:
        log(f"Querying {word}",end="")
        result = searcher.search(driver, word, 4)
        if (result['definitions'] is None) or (len(result['definitions']) == 0):
            log("Not found from dictionary, therefore skipping it.")
            continue
        else:
            log("Done!")
        results.append(result)

    driver.quit()
    thread_results[index] = results

def get_word_definitions(words, thread_count):
    timer = Timer()
    timer.start('def')
    threads = []
    word_chucks = split_words(words, thread_count)
    global thread_results
    thread_results = [[] for i in range(thread_count)]

    for i in range(thread_count):
        thread = Thread(target=get_word_definitions_job, args=(word_chucks[i], i))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    result = []
    for tresult in thread_results:
        result.extend(tresult)
    timer.stop(verbose=verbose)
    return result

def is_file(string):
    _, file_extension = os.path.splitext(string)
    return bool(file_extension)

def log(*args, **kwargs):
    if verbose:
        print(*args, **kwargs)

def main():
    parser = argparse.ArgumentParser(description='Fetch lyrics from bugs')
    parser.add_argument('query', help='Words to search in lemma form with white spaces in between, or a file that contains the words. Whether it is a file or not is determined by the dot(.).')
    parser.add_argument('--threads', type=int, default=1, help='Number of threads for multi-threading')
    parser.add_argument('--out', help='Output file path. Outputs to standard output if not specified.')
    parser.add_argument('--verbose', action='store_true', help='Prints current queries and progress')
    args = parser.parse_args()

    if not args.query:
        if args.verbose:
            print("Error: Please provide words using --query")
        return
    
    global verbose
    verbose = args.verbose
    
    if is_file(args.query):
        with open(args.query, 'r', encoding='UTF-8') as file:
            text = file.read()
    else:
        text = args.query
    
    dictionary = get_word_definitions(text.split(' '), args.threads)

    if not args.out:
        print(dictionary)
    else:
        with open(args.out, 'w', encoding='UTF-8') as json_file:
            json.dump(dictionary, json_file, indent=4, ensure_ascii=False)
            if args.verbose:
                print("Saved results as json:", args.out)

if __name__ == "__main__":
    main()
