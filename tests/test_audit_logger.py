from audit_logger import log_ai_request


def test_log_ai_request_runs_without_error():
    audit_data = {
        "backend": "openai",
        "model": "gpt-5",
        "files_processed": 3,
        "secrets_detected": 1,
        "sanitized": True
    }

    log_ai_request(audit_data)