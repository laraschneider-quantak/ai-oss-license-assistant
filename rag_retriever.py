import os

import chromadb

from config import (
    KNOWLEDGE_FOLDER, 
    MAX_RAG_DOCUMENTS
    )

from knowledge_loader import load_knowledge_documents

from retrieval_policy import RETRIEVAL_POLICY


chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="license_knowledge"
)

def determine_retrieval_strategy(scan_results):
    """
    Determine which retrieval strategy to use.
    """

    unique_licenses = {
        result.get("license")
        for result in scan_results
        if result.get("license")
    }

    if not unique_licenses:
        return RETRIEVAL_POLICY["no_license"]

    if len(unique_licenses) == 1:
        return RETRIEVAL_POLICY["single_license"]

    return RETRIEVAL_POLICY["multiple_licenses"]


def retrieve_knowledge_for_scan(scan_results):
    """
    Retrieve knowledge using the configured retrieval strategy.
    """

    strategy = determine_retrieval_strategy(
        scan_results
    )

    if strategy == "none":
        return "", strategy

    license_query = build_license_query(
        scan_results
    )

    if strategy == "direct":
        knowledge_context = retrieve_relevant_knowledge(
            license_query,
            n_results=1
        )

        return knowledge_context, strategy

    unique_licenses = {
        result.get("license")
        for result in scan_results
        if result.get("license")
    }

    n_results = min(
        len(unique_licenses),
        MAX_RAG_DOCUMENTS
    )

    knowledge_context = retrieve_relevant_knowledge(
        license_query,
        n_results=n_results
    )

    return knowledge_context, strategy



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

