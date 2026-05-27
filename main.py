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


def scan_licenses(file_path):
    df = pd.read_csv(file_path)

    ok_count = 0
    risk_count = 0
    check_count = 0
    unknown_count = 0

    print("\n--- LICENSE SCAN REPORT ---\n")

    for index, row in df.iterrows():
        software = row["software"]
        license_name = row["license"]

        result = classify_license(license_name)

        print(f"{software}: {license_name} -> {result}")

        if result == "OK":
            ok_count += 1

        elif result == "RISK":
            risk_count += 1

        elif result == "CHECK":
            check_count += 1

        else:
            unknown_count += 1
    print("\n--- SUMMARY ---\n")

    print(f"OK: {ok_count}")
    print(f"RISK: {risk_count}")
    print(f"CHECK: {check_count}")
    print(f"UNKNOWN: {unknown_count}")


scan_licenses("licenses.csv")