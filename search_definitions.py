import argparse
import json
import os

#import src.daum_parser as parser
import src.naver_parser as searcher

verbose = False

def get_word_definitions(words):
    results = []
    for word in words:
        log(f"Querying {word}",end="")
        result = searcher.search(word, 4)
        if (result['definitions'] is None) or (len(result['definitions']) == 0):
            log("Not found from dictionary, therefore skipping it.")
            continue
        else:
            log("Done!")
        results.append(result)
    return results

def is_file(string):
    _, file_extension = os.path.splitext(string)
    return bool(file_extension)

def log(*args, **kwargs):
    if verbose:
        print(*args, **kwargs)

def main():
    parser = argparse.ArgumentParser(description='Fetch lyrics from bugs')
    parser.add_argument('query', help='Words to search in lemma form with white spaces in between, or a file that contains the words. Whether it is a file or not is determined by the dot(.).')
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
    
    dictionary = get_word_definitions(text.split(' '))

    if not args.out:
        print(dictionary)
    else:
        with open(args.out, 'w', encoding='UTF-8') as json_file:
            json.dump(dictionary, json_file, indent=4, ensure_ascii=False)
            if args.verbose:
                print("Saved results as json:", args.out)

    searcher.quit()

if __name__ == "__main__":
    main()
