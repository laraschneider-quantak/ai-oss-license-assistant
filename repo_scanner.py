import os
import json

# Repository folder to scan
folder = "test_repo"

print("Scanning repository...\n")


# Detect the license type based on license text
def detect_license(text):

    text = text.lower()

    if "mit license" in text:
        return "MIT"

    if "gnu general public license" in text:
        return "GPL"

    if "apache license" in text:
        return "Apache"

    if "mozilla public license" in text:
        return "MPL"

    return "Unknown"


# Map licenses to compliance risk levels
def get_risk_level(license_name):

    risk_map = {
        "MIT": "Low Risk",
        "Apache": "Low Risk",
        "BSD": "Low Risk",
        "MPL": "Medium Risk",
        "LGPL": "Medium Risk",
        "GPL": "High Risk",
        "AGPL": "Very High Risk"
    }

    return risk_map.get(
        license_name,
        "Unknown Risk"
    )


# Map licenses to SPDX identifiers
def get_spdx_id(license_name):

    spdx_map = {
        "MIT": "MIT",
        "Apache": "Apache-2.0",
        "BSD": "BSD-3-Clause",
        "MPL": "MPL-2.0",
        "LGPL": "LGPL-2.1-only",
        "GPL": "GPL-3.0-only",
        "AGPL": "AGPL-3.0-only"
    }

    return spdx_map.get(
        license_name,
        "UNKNOWN"
    )


# Store scan results
scan_results = []


# Risk scoring used to calculate overall repository risk
risk_scores = {
    "Unknown Risk": 0,
    "Low Risk": 1,
    "Medium Risk": 2,
    "High Risk": 3,
    "Very High Risk": 4
}


# Walk through all folders and files
for root, dirs, files in os.walk(folder):

    # Skip folders that are not relevant
    dirs[:] = [
        d for d in dirs
        if d not in [
            "venv",
            "__pycache__",
            ".git",
            "chroma_db"
        ]
    ]

    # Process all files in the current folder
    for file in files:

        # Look for common license filenames
        if file.lower() in [
            "license",
            "license.txt",
            "license.md",
            "copying",
            "copying.txt"
        ]:

            filepath = os.path.join(root, file)

            # Read license file content
            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as license_file:

                content = license_file.read()

            # Detect license information
            license_name = detect_license(content)
            spdx_id = get_spdx_id(license_name)
            risk_level = get_risk_level(license_name)

            # Store scan result
            scan_results.append(
                {
                    "file": filepath,
                    "detected_license": license_name,
                    "spdx_id": spdx_id,
                    "license_expression": spdx_id,
                    "risk": risk_level
                }
            )


# Print detailed repository report
print("--- Repository Compliance Report ---\n")

for result in scan_results:

    print(f'File: {result["file"]}')
    print(f'Detected License: {result["detected_license"]}')
    print(f'SPDX ID: {result["spdx_id"]}')
    print(f'Risk Level: {result["risk"]}')
    print("-" * 40)


# Print repository summary
print("\n--- Summary ---")
print(f"Files scanned: {len(scan_results)}")


# Calculate highest repository risk
highest_risk = "Unknown Risk"

for result in scan_results:

    print(
        f'{result["file"]}: '
        f'{result["detected_license"]} '
        f'-> {result["risk"]}'
    )

    if risk_scores[result["risk"]] > risk_scores[highest_risk]:
        highest_risk = result["risk"]

print(f"Highest Risk: {highest_risk}")


# Build JSON compliance report
report = {
    "files_scanned": len(scan_results),
    "highest_risk": highest_risk,
    "results": scan_results
}


# Save report to disk
with open(
    "compliance_report.json",
    "w",
    encoding="utf-8"
) as report_file:

    json.dump(
        report,
        report_file,
        indent=4
    )

print(f"Overall Repository Risk: {highest_risk}")

print("\nJSON report saved: compliance_report.json")