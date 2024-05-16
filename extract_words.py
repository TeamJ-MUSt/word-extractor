import argparse
import json
import os

import src.daum_parser as parser
import src.fugashi_tokenizer as tokenizer

verbose = False

parser.set_max_delay(2)



def get_important_tokens(text):
    tokens = tokenizer.get_tokens(text)
    important_tokens = []
    banned_fields = ['助詞', '助動詞', '数詞']
    for token in tokens:
        ban = False
        for field in token['speechFields']:
            if field in banned_fields:
                ban = True
                break
        if ban:
            continue
        important_tokens.append(token)
    return important_tokens


def is_file(string):
    _, file_extension = os.path.splitext(string)
    return bool(file_extension)

def log(*args, **kwargs):
    if verbose:
        print(*args, **kwargs)

def main():
    parser = argparse.ArgumentParser(description='Fetch lyrics from bugs')
    parser.add_argument('query', help='The text to extract words from, or a file of texts. Whether it is a file or not is determined by the dot(.).')
    parser.add_argument('--out', help='Output file path. Outputs to standard output if not specified.')
    parser.add_argument('--verbose', action='store_true', help='Prints current queries and progress')
    args = parser.parse_args()

    if not args.query:
        if args.verbose:
            print("Error: Please provide text using --query")
        return
    
    global verbose
    verbose = args.verbose
    
    if is_file(args.query):
        with open(args.query, 'r', encoding='UTF-8') as file:
            text = file.read()
    else:
        text = args.query
    
    tokens = get_important_tokens(text)

    if not args.out:
        print(tokens)
    else:
        with open(args.out, 'w', encoding='UTF-8') as json_file:
            json.dump(tokens, json_file, indent=4, ensure_ascii=False)
            if args.verbose:
                print("Saved results as json:", args.out)


if __name__ == "__main__":
    main()
