import pandas as pd


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


df = pd.read_csv("licenses.csv")

print(df)

print("\n--- LICENSE REPORT ---\n")

for index, row in df.iterrows():

    software = row["software"]
    license_name = row["license"]

    result = classify_license(license_name)

    print(f"{software}: {license_name} -> {result}")