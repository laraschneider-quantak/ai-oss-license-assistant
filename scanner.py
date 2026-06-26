import os
import streamlit as st

from policy_engine import (
    get_risk_level,
    get_spdx_id,
    get_policy_decision
)


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
