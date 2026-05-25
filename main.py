licenses = [
    "MIT",
    "Apache 2.0",
    "GPL v3",
    "LGPL",
    "BSD",
    "AGPL"
]

def classify_license(license_name):
    if license_name == "AGPL":
        return "RISK"

    elif "LGPL" in license_name:
        return "CHECK"

    elif "GPL" in license_name:
        return "RISK"

    elif license_name in ["MIT", "BSD", "Apache 2.0"]:
        return "OK"

    else:
        return "UNKNOWN"


for license_name in licenses:
    result = classify_license(license_name)
    print(f"{result}: {license_name}")