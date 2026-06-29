from logger import logger


def generate_ai_compliance_advice(
    client,
    scan_results
):
    logger.info(
        "Generating AI compliance advice"
    )

    licenses_for_ai = []

    for result in scan_results:
        licenses_for_ai.append(
            {
                "file": result["File"],
                "license": result["License"],
                "spdx": result["SPDX"],
                "risk": result["Risk"],
                "policy": result["Policy Decision"]
            }
        )

    response = client.responses.create(
        model="gpt-5",
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
{licenses_for_ai}
"""
    )

    logger.info(
        "AI compliance advice generated successfully"
    )

    return response.output_text