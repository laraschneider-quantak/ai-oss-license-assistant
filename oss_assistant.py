import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="oss_compliance_knowledge"
)


def detect_license(query):
    query_lower = query.lower()

    license_map = {
        "mit": "mit.txt",
        "bsd": "bsd.txt",
        "apache": "apache.txt",
        "gplv2": "gplv2.txt",
        "gpl v2": "gplv2.txt",
        "gplv3": "gplv3.txt",
        "gpl v3": "gplv3.txt",
        "lgpl": "lgpl.txt",
        "agpl": "agpl.txt",
        "mpl": "mpl.txt"
    }

    for license_name, filename in license_map.items():
        if license_name in query_lower:
            return filename

    return None


print("OSS Compliance Assistant started.")
print("Type 'exit' to stop.\n")

while True:
    query = input("Ask a compliance question: ")

    if query.lower() == "exit":
        print("Assistant stopped.")
        break

    detected_license_file = detect_license(query)

    if detected_license_file:
        results = collection.get(
            ids=[detected_license_file]
        )

        documents_for_gpt = "\n\n".join(
            results["documents"]
        )

        print(f"\nDetected license file: {detected_license_file}")

    else:
        results = collection.query(
            query_texts=[query],
            n_results=5
        )

        documents_for_gpt = "\n\n".join(
            results["documents"][0]
        )

        print("\nTop documents:")
        print(results["ids"][0])

    response = client.responses.create(
        model="gpt-5",
        input=f"""
You are an OSS compliance assistant.

Use only the information below.

Task:
1. Answer the user's compliance question.
2. If multiple licenses are mentioned, compare their stated risk level.
3. If one license is described as "very high risk", choose that over "high risk".
4. If the information is not sufficient, say that the knowledge base does not contain enough information.

Information:
{documents_for_gpt}

Question:
{query}
"""
    )

    print("\nAnswer:")
    print(response.output_text)
    print("\n" + "-" * 50 + "\n")