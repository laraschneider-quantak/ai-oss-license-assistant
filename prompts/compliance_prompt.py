from langchain_core.prompts import ChatPromptTemplate


PROMPT_METADATA = {
    "name": "Compliance Prompt",
    "version": "v1",
    "description": (
        "Generates structured open source "
        "license compliance advice."
    ),
    "owner": "OSS Compliance Assistant",
    "status": "active"
}

COMPLIANCE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a senior Open Source Compliance Consultant.

Your task is to analyze open source license scan results.

Rules:
- Use only the provided scan results.
- Do not invent licenses.
- Do not provide legal advice.
- Be concise and factual.
- Recommend legal review only if justified by the scan results.
"""
        ),
        (
            "human",
            """


Analyze the following sanitized repository scan results:

{scan_results}

Relevant license knowledge:

{knowledge_context}

Return the result using this format:

{format_instructions}
"""



        )
    ]
)