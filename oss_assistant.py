import os
import chromadb
from openai import OpenAI

client = OpenAI(
    api_key="sk-proj-XYZ"
)

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="oss_compliance_knowledge"
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

print("OSS Compliance Assistant started.")
print("Type 'exit' to stop.\n")

while True:
    query = input("Ask a compliance question: ")

    if query.lower() == "exit":
        print("Assistant stopped.")
        break

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    documents_for_gpt = "\n\n".join(
        results["documents"][0]
    )

    response = client.responses.create(
        model="gpt-5",
        input=f"""
You are an OSS compliance assistant.

Use only the information below.

Task:
1. Identify all licenses mentioned in the information.
2. Compare their stated risk level.
3. If one license is described as "very high risk", choose that over "high risk".
4. Answer with the single highest-risk license first, then give a short reason.



Information:
{documents_for_gpt}

Question:
{query}
"""
    )

    print("\nAnswer:")
    print(response.output_text)
    print("\n" + "-" * 50 + "\n")