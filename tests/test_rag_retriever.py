from rag_retriever import (
    build_license_query,
    determine_retrieval_strategy
)

def test_retrieval_strategy_none():
    scan_results = []

    strategy = determine_retrieval_strategy(
        scan_results
    )

    assert strategy == "none"


def test_retrieval_strategy_direct_for_duplicate_license():
    scan_results = [
        {"license": "Apache-2.0"}
        for _ in range(100)
    ]

    strategy = determine_retrieval_strategy(
        scan_results
    )

    query = build_license_query(
        scan_results
    )

    assert query == "Apache-2.0"
    assert strategy == "direct"


def test_retrieval_strategy_semantic():
    scan_results = [
        {"license": "MIT"},
        {"license": "Apache-2.0"}
    ]

    strategy = determine_retrieval_strategy(
        scan_results
    )

    assert strategy == "semantic"


def test_build_license_query_removes_duplicates():
    scan_results = [
        {"license": "MIT"},
        {"license": "MIT"},
        {"license": "Apache-2.0"},
        {"license": "MIT"}
    ]

    query = build_license_query(scan_results)

    assert query == "Apache-2.0 MIT"