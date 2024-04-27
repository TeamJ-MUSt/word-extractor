import fugashi


tagger = fugashi.Tagger()

def get_tokens(text :str):
    words = [word for word in tagger(text)]
    tokens = []
    for word in words:
        if word.feature.lemma is None:
            continue
        info = {}
        info["surface"] = word.surface
        info["speechFields"] = [word.feature.pos1, word.feature.pos2, word.feature.pos3, word.feature.pos4]  #speech fields
        info["pronounciation"] = word.feature.lForm   #pronounciation of lemma, (alternative)pron: pronounciation including ー. 
        info["lemma"] = word.feature.lemma #(alternative)orth: written lemma
        #goshu: word type
        if not any(__compare_tokens(info, existing_item) for existing_item in tokens):
            tokens.append(info)
    return tokens
        

def __compare_tokens(dict1, dict2):
    return dict1['lemma'] == dict2['lemma'] and dict1['speechFields'][0] == dict2['speechFields'][0]
