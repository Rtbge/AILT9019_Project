"""Offline integration checks: real Streamlit UI and backend, simulated provider."""

import json

import pytest
from unittest.mock import MagicMock, patch

from streamlit.testing.v1 import AppTest


def launch():
    return AppTest.from_file("app.py").run()


def submit(app, text):
    app.text_area[0].set_value(text)
    return app.button[0].click().run()


def provider_response(corrected, errors):
    response = MagicMock()
    response.choices[0].message.content = json.dumps({
        "corrected_text": corrected,
        "errors": errors,
        "grammar_explanations": ["Use the verb form that agrees with the subject."],
        "vocabulary": [],
        "cefr_estimate": "A1",
        "cefr_note": "Simple sentence.",
    })
    return response


def test_correction_flows_through_real_backend(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-key")
    with patch("analyzer.OpenAI") as client:
        client.return_value.chat.completions.create.return_value = provider_response(
            "She goes to school every day.",
            [{"original": "go", "corrected": "goes", "explanation": "Use goes with the singular subject she."}],
        )
        app = submit(launch(), "She go to school every day.")
        assert not app.exception
        values = [item.value for item in app.text]
        assert "She goes to school every day." in values
        assert "Use goes with the singular subject she." in values
        assert client.return_value.chat.completions.create.call_count == 1
        assert "CEFR Estimate" not in [item.value for item in app.subheader]
        # Invalid resubmission must not leave the old correction visible.
        submit(app, "   ")
        assert app.warning
        assert "She goes to school every day." not in [item.value for item in app.text]
        assert client.return_value.chat.completions.create.call_count == 1


def test_correct_sentence(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-key")
    with patch("analyzer.OpenAI") as client:
        client.return_value.chat.completions.create.return_value = provider_response("I like reading.", [])
        app = submit(launch(), "I like reading.")
        assert not app.exception
        assert "no grammar mistakes" in app.success[0].value
        assert "I like reading." in [item.value for item in app.text]


def test_invalid_inputs_do_not_call_provider():
    with patch("analyzer.OpenAI") as client:
        app = launch()
        for text in ["", "   ", "a", "12345", "!!!", "这是一个中文句子。"]:
            submit(app, text)
            assert not app.exception
            assert app.warning or app.error
            assert not app.text
        client.assert_not_called()


def test_missing_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with patch("analyzer._get_api_key", return_value=None):
        app = submit(launch(), "She goes to school.")
        assert not app.exception
        assert "API key is not configured" in app.error[0].value
        assert not app.text


def test_provider_failure_is_readable(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-key")
    with patch("analyzer.OpenAI", side_effect=RuntimeError("private provider diagnostics")):
        app = submit(launch(), "She go to school.")
        assert not app.exception
        assert "AI service could not complete" in app.error[0].value
        assert "private provider diagnostics" not in app.error[0].value
        assert not app.text


def test_unreadable_provider_response(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-key")
    with patch("analyzer.OpenAI") as client:
        client.return_value.chat.completions.create.return_value.choices[0].message.content = "not JSON"
        app = submit(launch(), "She go to school.")
        assert not app.exception
        assert "unreadable response" in app.error[0].value
        assert not app.text


@pytest.mark.parametrize(("diagnostic", "expected"), [
    ("Error code: 403 AccessDenied.Unpurchased secret-test-value", "Reference: AccessDenied.Unpurchased"),
    ("Error code: 401 InvalidApiKey secret-test-value", "could not authenticate"),
    ("Error code: 403 Model.AccessDenied secret-test-value", "does not have permission"),
    ("Error code: 429 secret-test-value", "usage or rate limit"),
    ("Error code: 404 model_not_found secret-test-value", "was not found"),
    ("Connection error secret-test-value", "Cannot connect"),
    ("Request timed out secret-test-value", "too long"),
])
def test_provider_diagnostics_are_actionable_and_private(diagnostic, expected):
    with patch("analyzer.analyze_text", return_value={"success": False, "message": "API call failed: " + diagnostic}):
        app = submit(launch(), "She go to school.")
        assert not app.exception
        assert expected in app.error[0].value
        assert "secret-test-value" not in app.error[0].value
        assert not app.text


def test_multiple_corrections_and_literal_text(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-key")
    with patch("analyzer.OpenAI") as client:
        client.return_value.chat.completions.create.return_value = provider_response(
            "She goes to school. They were late. <b>example</b>",
            [
                {"original": "go", "corrected": "goes", "explanation": "Use goes with she."},
                {"original": "was", "corrected": "were", "explanation": "Use were with they."},
            ],
        )
        app = submit(launch(), "She go to school. They was late. <b>example</b>")
        assert not app.exception
        assert "2 grammar issues found." in app.info[0].value
        values = [element.value for element in app.text]
        assert "Use goes with she." in values
        assert "Use were with they." in values
        assert "She goes to school. They were late. <b>example</b>" in values
        assert app.session_state["analysis"]["success"]
        # A rerun must preserve feedback and must not send another API request.
        app.run()
        assert "Use were with they." in [element.value for element in app.text]
        assert client.return_value.chat.completions.create.call_count == 1
        # A later provider failure must remove the earlier successful feedback.
        client.return_value.chat.completions.create.side_effect = RuntimeError("test failure")
        submit(app, "She go home.")
        assert app.error and not app.text
        assert client.return_value.chat.completions.create.call_count == 2


def test_input_limit_and_long_paragraph(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-key")
    with patch("analyzer.OpenAI") as client:
        paragraph = "I like reading. " * 60
        client.return_value.chat.completions.create.return_value = provider_response(paragraph.strip(), [])
        app = launch()
        assert app.text_area[0].max_chars == 1000
        submit(app, paragraph)
        assert not app.exception
        assert paragraph.strip() in [element.value for element in app.text]
        assert client.return_value.chat.completions.create.call_count == 1
        # Streamlit truncates oversized widget input to its declared character limit.
        submit(app, "a" * 1001)
        assert not app.exception
        assert len(app.text_area[0].value) == 1000
        assert client.return_value.chat.completions.create.call_count == 2
        last_request = client.return_value.chat.completions.create.call_args.kwargs
        assert "a" * 1001 not in last_request["messages"][1]["content"]
