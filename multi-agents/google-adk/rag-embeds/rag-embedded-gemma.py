# Load Gemma 3
from transformers import pipeline

pipeline = pipeline(
    task="text-generation",
    model="google/gemma-3-1b-it",
    device_map="auto",
    dtype="auto"
)

## Load Embedding Model

import torch
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"

model_id = "google/embeddinggemma-300M"
model = SentenceTransformer(model_id).to(device=device)

print(f"Device: {model.device}")
#print(model)
#print("Total number of parameters in the model:", sum([p.numel() for _, p in model.named_parameters()]))

"""print("Available tasks:")
for name, prefix in model.prompts.items():
  print(f" {name}: \"{prefix}\"")    
"""

corp_knowledge_base = [
  {
    "category": "HR & Leave Policies",
    "documents": [
      {
        "title": "Procedure for Unscheduled Absence",
        "content": "In the event of an illness or emergency preventing you from working, please notify both your direct manager and the HR department via email by 9:30 AM JST. The subject line should be 'Sick Leave - [Your Name]'. If the absence extends beyond two consecutive days, a doctor's certificate (診断書) will be required upon your return."
      },
      {
        "title": "Annual Leave Policy",
        "content": "Full-time employees are granted 10 days of annual paid leave in their first year. This leave is granted six months after the date of joining and increases each year based on length of service. For example, an employee in their third year of service is entitled to 14 days per year. For a detailed breakdown, please refer to the attached 'Annual Leave Accrual Table'."
      },
    ]
  },
  {
    "category": "IT & Security",
    "documents": [
      {
        "title": "Account Password Management",
        "content": "If you have forgotten your password or your account is locked, please use the self-service reset portal at https://reset.ourcompany. You will be prompted to answer your pre-configured security questions. For security reasons, the IT Help Desk cannot reset passwords over the phone or email. If you have not set up your security questions, please visit the IT support desk on the 12th floor of the Shibuya office with your employee ID card."
      },
      {
        "title": "Software Procurement Process",
        "content": "All requests for new software must be submitted through the 'IT Service Desk' portal under the 'Software Request' category. Please include a business justification for the request. All software licenses require approval from your department head before procurement can begin. Please note that standard productivity software is pre-approved and does not require this process."
      },
    ]
  },
  {
    "category": "Finance & Expenses",
    "documents": [
      {
        "title": "Expense Reimbursement Policy",
        "content": "To ensure timely processing, all expense claims for a given month must be submitted for approval no later than the 5th business day of the following month. For example, all expenses incurred in July must be submitted by the 5th business day of August. Submissions after this deadline may be processed in the next payment cycle."
      },
      {
        "title": "Business Trip Expense Guidelines",
        "content": "Travel expenses for business trips will, as a rule, be reimbursed based on the actual cost of the most logical and economical route. Please submit a travel expense application in advance when using the Shinkansen or airplanes. Taxis are permitted only when public transportation is unavailable or when transporting heavy equipment. Receipts are mandatory."
      },
    ]
  },
  {
    "category": "Office & Facilities",
    "documents": [
      {
        "title": "Conference Room Booking Instructions",
        "content": "All conference rooms in the Shibuya office can be reserved through your Calendar App. Create a new meeting invitation, add the attendees, and then use the 'Room Finder' feature to select an available room. Please be sure to select the correct floor. For meetings with more than 10 people, please book the 'Sakura' or 'Fuji' rooms on the 14th floor."
      },
      {
        "title": "Mail and Delivery Policy",
        "content": "The company's mail services are intended for business-related correspondence only. For security and liability reasons, employees are kindly requested to refrain from having personal parcels or mail delivered to the Shibuya office address. The front desk will not be able to accept or hold personal deliveries."
      },
    ]
  },
]

question = "How do I reset my password?" # @param ["How many days of annual paid leave do I get?", "How do I reset my password?", "What travel expenses can be reimbursed for a business trip?", "Can I receive personal packages at the office?"] {type:"string", allow-input: true}

# Define a minimum confidence threshold for a match to be considered valid
similarity_threshold = 0.4 # @param {"type":"slider","min":0,"max":1,"step":0.1}
     
