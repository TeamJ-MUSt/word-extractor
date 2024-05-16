import fugashi

# This is our sample text.
# "Fugashi" is a Japanese snack primarily made of gluten.
#text = "空にある何かを見つめてたら12cars"
text = '遥か 遠く 終わらない べテルギウス'
# The Tagger object holds state about the dictionary. 
tagger = fugashi.Tagger()

words = [word for word in tagger(text)]

print(text)
for word in words:
    print(word.surface, end = " ")
    info = {}
    info["surface"] = word.surface
    info["speechFields"] = [word.feature.pos1, word.feature.pos2, word.feature.pos3, word.feature.pos4]  #speech fields
    info["pronounciation"] = word.feature.lForm   #pronounciation of lemma, (alternative)pron: pronounciation including ー. 
    info["lemma"] = word.feature.lemma #(alternative)orth: written lemma
    #goshu: word type
    print(info)


    
