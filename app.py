import os
import chromadb
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Open persistent ChromaDB database
chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

# Open or create the knowledge collection
collection = chroma_client.get_or_create_collection(
    name="oss_compliance_knowledge"
)


# Detect direct license mentions in user questions
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


# Detect license type from repository license text
def detect_repository_license(text):
    text = text.lower()

    if "affero general public license" in text:
        return "AGPL"

    if "lesser general public license" in text:
        return "LGPL"

    if "gnu general public license" in text:
        return "GPL"

    if "apache license" in text:
        return "Apache"

    if "mit license" in text:
        return "MIT"

    if (
        "redistribution and use in source and binary forms" in text
        and "neither the name of the copyright holder" in text
    ):
        return "BSD"

    if "mozilla public license" in text:
        return "MPL"

    if "eclipse public license" in text:
        return "EPL"

    if "common development and distribution license" in text:
        return "CDDL"

    return "Unknown"


# Map detected licenses to compliance risk levels
def get_risk_level(license_name):
    risk_map = {
        "MIT": "Low Risk",
        "Apache": "Low Risk",
        "BSD": "Low Risk",
        "MPL": "Medium Risk",
        "EPL": "Medium Risk",
        "CDDL": "Medium Risk",
        "LGPL": "Medium Risk",
        "GPL": "High Risk",
        "AGPL": "Very High Risk"
    }

    return risk_map.get(
        license_name,
        "Unknown Risk"
    )


# Page title
st.title("OSS Compliance Assistant")

# Clear chat history
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input field
query = st.chat_input(
    "Ask a compliance question"
)

# Process chat query
if query:
    detected_license_file = detect_license(query)

    # If a specific license is mentioned, retrieve the exact document
    if detected_license_file:
        results = collection.get(
            ids=[detected_license_file]
        )

        documents_for_gpt = "\n\n".join(
            results["documents"]
        )

        sources = [detected_license_file]

    # Otherwise use semantic search
    else:
        results = collection.query(
            query_texts=[query],
            n_results=5
        )

        documents_for_gpt = "\n\n".join(
            results["documents"][0]
        )

        sources = results["ids"][0]

    # Ask GPT using the retrieved context
    with st.spinner("Thinking..."):
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

    # Store question, answer and sources in chat history
    st.session_state.messages.append(
        {
            "question": query,
            "answer": response.output_text,
            "sources": sources
        }
    )


# Display chat history
for message in st.session_state.messages:
    with st.chat_message("user"):
        st.write(message["question"])

    with st.chat_message("assistant"):
        st.write(message["answer"])
        st.caption(
            "Sources: " + ", ".join(message["sources"])
        )


st.divider()

st.header("Repository Compliance Scanner")

# Repository path input
repo_path = st.text_input(
    "Repository path:",
    value="test_repo"
)

# Scan repository button
if st.button("Scan Repository"):
    if os.path.exists(repo_path):
        st.success(
            f"Repository found: {repo_path}"
        )

        license_files = []

        # Walk through repository folders
        for root, dirs, files in os.walk(repo_path):

            # Skip folders that should not be scanned
            dirs[:] = [
                d for d in dirs
                if d not in [
                    ".git",
                    "__pycache__",
                    "venv",
                    "chroma_db"
                ]
            ]

            # Find common license file names
            for file in files:
                if file.lower() in [
                    "license",
                    "license.txt",
                    "license.md",
                    "copying",
                    "copying.txt"
                ]:
                    filepath = os.path.join(
                        root,
                        file
                    )

                    license_files.append(
                        filepath
                    )

        st.subheader("License Files Found")

        if license_files:
            highest_risk = "Unknown Risk"

            risk_scores = {
                "Unknown Risk": 0,
                "Low Risk": 1,
                "Medium Risk": 2,
                "High Risk": 3,
                "Very High Risk": 4
            }

            # Read each license file and detect license + risk
            for filepath in license_files:
                with open(
                    filepath,
                    "r",
                    encoding="utf-8"
                ) as license_file:
                    content = license_file.read()

                detected_license = detect_repository_license(
                    content
                )

                risk_level = get_risk_level(
                    detected_license
                )

                if risk_scores[risk_level] > risk_scores[highest_risk]:
                    highest_risk = risk_level

                st.write(
                    f"{filepath} → {detected_license} → {risk_level}"
                )

            st.subheader("Repository Summary")

            st.write(
                f"Overall Repository Risk: {highest_risk}"
            )

        else:
            st.warning("No license files found.")

    else:
        st.error(
            f"Repository not found: {repo_path}"
        )