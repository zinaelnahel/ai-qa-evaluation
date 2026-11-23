import os

import pytest

from rag import ABSTAIN, answer, load_fixture, ollama_generator, retrieve

CASES = load_fixture("cases")
ANSWERABLE = [case for case in CASES if case["expected_source"]]
UNANSWERABLE = [case for case in CASES if not case["expected_source"]]
LIVE_IDS = {"leave-archived-conflict", "expense-paraphrase", "it-contact",
            "unknown-parking", "restricted-record", "unapproved-record"}


@pytest.mark.parametrize("case", ANSWERABLE, ids=lambda case: case["id"])
def test_retrieval(case):
    sources = [doc["id"] for _, doc in retrieve(case["question"], case["audience"])]
    assert case["expected_source"] in sources


@pytest.mark.parametrize("case", ANSWERABLE, ids=lambda case: case["id"])
def test_grounding(case):
    assert answer(case["question"], case["audience"]) == {
        "answer": case["expected_quote"], "source": case["expected_source"],
    }


@pytest.mark.parametrize("case", UNANSWERABLE, ids=lambda case: case["id"])
def test_abstention(case):
    assert answer(case["question"], case["audience"]) == {"answer": ABSTAIN, "source": None}


def test_isolation_after_authorized_request():
    assert answer("finance reconciliation reference", "finance")["source"] == "finance"
    assert answer("finance reconciliation reference") == {"answer": ABSTAIN, "source": None}


def test_ambiguous_query_has_competing_evidence():
    ranked = retrieve("Is this the remote work policy or the laptop replacement policy?")
    assert [doc["id"] for _, doc in ranked] == ["equipment", "remote"]
    assert ranked[0][0] == ranked[1][0] == 2


def test_only_approved_evidence_reaches_generation():
    def inspect_evidence(question, evidence):
        assert [doc["id"] for doc in evidence] == ["leave"]
        return {"source": "leave", "quote": evidence[0]["text"]}

    assert answer("annual vacation paid days", generate=inspect_evidence)["source"] == "leave"


def test_restricted_evidence_never_reaches_generation():
    def inspect_evidence(question, evidence):
        assert [doc["id"] for doc in evidence] == ["support"]
        return {"source": "support", "quote": evidence[0]["text"]}

    question = "Where do I send IT support tickets for a reconciliation reference?"
    assert answer(question, generate=inspect_evidence)["source"] == "support"


@pytest.mark.parametrize("candidate", [
    {"source": "leave", "quote": "Unsupported policy statement"},
    {"source": "leave-old", "quote": "Employees receive 20 paid vacation days per calendar year."},
    {"source": "leave", "quote": "Employees receive 24 paid vacation days per calendar year.",
     "extra": "QA-UNVERIFIED-9921"},
    "unstructured answer",
], ids=["unsupported-quote", "archived-citation", "extra-field", "malformed-response"])
def test_untrusted_model_output(candidate):
    assert answer("annual vacation paid days", generate=lambda *_: candidate) == {
        "answer": ABSTAIN, "source": None,
    }


@pytest.mark.live
@pytest.mark.parametrize("case", [case for case in CASES if case["id"] in LIVE_IDS],
                         ids=lambda case: case["id"])
def test_live_model(case):
    model = os.environ.get("AI_QA_OLLAMA_MODEL")
    if not model:
        pytest.fail("Set AI_QA_OLLAMA_MODEL to an installed local model.")
    calls = []
    generate = ollama_generator(model)

    def record_call(question, evidence):
        calls.append(True)
        return generate(question, evidence)

    expected = {"answer": case["expected_quote"] or ABSTAIN, "source": case["expected_source"]}
    for _ in range(2):
        assert answer(case["question"], case["audience"], generate=record_call) == expected
    assert len(calls) == (2 if case["expected_source"] else 0)
