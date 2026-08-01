from logger import logger
from security_filter import sanitize_scan_results
from audit_logger import log_ai_request
from config import (
    AI_BACKEND,
    AI_MODEL,
    AI_PROMPT_VERSION,
    OPENAI_API_KEY
)
from langchain_advisor import (
    generate_langchain_compliance_advice
)
from openai import OpenAI

from schemas.ai_advice_schema import AIComplianceAdvice


client = OpenAI(
    api_key=OPENAI_API_KEY
)

def normalize_compliance_advice(
    advice
) -> AIComplianceAdvice:
    """
    Normalize AI output into an AIComplianceAdvice object.
    """

    if isinstance(advice, AIComplianceAdvice):
        return advice

    if isinstance(advice, str):
        return AIComplianceAdvice.model_validate_json(
            advice
        )

    if isinstance(advice, dict):
        return AIComplianceAdvice.model_validate(
            advice
        )

    raise TypeError(
        "Unsupported compliance advice type: "
        f"{type(advice).__name__}"
    )


def generate_ai_compliance_advice(
    client,
    scan_results
):
    logger.info(
        "Generating AI compliance advice"
    )

    response = client.responses.create(
        model=AI_MODEL,
        input=f"""
You are a senior Open Source Compliance Consultant.

Analyze the repository scan results and provide:

1. Executive Summary
2. Detected Licenses
3. Risk Assessment
4. Compliance Actions
5. Legal Review Recommendation

Maximum 300 words.
Be concise and practical.

Important:
- This is not legal advice.
- Do not invent licenses.
- Base your answer only on the scan results.

Scan results:
{scan_results}
"""
    )

    logger.info(
        "AI compliance advice generated successfully"
    )

    return response.output_text


def generate_compliance_advice(
    scan_results
):
    """
    Select AI backend for compliance advice.
    """

    print(
        "DISPATCHER CALLED | "
        f"AI_BACKEND={AI_BACKEND!r}"
    )

    sanitized_results = sanitize_scan_results(
        scan_results
    )

    secrets_detected = sum(
        1
        for result in sanitized_results
        if "security_warning" in result
    )

    audit_data = {
        "backend": AI_BACKEND,
        "model": AI_MODEL,
        "prompt_version": AI_PROMPT_VERSION,
        "files_processed": len(sanitized_results),
        "secrets_detected": secrets_detected,
        "sanitized": True
    }

    log_ai_request(
        audit_data
    )

    logger.info(
        "Using AI backend: %s",
        AI_BACKEND
    )

    print(
        f"CURRENT AI BACKEND: {AI_BACKEND!r}",
        flush=True
    )

    if AI_BACKEND == "langchain":

        print(
             "LANGCHAIN BRANCH SELECTED"
            )

        advice = generate_langchain_compliance_advice(
                sanitized_results
            )

    else:
        advice = generate_ai_compliance_advice(
            client,
            sanitized_results
        )

    normalized_advice = normalize_compliance_advice(
            advice
        )

    print(
            "NORMALIZED ADVICE TYPE:",
            type(normalized_advice).__name__
        )

    return normalized_advice