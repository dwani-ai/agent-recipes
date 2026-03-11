
import torch
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"

model_id = "google/embeddinggemma-300M"
model = SentenceTransformer(model_id).to(device=device)

print(f"Device: {model.device}")
print(model)
print("Total number of parameters in the model:", sum([p.numel() for _, p in model.named_parameters()]))


## Step 2

words = ["apple", "banana", "car"]

# Calculate embeddings by calling model.encode()
embeddings = model.encode(words)

print(embeddings)
for idx, embedding in enumerate(embeddings):
  print(f"Embedding {idx+1} (shape): {embedding.shape}")



##Step 3

# The sentences to encode
sentence_high = [
    "The chef prepared a delicious meal for the guests.",
    "A tasty dinner was cooked by the chef for the visitors."
]
sentence_medium = [
    "She is an expert in machine learning.",
    "He has a deep interest in artificial intelligence."
]
sentence_low = [
    "The weather in Tokyo is sunny today.",
    "I need to buy groceries for the week."
]

for sentence in [sentence_high, sentence_medium, sentence_low]:
  print("🙋‍♂️")
  print(sentence)
  embeddings = model.encode(sentence)
  similarities = model.similarity(embeddings[0], embeddings[1])
  print("`-> 🤖 score: ", similarities.numpy()[0][0])


## Step 4 - Using Prompts for Tasks

print("Available tasks:")
for name, prefix in model.prompts.items():
  print(f" {name}: \"{prefix}\"")
print("-"*80)

for sentence in [sentence_high, sentence_medium, sentence_low]:
  print("🙋‍♂️")
  print(sentence)
  embeddings = model.encode(sentence, prompt_name="STS")
  similarities = model.similarity(embeddings[0], embeddings[1])
  print("`-> 🤖 score: ", similarities.numpy()[0][0])


### Step 5 - Classification

labels = ["Billing Issue", "Technical Support", "Sales Inquiry"]

sentence = [
  "Excuse me, the app freezes on the login screen. It won't work even when I try to reset my password.",
  "I would like to inquire about your enterprise plan pricing and features for a team of 50 people.",
]

# Calculate embeddings by calling model.encode()
label_embeddings = model.encode(labels, prompt_name="Classification")
embeddings = model.encode(sentence, prompt_name="Classification")

# Calculate the embedding similarities
similarities = model.similarity(embeddings, label_embeddings)
print(similarities)

idx = similarities.argmax(1)
print(idx)

for example in sentence:
  print("🙋‍♂️", example, "-> 🤖", labels[idx[sentence.index(example)]])


## Step -5 - Matryoshka Representation Learning (MRL)
def check_word_similarities():
  # Calculate the embedding similarities
  print("similarity function: ", model.similarity_fn_name)
  similarities = model.similarity(embeddings[0], embeddings[1:])
  print(similarities)

  for idx, word in enumerate(words[1:]):
    print("🙋‍♂️ apple vs.", word, "-> 🤖 score: ", similarities.numpy()[0][idx])

# Calculate embeddings by calling model.encode()
embeddings = model.encode(words, prompt_name="STS")

check_word_similarities()

###

embeddings = model.encode(words, truncate_dim=512, normalize_embeddings=True)

for idx, embedding in enumerate(embeddings):
  print(f"Embedding {idx+1}: {embedding.shape}")

print("-"*80)
check_word_similarities()


###

model = SentenceTransformer(model_id, truncate_dim=256, similarity_fn_name="dot").to(device=device)
embeddings = model.encode(words, prompt_name="STS", normalize_embeddings=True)

for idx, embedding in enumerate(embeddings):
  print(f"Embedding {idx+1}: {embedding.shape}")

print("-"*80)
check_word_similarities()
