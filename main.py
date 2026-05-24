licenses = [
    "MIT License",
    "Apache License 2.0",
    "GPL v3"
]

for license_name in licenses:
    if "GPL" in license_name:
        print(f"RISIKO: {license_name}")
    else:
        print(f"OK: {license_name}")