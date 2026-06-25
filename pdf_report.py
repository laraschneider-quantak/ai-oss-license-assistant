from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf_report(
    report_path,
    repo_name,
    compliance_score,
    overall_policy,
    overall_risk,
    ai_advice
):
    """
    Generate a PDF compliance report.
    """

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        report_path
    )

    story = []

    story.append(
        Paragraph(
            "OSS Compliance Report",
            styles["Heading1"]
        )
    )

    story.append(
        Spacer(
            1,
            20
        )
    )

    story.append(
        Paragraph(
            f"<b>Repository:</b> {repo_name}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Compliance Score:</b> {compliance_score}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Overall Policy:</b> {overall_policy}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Overall Risk:</b> {overall_risk}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(
            1,
            20
        )
    )

    story.append(
        Paragraph(
            "AI Compliance Advice",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            ai_advice,
            styles["Normal"]
        )
    )

    doc.build(
        story
    )