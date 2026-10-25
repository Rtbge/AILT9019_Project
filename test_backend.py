"""
test_backend.py – Automated tests for analyzer.analyze_text().

Tests run OFFLINE using mocked API responses (no live API key needed).

Run:
    pytest test_backend.py -v

Optional live smoke test:
    pytest test_backend.py -v --run-live
    (requires OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL in env)
"""

from __future__ import annotations

import json
import os
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Helpers: mock the OpenAI client so no real API calls are made
# ---------------------------------------------------------------------------


def _make_mock_response(content: str) -> MagicMock:
    """Build a fake OpenAI ChatCompletion response object."""
    message = MagicMock()
    message.content = content
    choice = MagicMock()
    choice.message = message
    response = MagicMock()
    response.choices = [choice]
    return response


def _mock_client_factory(mock_response: MagicMock):
    """Return a patch-compatible class whose instances return *mock_response*."""

    class FakeOpenAI:
        def __init__(self, **kwargs):
            self.chat = MagicMock()
            self.chat.completions = MagicMock()
            self.chat.completions.create = MagicMock(return_value=mock_response)

    return FakeOpenAI


# ---------------------------------------------------------------------------
# Sample JSON responses the mocked LLM would return
# ---------------------------------------------------------------------------

SUBJECT_VERB_RESPONSE = json.dumps({
    "corrected_text": "She goes to school every day.",
    "errors": [
        {
            "original": "She go to school every day.",
            "corrected": "She goes to school every day.",
            "explanation": "With 'she' (third person singular), the verb needs an -s ending in the present simple tense.",
        }
    ],
    "grammar_explanations": [
        "In present simple tense, use 'goes' (not 'go') with he/she/it.",
    ],
    "vocabulary": [
        {"word": "school", "meaning": "a place where children go to learn"},
    ],
    "cefr_estimate": "A1",
    "cefr_note": "This is a basic present simple sentence, typical of A1 level.",
})

CONDITIONAL_RESPONSE = json.dumps({
    "corrected_text": "If I had studied harder, I would have passed the exam.",
    "errors": [
        {
            "original": "If I would have studied harder",
            "corrected": "If I had studied harder",
            "explanation": "In a third conditional 'if' clause, use the past perfect (had + past participle), not 'would have'.",
        }
    ],
    "grammar_explanations": [
        "Third conditional structure: If + past perfect, would have + past participle.",
        "The 'if' clause never uses 'would'. Use 'had studied' instead of 'would have studied'.",
    ],
    "vocabulary": [
        {"word": "exam", "meaning": "a formal test of knowledge"},
        {"word": "harder", "meaning": "with more effort"},
    ],
    "cefr_estimate": "B2",
    "cefr_note": "Third conditional is typically introduced at B1–B2 level.",
})

CORRECT_RESPONSE = json.dumps({
    "corrected_text": "The children are playing in the park.",
    "errors": [],
    "grammar_explanations": [
        "Your sentence is grammatically correct. Well done!",
        "'The children are playing' uses the present continuous tense correctly.",
    ],
    "vocabulary": [
        {"word": "children", "meaning": "more than one child"},
        {"word": "park", "meaning": "a public outdoor area for recreation"},
    ],
    "cefr_estimate": "A2",
    "cefr_note": "Present continuous with a simple subject is typical of A1–A2 level.",
})

MIXED_LANGUAGE_RESPONSE = json.dumps({
    "corrected_text": "I want to go to the market.",
    "errors": [
        {
            "original": "I want to 去 market",
            "corrected": "I want to go to the market",
            "explanation": "'去' is Chinese for 'go'. In English, use 'go to' instead.",
        }
    ],
    "grammar_explanations": [
        "The text contains a Chinese character (去) mixed into an English sentence. Use the English equivalent 'go to'.",
    ],
    "vocabulary": [
        {"word": "market", "meaning": "a place where goods are bought and sold"},
    ],
    "cefr_estimate": "A1",
    "cefr_note": "The English portion is basic, but mixed-language input makes assessment less reliable.",
})


# ---------------------------------------------------------------------------
# Tests – offline (mocked API)
# ---------------------------------------------------------------------------


