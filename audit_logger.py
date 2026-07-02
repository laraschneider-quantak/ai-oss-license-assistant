from logger import logger


def log_ai_request(audit_data):
    """
    Log AI request metadata for audit purposes.
    """

    logger.info(
        "AI AUDIT | %s",
        audit_data
    )