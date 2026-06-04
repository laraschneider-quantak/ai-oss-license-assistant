import os
import chromadb
from openai import OpenAI

client = OpenAI(
    api_key="sk-proj-XYZ"
)

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="license_knowledge"
)

folder = "knowledge"

documents = []
ids = []

for filename in os.listdir(folder):
    filepath = os.path.join(folder, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    documents.append(content)
    ids.append(filename)

collection.add(
    documents=documents,
    ids=ids
)

query = "Which license requires source code disclosure?"

results = collection.query(
    query_texts=[query],
    n_results=1
)

best_document = results["documents"][0][0]
best_id = results["ids"][0][0]

print("Best document:")
print(best_id)
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