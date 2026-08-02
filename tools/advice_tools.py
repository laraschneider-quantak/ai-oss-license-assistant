from langchain.tools import tool

from ai_advisor import generate_compliance_advice
from schemas.ai_advice_schema import AIComplianceAdvice


@tool
def generate_ai_advice_tool(
    scan_results: list[dict],
) -> AIComplianceAdvice:
    """
    Generate structured OSS compliance advice from repository scan results.

    Use this tool when the user asks for a compliance assessment,
    risk explanation, recommended actions, or legal-review guidance
    based on repository scan results.
    """

    print(">>> generate_ai_advice_tool called")

    return generate_compliance_advice(
        scan_results
    )