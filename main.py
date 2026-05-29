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


df = pd.read_excel("licenses.xlsx")

print("\n--- EXCEL LICENSE REPORT ---\n")

risk_count = 0
risk_percent = 0

for index, row in df.iterrows():

    software = row["software"]
    license_name = row["license"]

    result = classify_license(license_name)

    if result == "RISK":
     risk_count += 1
     print(f"{software}: {license_name} -> {result}")
 
    print(f"Total Risks: {risk_count}")
    risk_percent = (risk_count / len(df)) * 100
    print(f"Risk percent: {risk_percent}")