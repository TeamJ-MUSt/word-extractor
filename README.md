# words-extractor
Python script that will extract words and search definitions of a japanese text.

## Environment
Python 3.9.12

## How to run
1. Clone this repository
```
git clone https://github.com/TeamJ-MUSt/word-extractor
cd word-extractor
```
2. Install `requirements.txt` and [UniDic](https://github.com/polm/unidic-py?tab=readme-ov-file). Installing UniDic will take a while.
```
pip install -r requirements.txt
python -m unidic download
```
3. Run `extract_words.py` or `search_definitions.py` with arguments

### extract_words.py
Running this will tokenize the given query using fugashi, a nice wrapper of Mecab. It will return a list of dictionaries, where each dictionary contains lema, speeh fields, and others. Connecting words(助詞) will be excluded.

usage: `python extract_words.py [-h] [--out OUT] [--verbose] query`

positional arguments:  
- `query`: The text to extract words from, or a file of texts. Whether it is a file or not is determined by the dot(.).  

optional arguments:  
- `-h`, `--help`: Show help message  
- `--out OUT`: Output file path. Outputs to standard output if not specified.  
- `--verbose`: Prints current queries and progress. Defaults to `False`
```
// Using simple query, output to file, log process
python extract_words.py 空にある何かを見つめてたら --out result.txt --verbose

// Using file query, output to standard output
python fetch.py queries.txt
```
### search_definitions.py
Running this will search the korean definitions of given words in query. It will return a list of dictionaries, where each dictionary has the list of definitions. The query should contain the lemma forms.

usage: `python search_definitions.py [-h] [--out OUT] [--verbose] query`

positional arguments:  
- `query`: Words to search in lemma form with white spaces in between, or a file that contains the words. Whether it is a file or not is determined by the dot(.).  

optional arguments:  
- `-h`, `--help`: Show help message  
- `--out OUT`: Output file path. Outputs to standard output if not specified.  
- `--verbose`: Prints current queries and progress. Defaults to `False`
```
// Using simple query, output to file, log process
python extract_words.py "空 何 てる" --out result.txt --verbose

// Using file query, output to standard output
python extract_words.py queries.txt
```
