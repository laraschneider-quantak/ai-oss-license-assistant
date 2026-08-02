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


def scan_repository(
    repo_path,
    repo_name,
):
    if not os.path.exists(repo_path):
        return {
            "success": False,
            "message": f"Repository not found: {repo_path}",
            "scan_results": [],
            "highest_risk": "Unknown Risk",
            "highest_policy": "Manual Review",
            "repo_name": repo_name,
        }

    license_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in [
                ".git",
                "__pycache__",
                "venv",
                "chroma_db",
            ]
        ]

        for file in files:
            if file.lower() in [
                "license",
                "license.txt",
                "license.md",
                "copying",
                "copying.txt",
            ]:
                filepath = os.path.join(
                    root,
                    file,
                )

                license_files.append(
                    filepath
                )

    if not license_files:
        return {
            "success": False,
            "message": "No license files found.",
            "scan_results": [],
            "highest_risk": "Unknown Risk",
            "highest_policy": "Manual Review",
            "repo_name": repo_name,
        }

    highest_risk = "Unknown Risk"
    highest_policy = "Approved"

    risk_scores = {
        "Unknown Risk": 0,
        "Low Risk": 1,
        "Medium Risk": 2,
        "High Risk": 3,
        "Very High Risk": 4,
    }

    policy_scores = {
        "Approved": 0,
        "Review Required": 1,
        "Manual Review": 2,
        "Legal Review Required": 3,
        "Blocked / High Review": 4,
    }

    scan_results = []

    for filepath in license_files:
        with open(
            filepath,
            "r",
            encoding="utf-8",
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
                "Policy Decision": policy_decision,
            }
        )

        if (
            risk_scores[risk_level]
            > risk_scores[highest_risk]
        ):
            highest_risk = risk_level

        if (
            policy_scores[policy_decision]
            > policy_scores[highest_policy]
        ):
            highest_policy = policy_decision

    return {
        "success": True,
        "message": "Repository scanned successfully.",
        "scan_results": scan_results,
        "highest_risk": highest_risk,
        "highest_policy": highest_policy,
        "repo_name": repo_name,
    }