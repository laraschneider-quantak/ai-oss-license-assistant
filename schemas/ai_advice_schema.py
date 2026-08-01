from typing import List

from pydantic import BaseModel


class AIComplianceAdvice(BaseModel):
    """
    Structured AI compliance advice.
    """

    executive_summary: str
    detected_licenses: List[str]
    risk_assessment: str
    compliance_actions: List[str]
    legal_review_recommended: bool
    disclaimer: str