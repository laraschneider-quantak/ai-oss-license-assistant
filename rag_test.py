from openai import OpenAI
from math import sqrt

client = OpenAI(
    api_key="sk-proj-XYZ"
)

documents = [
    "MIT License is a permissive open source license.",
    "GPL v3 requires source code disclosure when distributed.",
    "Apache License 2.0 includes an explicit patent grant.",
    "BSD License is a permissive open source license."
]

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

def cosine_similarity(a, b):

    dot_product = sum(x * y for x, y in zip(a, b))

    magnitude_a = sqrt(sum(x * x for x in a))
    magnitude_b = sqrt(sum(y * y for y in b))

    return dot_product / (magnitude_a * magnitude_b)

document_embeddings = []

for doc in documents:
    embedding = get_embedding(doc)
    document_embeddings.append(embedding)

query = "Which license requires source code disclosure?"
query_embedding = get_embedding(query)

best_score = -1
best_document = ""

for doc, emb in zip(documents, document_embeddings):

    score = cosine_similarity(query_embedding, emb)

    print(score, doc)

    if score > best_score:
        best_score = score
        best_document = doc

print("\nBest Match:")
print(best_document)

response = client.responses.create(
    model="gpt-5",
    input=f"""
Answer the question using only the information below.

Information:
{best_document}

Question:
{query}
"""
)

print("\nLLM Answer:")
print(response.output_text)

