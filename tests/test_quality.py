"""
test_quality.py — Test di qualità delle risposte chat (Claude-as-judge).

Richiedono ANTHROPIC_API_KEY e un database popolato.
Eseguire con: pytest -m quality
"""
import os
import pytest
import anthropic

QUALITY_CASES = [
    {
        "question": "What ETF has the ticker symbol SPY?",
        "must_contain": ["SPY"],
        "judge_prompt": "Does this response correctly identify SPY as an ETF (S&P 500 or similar)?",
    },
    {
        "question": "Quanti ETF ci sono nel database?",
        "must_contain": [],
        "judge_prompt": "Does this response provide a specific number of ETFs available in the database?",
    },
    {
        "question": "What is the most recent date available for QQQ prices?",
        "must_contain": ["QQQ"],
        "judge_prompt": "Does this response provide a specific date for QQQ price data?",
    },
]


def _judge(question: str, answer: str, judge_prompt: str) -> bool:
    """Usa Claude come giudice per valutare la correttezza della risposta."""
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=10,
        messages=[{
            "role": "user",
            "content": (
                f"Answer only YES or NO.\n"
                f"{judge_prompt}\n\n"
                f"Question asked: {question}\n\n"
                f"Response to evaluate:\n{answer}"
            ),
        }],
    )
    verdict = resp.content[0].text.strip().upper()
    return verdict.startswith("YES")


@pytest.mark.quality
@pytest.mark.parametrize("case", QUALITY_CASES)
def test_chat_quality(client, case):
    if not os.getenv("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY non impostata")

    res = client.post("/api/chat", json={"message": case["question"]})
    assert res.status_code == 200
    answer = res.json().get("response", "")
    assert answer, "La risposta non deve essere vuota"

    # Controlli stringa hard
    for expected in case["must_contain"]:
        assert expected.lower() in answer.lower(), \
            f"La risposta non contiene '{expected}': {answer[:200]}"

    # Valutazione Claude-as-judge
    if case.get("judge_prompt") and os.getenv("ANTHROPIC_API_KEY"):
        ok = _judge(case["question"], answer, case["judge_prompt"])
        assert ok, f"Il giudice ha valutato la risposta come NON corretta.\nRisposta: {answer[:300]}"
