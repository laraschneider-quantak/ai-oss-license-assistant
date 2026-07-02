import re
from logger import logger


SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9_\-]+",
    r"api[_-]?key\s*=\s*[A-Za-z0-9_\-]+",
    r"token\s*=\s*[A-Za-z0-9_\-]+",
]


def contains_secret(value):
    """
    Check whether a value contains a potential secret.
    """

    if value is None:
        return False

    text = str(value)

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def sanitize_scan_results(scan_results):
    """
    Remove sensitive information before sending scan results to an AI backend.
    """

    sanitized_results = []

    for index, result in enumerate(scan_results, start=1):
        sanitized_result = {
            "file": f"file_{index:03d}",
            "license": result.get("License", "Unknown"),
            "spdx": result.get("SPDX", "Unknown"),
            "risk": result.get("Risk", "Unknown"),
            "policy": result.get("Policy Decision", "Unknown")
        }

        if any(
            contains_secret(value)
            for value in result.values()
        ):
            
            logger.warning(
                "Potential secret detected in scan result %s and removed before AI processing.",
                index
            )
            
            sanitized_result["security_warning"] = (
                "Potential secret detected and removed before AI processing."
            )

        sanitized_results.append(sanitized_result)

    return sanitized_results