import os
import json

folder = "test_repo"

print("Scanning repository...\n")


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

    return risk_map.get(license_name, "Unknown Risk")


scan_results = []

risk_scores = {
    "Unknown Risk": 0,
    "Low Risk": 1,
    "Medium Risk": 2,
    "High Risk": 3,
    "Very High Risk": 4
}


for root, dirs, files in os.walk(folder):

    dirs[:] = [
        d for d in dirs
        if d not in [
            "venv",
            "__pycache__",
            ".git",
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
            filepath = os.path.join(root, file)

            with open(filepath, "r", encoding="utf-8") as license_file:
                content = license_file.read()

            license_name = detect_license(content)
            risk_level = get_risk_level(license_name)

            scan_results.append(
                {
                    "file": filepath,
                     "detected_license": license_name,
                     "spdx_id": license_name,        
                     "license_expression": license_name,
                     "risk": risk_level
                }
            )


print("--- Repository Compliance Report ---\n")

for result in scan_results:
    print(f'File: {result["file"]}')
    print(f'Detected License: {result["detected_license"]}')
    print(f'Risk Level: {result["risk"]}')
    print("-" * 40)

print("\n--- Summary ---")
print(f"Files scanned: {len(scan_results)}")

highest_risk = "Unknown Risk"

for result in scan_results:
    if risk_scores[result["risk"]] > risk_scores[highest_risk]:
        highest_risk = result["risk"]

print(f"Highest Risk: {highest_risk}")
report = {
    "files_scanned": len(scan_results),
    "highest_risk": highest_risk,
    "results": scan_results
}

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

print(
    "\nJSON report saved: compliance_report.json"
)

print(f'{result["file"]}: {result["detected_license"]} -> {result["risk"]}')