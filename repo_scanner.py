import os

folder = "test_repo"
print("Folder:", folder)
print("Exists:", os.path.exists(folder))

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

    return risk_map.get(
        license_name,
        "Unknown Risk"
    )

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

            print(f"Found license file: {filepath}")

with open(filepath, "r", encoding="utf-8") as license_file:
    content = license_file.read()

    license_name = detect_license(content)

    risk_level = get_risk_level(
    license_name
    )

print(
    f"Risk Level: {risk_level}"
)

print(f"\nDetected License: {license_name}")

print("\nContent preview:")
print(content[:300])