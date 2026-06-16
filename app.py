import os
import subprocess
import chromadb
import streamlit as st
import pandas as pd
import json
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


# Convert detected licenses to SPDX identifiers
def get_spdx_id(license_name):

    spdx_map = {
        "MIT": "MIT",
        "Apache": "Apache-2.0",
        "BSD": "BSD-3-Clause",
        "MPL": "MPL-2.0",
        "LGPL": "LGPL-2.1-only",
        "GPL": "GPL-3.0-only",
        "AGPL": "AGPL-3.0-only",
        "EPL": "EPL-2.0",
        "CDDL": "CDDL-1.0"
    }

    return spdx_map.get(
        license_name,
        "UNKNOWN"
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

if "scan_results" not in st.session_state:
    st.session_state.scan_results = []

if "highest_risk" not in st.session_state:
    st.session_state.highest_risk = "Unknown Risk"

if "repo_name" not in st.session_state:
    st.session_state.repo_name = ""

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

github_url = st.text_input(
    "GitHub repository URL:",
    value="https://github.com/psf/requests.git"
)

repo_name = github_url.rstrip("/").split("/")[-1].replace(".git", "")

clone_path = os.path.join(
    "external_repos",
    repo_name
)

if st.button("Clone Repository"):

    os.makedirs(
        "external_repos",
        exist_ok=True
    )

    if os.path.exists(clone_path):

        st.info(
            f"Repository already exists: {clone_path}"
        )

    else:

        with st.spinner("Cloning repository..."):

            subprocess.run(
                [
                    "git",
                    "clone",
                    github_url,
                    clone_path
                ],
                check=True
            )

        st.success(
            f"Repository cloned to: {clone_path}"
        )

# Repository path input
repo_path = clone_path

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

        if license_files:

            highest_risk = "Unknown Risk"

            risk_scores = {
                "Unknown Risk": 0,
                "Low Risk": 1,
                "Medium Risk": 2,
                "High Risk": 3,
                "Very High Risk": 4
            }

            scan_results = []

            # Read each license file and detect license, SPDX ID and risk
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

                spdx_id = get_spdx_id(
                    detected_license
                )

                scan_results.append(
                    {
                        "File": filepath,
                        "License": detected_license,
                        "SPDX": spdx_id,
                        "Risk": risk_level
                    }
                )

                if risk_scores[risk_level] > risk_scores[highest_risk]:
                    highest_risk = risk_level

            # Store scan results so they survive Streamlit reruns
            st.session_state.scan_results = scan_results
            st.session_state.highest_risk = highest_risk
            st.session_state.repo_name = repo_name

        else:

            st.warning("No license files found.")

    else:

        st.error(
            f"Repository not found: {repo_path}"
        )


# Display latest scan results
if st.session_state.scan_results:

    st.subheader("License Scan Results")

    df = pd.DataFrame(
        st.session_state.scan_results
    )

    st.table(df)

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name="compliance_report.csv",
        mime="text/csv",
        key="csv_download"
    )

    spdx_report = {
        "spdxVersion": "SPDX-2.3",
        "name": st.session_state.repo_name,
        "documentNamespace":
            f"https://example.com/spdx/{st.session_state.repo_name}",
        "packages": []
    }

    for result in st.session_state.scan_results:

        spdx_report["packages"].append(
            {
                "name": result["File"],
                "licenseConcluded": result["SPDX"]
            }
        )

    spdx_json = json.dumps(
        spdx_report,
        indent=4
    )

    st.download_button(
        label="Download SPDX Report",
        data=spdx_json,
        file_name="spdx_report.json",
        mime="application/json",
        key="spdx_download"
    )

    st.metric(
        "License Files",
        len(st.session_state.scan_results)
    )

    highest_risk = st.session_state.highest_risk

    if highest_risk == "Very High Risk":
        st.error("Overall Repository Risk: Very High Risk")

    elif highest_risk == "High Risk":
        st.warning("Overall Repository Risk: High Risk")

    elif highest_risk == "Medium Risk":
        st.info("Overall Repository Risk: Medium Risk")

    elif highest_risk == "Low Risk":
        st.success("Overall Repository Risk: Low Risk")

    else:
        st.warning("Overall Repository Risk: Unknown Risk")
        