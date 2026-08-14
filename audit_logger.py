from logger import logger


def log_ai_request(audit_data):
    """
    Log AI request metadata for audit purposes.
    """

    logger.info(
        "AI AUDIT | %s",
        audit_data
    )


def log_rag_retrieval(
    strategy,
    knowledge_retrieved,
):
    """
    Log RAG retrieval metadata without
    logging document content.
    """

    print(
        "RAG AUDIT FUNCTION CALLED"
    )

    logger.info(
        (
            "RAG AUDIT | "
            "strategy=%s | "
            "knowledge_retrieved=%s"
        ),
        strategy,
        knowledge_retrieved,
    )


def log_workflow_event(
    event_data: dict,
):
    """
    Log workflow execution metadata
    for audit and traceability.
    """

    logger.info(
        "WORKFLOW AUDIT | %s",
        event_data,
    )