from logger import logger
from security_filter import sanitize_scan_results
from audit_logger import log_ai_request
from config import AI_BACKEND, AI_MODEL
from langchain_advisor import generate_langchain_compliance_advice
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY
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


def generate_compliance_advice(scan_results):

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
        "files_processed": len(sanitized_results),
        "secrets_detected": secrets_detected,
        "sanitized": True
    }

    log_ai_request(audit_data)

    """
    Select AI backend for compliance advice.
    """
 
    logger.info(
        "Using AI backend: %s",
        AI_BACKEND
    )

    if AI_BACKEND == "langchain":
        return generate_langchain_compliance_advice(
            scan_results
        )

    return generate_ai_compliance_advice(
        client,
        scan_results
    )