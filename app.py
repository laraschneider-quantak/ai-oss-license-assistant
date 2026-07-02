import os
import subprocess
import chromadb
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from pdf_report import generate_pdf_report
from scanner import scan_repository
from spdx_export import generate_spdx_report
from ai_advisor import generate_ai_compliance_advice
from dashboard import (
    calculate_compliance_score,
    calculate_overall_policy,
    calculate_risk_summary,
    calculate_policy_summary,
    calculate_dashboard_metrics
)

from config import (
    OPENAI_API_KEY,
    CHROMA_DB_PATH,
    EXTERNAL_REPOS_PATH,
    PDF_REPORT_NAME,
    SPDX_REPORT_NAME
)

from config import AI_BACKEND

from logger import logger

load_dotenv()


client = OpenAI(
    api_key=OPENAI_API_KEY
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
    EXTERNAL_REPOS_PATH,
    repo_name
)

if st.button("Clone & Scan Repository"):

    os.makedirs(
        EXTERNAL_REPOS_PATH,
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

        logger.info(
            f"Repository cloned: {repo_name}"
        )

    scan_repository(
        repo_path=clone_path,
        repo_name=repo_name
    )


if st.session_state.scan_results:

    st.header("Compliance Dashboard")

    st.caption(
        "Repository compliance overview and governance metrics"
    )


    (
        license_count,
        unique_licenses,
        high_risk_count,
        approved_count
    ) = calculate_dashboard_metrics(
        st.session_state.scan_results
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

    compliance_score = calculate_compliance_score(
        st.session_state.scan_results
    )

    st.metric(
        "Compliance Score",
        f"{compliance_score}%"
    )

    risk_summary = calculate_risk_summary(
        st.session_state.scan_results
    )

    policy_summary = calculate_policy_summary(
        st.session_state.scan_results
    )

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:
        st.subheader("Risk Summary")

        risk_df = pd.DataFrame(
            list(risk_summary.items()),
            columns=[
                "Risk Level",
                "Count"
            ]
        )

        st.dataframe(
            risk_df,
            use_container_width=True
        )

    with summary_col2:
        st.subheader("Policy Summary")

        policy_df = pd.DataFrame(
            list(policy_summary.items()),
            columns=[
                "Policy Decision",
                "Count"
            ]
        )

        st.dataframe(
            policy_df,
            use_container_width=True
        )

    overall_policy = calculate_overall_policy(
        st.session_state.scan_results
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

    spdx_json = generate_spdx_report(
        repo_name=st.session_state.repo_name,
        scan_results=st.session_state.scan_results
    )

    st.download_button(
        label="Download SPDX Report",
        data=spdx_json,
        file_name=SPDX_REPORT_NAME,
        mime="application/json",
        key="spdx_download"
    )

    pdf_path = PDF_REPORT_NAME

    generate_pdf_report(
        report_path=pdf_path,
        repo_name=st.session_state.repo_name,
        compliance_score=compliance_score,
        overall_policy=overall_policy,
        overall_risk=st.session_state.highest_risk,
        ai_advice=st.session_state.ai_advice
    )

    with open(
        pdf_path,
        "rb"
    ) as pdf_file:

        st.download_button(
            label="Download PDF Report",
            data=pdf_file,
            file_name=PDF_REPORT_NAME,
            mime="application/pdf"
        )

    if st.button("Generate AI Compliance Advice"):

        try:
            with st.spinner(
                "Generating AI compliance advice..."
            ):
                logger.info(
                    "Generating AI compliance advice"
                )
                
                st.session_state.ai_advice = (
                    generate_ai_compliance_advice(
                        client=client,
                        scan_results=st.session_state.scan_results
                    )
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