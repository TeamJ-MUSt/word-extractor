from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine

# Load pre-trained model tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-uncased')
# Load pre-trained model
model = BertModel.from_pretrained('bert-base-multilingual-uncased')

# Define the sentences
sentence1 = "오늘은 눈이 내렸다."
sentence2 = "오늘은 eye이 내렸다."
sentence3 = "오늘은 snow이 내렸다."

# Tokenize the sentences
inputs1 = tokenizer(sentence1, return_tensors="pt", padding=True, truncation=True)
inputs2 = tokenizer(sentence2, return_tensors="pt", padding=True, truncation=True)
inputs3 = tokenizer(sentence3, return_tensors="pt", padding=True, truncation=True)

# Get BERT representations
with torch.no_grad():
    outputs1 = model(**inputs1)
    outputs2 = model(**inputs2)
    outputs3 = model(**inputs3)

# Get the pooled output (CLS token)
sentence_embedding1 = torch.mean(outputs1.last_hidden_state, dim=1).numpy()
sentence_embedding2 = torch.mean(outputs2.last_hidden_state, dim=1).numpy()
sentence_embedding3 = torch.mean(outputs3.last_hidden_state, dim=1).numpy()

# Calculate cosine similarity
similarity_1_2 = 1 - cosine(sentence_embedding1, sentence_embedding2)
similarity_1_3 = 1 - cosine(sentence_embedding1, sentence_embedding3)
similarity_2_3 = 1 - cosine(sentence_embedding2, sentence_embedding3)

print("Similarity between sentence 1 and sentence 2:", similarity_1_2)
print("Similarity between sentence 1 and sentence 3:", similarity_1_3)
print("Similarity between sentence 2 and sentence 3:", similarity_2_3)
