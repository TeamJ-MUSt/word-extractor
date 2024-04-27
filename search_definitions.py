import argparse
import json
import os

import src.daum_parser as parser
import src.fugashi_tokenizer as tokenizer

verbose = False

parser.set_max_delay(2)


def get_word_definitions(words):
    result = []
    for word in words:
        definitions = parser.get_definition_lists(word)
        if (definitions is None) or (len(definitions) == 0):
            log(word, "is not found from dictionary, therefore skipping it.")
            continue
        result.append({'word' : word, 'definitions':definitions})
    return result

def is_file(string):
    _, file_extension = os.path.splitext(string)
    return bool(file_extension)

def log(*args, **kwargs):
    if verbose:
        print(*args, **kwargs)

def main():
    parser = argparse.ArgumentParser(description='Fetch lyrics from bugs')
    parser.add_argument('query', help='Search query string, or Input file path of search queries. Whether it is a file or not is determined by the dot(.).')
    parser.add_argument('--out', help='Output file path. Outputs to standard output if not specified.')
    parser.add_argument('--verbose', action='store_true', help='Prints current queries and progress')
    args = parser.parse_args()

    if not args.query:
        if args.verbose:
            print("Error: Please provide an query using --query")
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


if __name__ == "__main__":
    main()
