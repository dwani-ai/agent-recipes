import torch
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"

model_id = "google/embeddinggemma-300M"
model = SentenceTransformer(model_id).to(device=device)

print(f"Device: {model.device}")
print(model)
print("Total number of parameters in the model:", sum([p.numel() for _, p in model.named_parameters()]))


from datasets import Dataset

dataset = [
    ["How do I open a NISA account?", "What is the procedure for starting a new tax-free investment account?", "I want to check the balance of my regular savings account."],
    ["Are there fees for making an early repayment on a home loan?", "If I pay back my house loan early, will there be any costs?", "What is the management fee for this investment trust?"],
    ["What is the coverage for medical insurance?", "Tell me about the benefits of the health insurance plan.", "What is the cancellation policy for my life insurance?"],
]

# Convert the list-based dataset into a list of dictionaries.
data_as_dicts = [ {"anchor": row[0], "positive": row[1], "negative": row[2]} for row in dataset ]

# Create a Hugging Face `Dataset` object from the list of dictionaries.
train_dataset = Dataset.from_list(data_as_dicts)
print(train_dataset)


task_name = "STS"

def get_scores(query, documents):
  # Calculate embeddings by calling model.encode()
  query_embeddings = model.encode(query, prompt_name=task_name)
  doc_embeddings = model.encode(documents, prompt_name=task_name)

  # Calculate the embedding similarities
  similarities = model.similarity(query_embeddings, doc_embeddings)

  for idx, doc in enumerate(documents):
    print("Document: ", doc, "-> 🤖 Score: ", similarities.numpy()[0][idx])

query = "I want to start a tax-free installment investment, what should I do?"
documents = ["Opening a NISA Account", "Opening a Regular Savings Account", "Home Loan Application Guide"]

get_scores(query, documents)


## Training model

from sentence_transformers import SentenceTransformerTrainer, SentenceTransformerTrainingArguments
from sentence_transformers.losses import MultipleNegativesRankingLoss
from transformers import TrainerCallback

loss = MultipleNegativesRankingLoss(model)

args = SentenceTransformerTrainingArguments(
    # Required parameter:
    output_dir="my-embedding-gemma",
    # Optional training parameters:
    prompts=model.prompts[task_name],    # use model's prompt to train
    num_train_epochs=5,
    per_device_train_batch_size=1,
    learning_rate=2e-5,
    warmup_ratio=0.1,
    # Optional tracking/debugging parameters:
    logging_steps=train_dataset.num_rows,
    report_to="none",
)

class MyCallback(TrainerCallback):
    "A callback that evaluates the model at the end of eopch"
    def __init__(self, evaluate):
        self.evaluate = evaluate # evaluate function

    def on_log(self, args, state, control, **kwargs):
        # Evaluate the model using text generation
        print(f"Step {state.global_step} finished. Running evaluation:")
        self.evaluate()

def evaluate():
  get_scores(query, documents)

trainer = SentenceTransformerTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    loss=loss,
    callbacks=[MyCallback(evaluate)]
)
trainer.train()


get_scores(query, documents)

# Push to Hub
#model.push_to_hub("my-embedding-gemma")
