import os
import chromadb
from openai import OpenAI

client = OpenAI(
    api_key="sk-projXYZ"
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

query = input("Ask a compliance question: ")

results = collection.query(
    query_texts=[query],
    n_results=3
)
documents_for_gpt = "\n\n".join(
    results["documents"][0]
)

print("\nQuestion:")
print(query)

print("\nTop 3 Documents:")
print(results["ids"][0])

print("\nDistances:")
print(results["distances"][0])

#print("\nDocuments sent to GPT:")
#print(documents_for_gpt)

response = client.responses.create(
    model="gpt-5",
    input=f"""
Answer the question using only the information below.

Information:
{documents_for_gpt}

Question:
{query}
"""
)

print("\nLLM Answer:")
print(response.output_text)