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
    knowledge_retrieved
):
    
    print("RAG AUDIT FUNCTION CALLED")
    """
    Log RAG retrieval metadata without logging document content.
    """

    logger.info(
        (
            "RAG AUDIT | "
            "strategy=%s | "
            "knowledge_retrieved=%s"
        ),
        strategy,
        knowledge_retrieved
    )