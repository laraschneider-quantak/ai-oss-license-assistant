import os
import chromadb
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

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

st.title("OSS Compliance Assistant")

query = st.text_input(
    "Ask a compliance question:"
)

if st.button("Ask"):

    detected_license_file = detect_license(query)

    if detected_license_file:
        results = collection.get(
            ids=[detected_license_file]
        )

        documents_for_gpt = "\n\n".join(
            results["documents"]
        )

    else:
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

Information:
{documents_for_gpt}

Question:
{query}
"""
    )

    st.subheader("Answer")
    st.write(response.output_text)