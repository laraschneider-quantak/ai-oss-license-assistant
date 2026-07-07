import os

import chromadb

from config import KNOWLEDGE_FOLDER

from knowledge_loader import load_knowledge_documents



chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="license_knowledge"
)


def load_knowledge_base():
    """
    Load knowledge documents into ChromaDB.
    """

    documents, ids = load_knowledge_documents()

    if documents:
        collection.add(
            documents=documents,
            ids=ids
        )

def build_license_query(scan_results):
    """
    Build a retrieval query from detected licenses.
    """

    licenses = set()

    for result in scan_results:
        license_name = result.get(
            "license"
        )

        if license_name:
            licenses.add(
                license_name
            )

    return " ".join(
        sorted(licenses)
    )


def retrieve_relevant_knowledge(query, n_results=3):
    """
    Retrieve relevant knowledge snippets for a query.
    """

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return "\n\n".join(
        results["documents"][0]
    )

