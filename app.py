import os
import subprocess
import chromadb
import streamlit as st
import pandas as pd
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

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


def get_policy_decision(license_name):
    policy_map = {
        "MIT": "Approved",
        "Apache": "Approved",
        "BSD": "Approved",
        "MPL": "Review Required",
        "EPL": "Review Required",
        "CDDL": "Review Required",
        "LGPL": "Review Required",
        "GPL": "Legal Review Required",
        "AGPL": "Blocked / High Review",
        "Unknown": "Manual Review"
    }

    return policy_map.get(
        license_name,
        "Manual Review"
    )


def scan_repository(repo_path, repo_name):
    if not os.path.exists(repo_path):
        st.error(
            f"Repository not found: {repo_path}"
        )
        return

    st.success(
        f"Repository found: {repo_path}"
    )

    license_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d for d in dirs
            if d not in [
                ".git",
                "__pycache__",
                "venv",
                "chroma_db"
            ]
        ]

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

    if not license_files:
        st.warning("No license files found.")
        return

    highest_risk = "Unknown Risk"

    risk_scores = {
        "Unknown Risk": 0,
        "Low Risk": 1,
        "Medium Risk": 2,
        "High Risk": 3,
        "Very High Risk": 4
    }

    scan_results = []

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

        policy_decision = get_policy_decision(
            detected_license
        )

        scan_results.append(
            {
                "File": filepath,
                "License": detected_license,
                "SPDX": spdx_id,
                "Risk": risk_level,
                "Policy Decision": policy_decision
            }
        )

        if risk_scores[risk_level] > risk_scores[highest_risk]:
            highest_risk = risk_level

    st.session_state.scan_results = scan_results
    st.session_state.highest_risk = highest_risk
    st.session_state.repo_name = repo_name
    st.session_state.ai_advice = ""


st.title("OSS Compliance Assistant")

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "scan_results" not in st.session_state:
    st.session_state.scan_results = []

if "highest_risk" not in st.session_state:
    st.session_state.highest_risk = "Unknown Risk"

if "repo_name" not in st.session_state:
    st.session_state.repo_name = ""

if "ai_advice" not in st.session_state:
    st.session_state.ai_advice = ""

query = st.chat_input(
    "Ask a compliance question"
)

if query:
    detected_license_file = detect_license(query)

    if detected_license_file:
        results = collection.get(
            ids=[detected_license_file]
        )

        documents_for_gpt = "\n\n".join(
            results["documents"]
        )

        sources = [detected_license_file]

    else:
        results = collection.query(
            query_texts=[query],
            n_results=5
        )

        documents_for_gpt = "\n\n".join(
            results["documents"][0]
        )

        sources = results["ids"][0]

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

    st.session_state.messages.append(
        {
            "question": query,
            "answer": response.output_text,
            "sources": sources
        }
    )


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

if st.button("Clone & Scan Repository"):
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

    scan_repository(
        repo_path=clone_path,
        repo_name=repo_name
    )


if st.session_state.scan_results:

    license_count = len(
        st.session_state.scan_results
    )

    unique_licenses = len(
        set(
            result["License"]
            for result in st.session_state.scan_results
        )
    )

    high_risk_count = sum(
        1
        for result in st.session_state.scan_results
        if result["Risk"] in [
            "High Risk",
            "Very High Risk"
        ]
    )

    approved_count = sum(
        1
        for result in st.session_state.scan_results
        if result["Policy Decision"]
        == "Approved"
    )


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "License Files",
        license_count
    )

    col2.metric(
        "Unique Licenses",
        unique_licenses
    )

    col3.metric(
        "High Risk Licenses",
        high_risk_count
    )

    col4.metric(
        "Approved Licenses",
        approved_count
    )

    compliance_score = 100

    compliance_score -= high_risk_count * 25

    review_count = sum(
        1
        for result in st.session_state.scan_results
        if result["Policy Decision"] in [
            "Review Required",
            "Manual Review"
        ]
    )

    compliance_score -= review_count * 10

    if compliance_score < 0:
        compliance_score = 0

    st.metric(
        "Compliance Score",
        f"{compliance_score}%"
    )


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

    st.metric(
        "License Files",
        len(st.session_state.scan_results)
    )

    policy_priority = {
        "Approved": 1,
        "Review Required": 2,
        "Manual Review": 3,
        "Legal Review Required": 4,
        "Blocked / High Review": 5
    }

    overall_policy = "Approved"

    for result in st.session_state.scan_results:
        current_policy = result[
            "Policy Decision"
        ]

        if (
            policy_priority[current_policy]
            >
            policy_priority[overall_policy]
        ):
            overall_policy = current_policy

    if overall_policy == "Approved":
        st.success(
            f"Overall Policy Status: {overall_policy}"
        )

    elif overall_policy == "Review Required":
        st.info(
            f"Overall Policy Status: {overall_policy}"
        )

    elif overall_policy == "Manual Review":
        st.warning(
            f"Overall Policy Status: {overall_policy}"
        )

    elif overall_policy == "Legal Review Required":
        st.error(
            f"Overall Policy Status: {overall_policy}"
        )

    elif overall_policy == "Blocked / High Review":
        st.error(
            f"Overall Policy Status: {overall_policy}"
        )

    spdx_report = {
        "spdxVersion": "SPDX-2.3",
        "SPDXID": "SPDXRef-DOCUMENT",
        "dataLicense": "CC0-1.0",
        "name": st.session_state.repo_name,
        "documentNamespace":
            f"https://example.com/spdx/{st.session_state.repo_name}",

        "creationInfo": {
            "created": datetime.now().isoformat(),
            "creators": [
                "Tool: OSS Compliance Assistant"
            ]
        },

        "packages": []
    }

    for index, result in enumerate(
        st.session_state.scan_results,
        start=1
    ):
        spdx_report["packages"].append(
            {
                "SPDXID": f"SPDXRef-Package-{index}",
                "name": result["File"],
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": False,
                "licenseConcluded": result["SPDX"],
                "licenseDeclared": result["SPDX"],
                "copyrightText": "NOASSERTION"
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

    if st.button("Generate AI Compliance Advice"):
        licenses_for_ai = []

        for result in st.session_state.scan_results:
            licenses_for_ai.append(
                {
                    "file": result["File"],
                    "license": result["License"],
                    "spdx": result["SPDX"],
                    "risk": result["Risk"],
                    "policy": result["Policy Decision"]
                }
            )

        try:
            with st.spinner(
                "Generating AI compliance advice..."
            ):
                response = client.responses.create(
                    model="gpt-5",
                    input=f"""
You are a senior Open Source Compliance Consultant.

Analyze the repository scan results and provide:

1. Executive Summary
2. Detected Licenses
3. Risk Assessment
4. Compliance Actions
5. Legal Review Recommendation

Maximum 300 words.
Be concise and practical.

Important:
- This is not legal advice.
- Do not invent licenses.
- Base your answer only on the scan results.

Scan results:
{licenses_for_ai}
"""
                )

            st.session_state.ai_advice = (
                response.output_text
            )

        except Exception as error:
            st.error(
                f"AI Compliance Advisor failed: {error}"
            )

    if st.session_state.ai_advice:
        st.subheader("AI Compliance Advice")

        st.markdown(
            st.session_state.ai_advice
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