# --- Helper Functions for Semantic Search ---

def _calculate_best_match(similarities):
    print(similarities)
    if similarities is None or similarities.nelement() == 0:
        return None, 0.0

    # Find the index and value of the highest score
    best_index = similarities.argmax().item()
    best_score = similarities[0, best_index].item()

    return best_index, best_score

def find_best_category(model, query, candidates):
    """
    Finds the most relevant category from a list of candidates.

    Args:
        model: The SentenceTransformer model.
        query: The user's query string.
        candidates: A list of category name strings.

    Returns:
        A tuple containing the index of the best category and its similarity score.
    """
    if not candidates:
        return None, 0.0

    # Encode the query and candidate categories for classification
    query_embedding = model.encode(query, prompt_name="Classification")
    candidate_embeddings = model.encode(candidates, prompt_name="Classification")

    print(candidates)
    return _calculate_best_match(model.similarity(query_embedding, candidate_embeddings))

def find_best_doc(model, query, candidates):
    """
    Finds the most relevant document from a list of candidates.

    Args:
        model: The SentenceTransformer model.
        query: The user's query string.
        candidates: A list of document dictionaries, each with 'title' and 'content'.

    Returns:
        A tuple containing the index of the best document and its similarity score.
    """
    if not candidates:
        return None, 0.0

    # Encode the query for retrieval
    query_embedding = model.encode(query, prompt_name="Retrieval-query")

    # Encode the document for similarity check
    doc_texts = [
        f"title: {doc.get('title', 'none')} | text: {doc.get('content', '')}"
        for doc in candidates
    ]
    candidate_embeddings = model.encode(doc_texts)

    print([doc['title'] for doc in candidates])

    # Calculate cosine similarity
    return _calculate_best_match(model.similarity(query_embedding, candidate_embeddings))

# --- Main Search Logic ---

# In your application, `best_document` would result from a search.
# We initialize it to None to ensure it always exists.
best_document = None

# 1. Find the most relevant category
print("Step 1: Finding the best category...")
categories = [item["category"] for item in corp_knowledge_base]
best_category_index, category_score = find_best_category(
    model, question, categories
)

# Check if the category score meets the threshold
if category_score < similarity_threshold:
    print(f" `-> 🤷 No relevant category found. The highest score was only {category_score:.2f}.")
else:
    best_category = corp_knowledge_base[best_category_index]
    print(f" `-> ✅ Category Found: '{best_category['category']}' (Score: {category_score:.2f})")

    # 2. Find the most relevant document ONLY if a good category was found
    print("\nStep 2: Finding the best document in that category...")
    best_document_index, document_score = find_best_doc(
        model, question, best_category["documents"]
    )

    # Check if the document score meets the threshold
    if document_score < similarity_threshold:
        print(f" `-> 🤷 No relevant document found. The highest score was only {document_score:.2f}.")
    else:
        best_document = best_category["documents"][best_document_index]
        # 3. Display the final successful result
        print(f" `-> ✅ Document Found: '{best_document['title']}' (Score: {document_score:.2f})")

qa_prompt_template = """Answer the following QUESTION based only on the CONTEXT provided. If the answer cannot be found in the CONTEXT, write "I don't know."

---
CONTEXT:
{context}
---
QUESTION:
{question}
"""

# First, check if a valid document was found before proceeding.
if best_document and "content" in best_document:
    # If the document exists and has a "content" key, generate the answer.
    context = best_document["content"]

    prompt = qa_prompt_template.format(context=context, question=question)

    messages = [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        },
    ]

    print("Question🙋‍♂️: " + question)
    # This part assumes your pipeline and response parsing logic are correct
    answer = pipeline(messages, max_new_tokens=256, disable_compile=True)[0]["generated_text"][1]["content"]
    print("Using document: " + best_document["title"])
    print("Answer🤖: " + answer)

else:
    # If best_document is None or doesn't have content, give a direct response.
    print("Question🙋‍♂️: " + question)
    print("Answer🤖: I'm sorry, I could not find a relevant document to answer that question.")