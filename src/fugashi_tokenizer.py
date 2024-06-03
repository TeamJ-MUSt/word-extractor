import fugashi
import re

tagger = fugashi.Tagger()

def is_japanese_only(s: str) -> bool:
    # Define the regex pattern for Japanese characters
    pattern = r'^[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FBF]+$'
    # Check if the string matches the pattern
    return bool(re.match(pattern, s))

def get_tokens(text :str):
    words = [word for word in tagger(text)]
    tokens = []
    for word in words:
        if word.feature.lemma is None or word.feature.lemma == "":
            continue
        if not is_japanese_only(word.surface) or not is_japanese_only(word.feature.lemma):
            continue
        info = {}
        info["surface"] = word.surface
        info["speechFields"] = [word.feature.pos1, word.feature.pos2, word.feature.pos3, word.feature.pos4]  #speech fields
        #info["pronounciation"] = word.feature.lForm   #pronounciation of lemma, (alternative)pron: pronounciation including ー. 
        info["lemma"] = word.feature.lemma #(alternative)orth: written lemma
        #goshu: word type

        if not any(__compare_tokens(info, existing_item) for existing_item in tokens):
            tokens.append(info)
    return tokens
        

def __compare_tokens(dict1, dict2):
    return dict1['lemma'] == dict2['lemma'] and dict1['speechFields'][0] == dict2['speechFields'][0]
