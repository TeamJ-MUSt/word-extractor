import spacy

def semantic_analysis(sentence):
    nlp = spacy.load("ja_core_news_sm")
    doc = nlp(sentence)
    # Perform semantic analysis tasks such as entity recognition and sentiment analysis
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    sentiment = doc.sentiment
    return entities, sentiment

sentence = "彼は素晴らしいアーティストです。"
entities, sentiment = semantic_analysis(sentence)
print("Entities:", entities)
print("Sentiment:", sentiment)
