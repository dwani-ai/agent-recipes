
import torch
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"

model_id = "google/embeddinggemma-300M"
model = SentenceTransformer(model_id).to(device=device)

print(f"Device: {model.device}")
print(model)
print("Total number of parameters in the model:", sum([p.numel() for _, p in model.named_parameters()]))

"""
## Step 2

words = ["apple", "banana", "car"]

# Calculate embeddings by calling model.encode()
embeddings = model.encode(words)

print(embeddings)
for idx, embedding in enumerate(embeddings):
  print(f"Embedding {idx+1} (shape): {embedding.shape}")
"""


"""

Step 3

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

"""