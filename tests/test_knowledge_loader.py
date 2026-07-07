from knowledge_loader import load_knowledge_documents


def test_load_knowledge_documents_returns_lists():
    documents, ids = load_knowledge_documents()

    assert isinstance(documents, list)
    assert isinstance(ids, list)