class TestAnalyzeTextMocked:
    """All tests in this class use mocked OpenAI responses."""

    # -- 1. Incorrect subject-verb agreement --------------------------------
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-fake"})
    @patch("analyzer.OpenAI", _mock_client_factory(_make_mock_response(SUBJECT_VERB_RESPONSE)))
    def test_subject_verb_agreement(self):
        from analyzer import analyze_text

        result = analyze_text("She go to school every day.")

        assert result["success"] is True
        assert result["corrected_text"] == "She goes to school every day."
        assert len(result["errors"]) == 1
        assert result["errors"][0]["original"] == "She go to school every day."
        assert "goes" in result["errors"][0]["corrected"]
        assert "third person" in result["errors"][0]["explanation"].lower() or "she" in result["errors"][0]["explanation"].lower()
        assert result["cefr_estimate"] == "A1"
        assert result["message"].startswith("Found 1")

    # -- 2. Incorrect conditional sentence ----------------------------------
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-fake"})
    @patch("analyzer.OpenAI", _mock_client_factory(_make_mock_response(CONDITIONAL_RESPONSE)))
    def test_conditional_sentence(self):
        from analyzer import analyze_text

        text = "If I would have studied harder, I would have passed the exam."
        result = analyze_text(text)

        assert result["success"] is True
        assert "had studied" in result["corrected_text"]
        assert len(result["errors"]) >= 1
        assert any("would have" in e["original"].lower() for e in result["errors"])
        assert result["cefr_estimate"] == "B2"
        assert any("conditional" in exp.lower() for exp in result["grammar_explanations"])

    # -- 3. Grammatically correct sentence ----------------------------------
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-fake"})
    @patch("analyzer.OpenAI", _mock_client_factory(_make_mock_response(CORRECT_RESPONSE)))
    def test_correct_sentence(self):
        from analyzer import analyze_text

        result = analyze_text("The children are playing in the park.")

        assert result["success"] is True
        assert result["errors"] == []
        assert result["corrected_text"] == "The children are playing in the park."
        assert any("correct" in exp.lower() for exp in result["grammar_explanations"])
        assert result["message"].startswith("No grammar mistakes")

    # -- 4. Empty input -----------------------------------------------------
    def test_empty_input(self):
        from analyzer import analyze_text

        result = analyze_text("")
        assert result["success"] is False
        assert "empty" in result["message"].lower()

        result_none = analyze_text(None)  # type: ignore[arg-type]
        assert result_none["success"] is False

        result_spaces = analyze_text("   ")
        assert result_spaces["success"] is False

    # -- 5. Overly long input -----------------------------------------------
    def test_too_long_input(self):
        from analyzer import analyze_text

        long_text = "word " * 300  # ~1500 chars
        result = analyze_text(long_text)

        assert result["success"] is False
        assert "too long" in result["message"].lower()

    # -- 6. Too short input -------------------------------------------------
    def test_too_short_input(self):
        from analyzer import analyze_text

        result = analyze_text("a")
        assert result["success"] is False
        assert "too short" in result["message"].lower()

    # -- 7. Invalid CEFR level ----------------------------------------------
    def test_invalid_cefr_level(self):
        from analyzer import analyze_text

        result = analyze_text("Hello world.", cefr_level="X9")
        assert result["success"] is False
        assert "invalid cefr" in result["message"].lower()

    # -- 8. Valid CEFR level accepted ----------------------------------------
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-fake"})
    @patch("analyzer.OpenAI", _mock_client_factory(_make_mock_response(CORRECT_RESPONSE)))
    def test_valid_cefr_level(self):
        from analyzer import analyze_text

        result = analyze_text("The children are playing in the park.", cefr_level="b1")
        assert result["success"] is True

    # -- 9. Heavily mixed-language input is rejected -----------------------
    def test_mixed_language_input_rejected(self):
        """
        Text that is primarily non-English (majority of alphabetic
        characters in a non-Latin script) is rejected before the API
        call.  'I want to 去 market' has 15 Latin letters vs 1 CJK
        character — this passes because < 30 % non-Latin.  But a
        sentence where non-Latin letters dominate must be rejected.
        """
        from analyzer import analyze_text

        # Mostly Chinese characters — should be rejected
        result = analyze_text("我々要去 the market 买东西")
        assert result["success"] is False
        assert "does not appear to be english" in result["message"].lower()

    # -- 9b. Pure non-English input is rejected ----------------------------
    def test_pure_non_english_rejected(self):
        from analyzer import analyze_text

        result = analyze_text("这是一个测试句子")
        assert result["success"] is False
        assert "does not appear to be english" in result["message"].lower()

    # -- 9c. Mostly-English text with a few non-Latin chars is accepted ----
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-fake"})
    @patch("analyzer.OpenAI", _mock_client_factory(_make_mock_response(MIXED_LANGUAGE_RESPONSE)))
    def test_mostly_english_with_loanword(self):
        """
        A sentence that is overwhelmingly Latin-script but contains one
        or two non-Latin characters (loanwords, proper nouns) should
        still be accepted.
        """
        from analyzer import analyze_text

        result = analyze_text("I want to 去 market.")
        # 15 Latin letters vs 1 CJK character — well under 30 %
        assert result["success"] is True

    # -- 10. API failure handling -------------------------------------------
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-fake"})
    @patch("analyzer.OpenAI", side_effect=Exception("Connection refused"))
    def test_api_failure(self, _):
        from analyzer import analyze_text

        result = analyze_text("She go to school.")

        assert result["success"] is False
        assert "api call failed" in result["message"].lower()

    # -- 11. Model returns non-JSON -----------------------------------------
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-fake"})
    @patch("analyzer.OpenAI", _mock_client_factory(_make_mock_response("Sorry, I can't help with that.")))
    def test_non_json_response(self):
        from analyzer import analyze_text

        result = analyze_text("She go to school.")

        assert result["success"] is False
        assert "unreadable" in result["message"].lower()

    # -- 12. Model returns JSON fenced in markdown --------------------------
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-fake"})
    def test_markdown_fenced_json(self):
        from analyzer import analyze_text

        fenced = "```json\n" + SUBJECT_VERB_RESPONSE + "\n```"
        fake_client = _mock_client_factory(_make_mock_response(fenced))

        with patch("analyzer.OpenAI", fake_client):
            result = analyze_text("She go to school every day.")

        assert result["success"] is True
        assert result["corrected_text"] == "She goes to school every day."

    # -- 13. Missing API key ------------------------------------------------
    @patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=False)
    def test_missing_api_key(self):
        from analyzer import analyze_text

        result = analyze_text("Hello world.")
        assert result["success"] is False
        assert "api key" in result["message"].lower()

    # -- 14. Response structure completeness --------------------------------
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-fake"})
    @patch("analyzer.OpenAI", _mock_client_factory(_make_mock_response(SUBJECT_VERB_RESPONSE)))
    def test_response_structure(self):
        from analyzer import analyze_text

        result = analyze_text("She go to school every day.")

        required_keys = {
            "success",
            "original_text",
            "corrected_text",
            "errors",
            "grammar_explanations",
            "vocabulary",
            "cefr_estimate",
            "message",
        }
        assert required_keys.issubset(result.keys())

        # Each error must have the three required sub-keys
        for err in result["errors"]:
            assert "original" in err
            assert "corrected" in err
            assert "explanation" in err

    # -- 15. CEFR disclaimer always present ---------------------------------
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-fake"})
    @patch("analyzer.OpenAI", _mock_client_factory(_make_mock_response(SUBJECT_VERB_RESPONSE)))
    def test_cefr_disclaimer(self):
        from analyzer import analyze_text

        result = analyze_text("She go to school every day.")
        assert result["success"] is True
        # The disclaimer is stored in cefr_note
        assert "not an official" in result.get("cefr_note", "").lower()

    # -- 16. Correct text gets positive / encouraging feedback -------------
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-fake"})
    @patch("analyzer.OpenAI", _mock_client_factory(_make_mock_response(CORRECT_RESPONSE)))
    def test_positive_feedback_for_correct_text(self):
        from analyzer import analyze_text

        result = analyze_text("The children are playing in the park.")
        assert result["success"] is True
        assert result["errors"] == []
        # The top-level message should be positive
        assert "great job" in result["message"].lower() or "correct" in result["message"].lower()
        # grammar_explanations should contain encouragement
        combined = " ".join(result["grammar_explanations"]).lower()
        assert "correct" in combined or "well done" in combined or "great" in combined

    # -- 17. Every error has a non-empty explanation -------------------------
    def test_error_explanations_non_empty(self):
        """
        Even if the model returns an empty explanation string, the
        backend should fill in a fallback so the frontend never shows
        a blank explanation to the learner.
        """
        from analyzer import _validate_response

        data = {
            "corrected_text": "She goes to school.",
            "errors": [
                {"original": "She go", "corrected": "She goes", "explanation": ""},
                {"original": "She go", "corrected": "She goes", "explanation": "   "},
            ],
            "grammar_explanations": ["Present simple agreement."],
            "vocabulary": [],
            "cefr_estimate": "A1",
        }
        validated = _validate_response(data)
        for err in validated["errors"]:
            assert err["explanation"].strip() != ""

    # -- 18. Cyrillic / Arabic / other scripts rejected --------------------
    @pytest.mark.parametrize("text", [
        "Это предложение на русском языке",
        "هذه جملة باللغة العربية",
        "これは日本語のテストです",
    ])
    def test_various_non_latin_scripts_rejected(self, text):
        from analyzer import analyze_text

        result = analyze_text(text)
        assert result["success"] is False
        assert "does not appear to be english" in result["message"].lower()


# ---------------------------------------------------------------------------
# Optional live smoke test (skipped unless --run-live flag is passed)
# ---------------------------------------------------------------------------


# pytest_addoption is in conftest.py (shared across all test modules)


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set – skipping live smoke test",
)
class TestLiveSmoke:
    """
    Live smoke test – calls the real API endpoint.
    Only runs when --run-live is passed AND OPENAI_API_KEY is set.
    Run with:  pytest test_backend.py -v --run-live
    """

    def test_live_basic(self, request: pytest.FixtureRequest):
        if not request.config.getoption("--run-live"):
            pytest.skip("Pass --run-live to enable live API tests")

        from analyzer import analyze_text

        result = analyze_text("She go to school every day.")
        assert result["success"] is True
        assert len(result["errors"]) >= 1
        print("\n[LIVE SMOKE TEST] Result:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
