import os
from math import sqrt
from openai import OpenAI

client = OpenAI(
    api_key="sk-proXYZ"
)

folder = "knowledge"


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


documents = []

for filename in os.listdir(folder):
    filepath = os.path.join(folder, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    documents.append({
        "filename": filename,
        "content": content,
        "embedding": get_embedding(content)
    })

query = "Which license requires source code disclosure?"
query_embedding = get_embedding(query)

best_score = -1
best_document = None

for document in documents:
    score = cosine_similarity(query_embedding, document["embedding"])

    print(f'{score:.4f} - {document["filename"]}')

    if score > best_score:
        best_score = score
        best_document = document

print("\nBest document:")
print(best_document["filename"])
print(best_document["content"])

response = client.responses.create(
    model="gpt-5",
    input=f"""
Answer the question using only the information below.

Information:
{best_document["content"]}

Question:
{query}
"""
)

print("\nLLM Answer:")
print(response.output_text)