from security_filter import (
    contains_secret,
    sanitize_scan_results
)


def test_contains_secret_detects_openai_key():
    assert contains_secret(
        "sk-123456789abcdef"
    )


def test_contains_secret_returns_false():
    assert not contains_secret(
        "MIT License"
    )


def test_sanitize_scan_results():
    scan_results = [
        {
            "File": r"C:\Projects\SecretProject\main.py",
            "License": "MIT",
            "SPDX": "MIT",
            "Risk": "Low",
            "Policy Decision": "Approved"
        }
    ]

    sanitized = sanitize_scan_results(
        scan_results
    )

    assert sanitized[0]["file"] == "file_001"
    assert sanitized[0]["license"] == "MIT"
    assert sanitized[0]["risk"] == "Low"