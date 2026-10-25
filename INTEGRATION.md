# INTEGRATION.md – Streamlit Frontend Integration Guide

This document tells Person 2 exactly how to connect the Streamlit frontend
to the grammar-analysis backend.

---

## 1. Files You Need

| File | Purpose |
|---|---|
| `analyzer.py` | The backend module — import `analyze_text` from it |
| `requirements.txt` | Python packages to install |
| `.env.example` | Template for API credentials |

**Copy `.env.example` to `.env`** and fill in real credentials before running
the app.

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs `openai`, `python-dotenv`, and `pytest`.

---

## 3. Configure API Credentials

Create a file named `.env` in the project root:

```env
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_API_KEY=sk-your-own-key-here
OPENAI_MODEL=qwen-plus
```

> **Important:** Each team member must use their own API key.
> Do not reuse credentials from other tools or subscriptions.

---

## 4. Importing the Backend

In your Streamlit app (e.g. `app.py`):

```python
from analyzer import analyze_text
```

That is the only public function you need.

---

## 5. Function Signature

```python
analyze_text(text: str, cefr_level: str | None = None) -> dict
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | `str` | Yes | The English sentence or paragraph to analyse |
| `cefr_level` | `str` or `None` | No | Learner's CEFR level hint (`"A1"` through `"C2"`) |

---

## 6. Return Dictionary

The function always returns a `dict` with these keys:

| Key | Type | Description |
|---|---|---|
| `success` | `bool` | `True` if analysis completed; `False` on any error |
| `original_text` | `str` | The text the user submitted |
| `corrected_text` | `str` or `None` | The grammatically corrected text (None if `success=False`) |
| `errors` | `list[dict]` | Each error has `original`, `corrected`, and `explanation` |
| `grammar_explanations` | `list[str]` | Human-readable explanations of the grammar points |
| `vocabulary` | `list[dict]` | Each entry has `word` and `meaning` |
| `cefr_estimate` | `str` or `None` | Estimated CEFR level (e.g. `"B1"`) |
| `cefr_note` | `str` | Explanation of the CEFR estimate + disclaimer |
| `message` | `str` | A user-facing summary message |

---

## 7. Handling Errors

Always check `result["success"]` before rendering results.

```python
result = analyze_text(user_input)

if not result["success"]:
    st.error(result["message"])
    # Stop here — corrected_text, errors, etc. are empty/None
    return
```

When `success` is `False`:
- `corrected_text` is `None`
- `errors` is `[]`
- `grammar_explanations` is `[]`
- `vocabulary` is `[]`
- `cefr_estimate` is `None`
- `message` explains what went wrong

**Possible failure reasons:**

| Condition | Example message |
|---|---|
| Empty input | `"Input text is empty. Please enter a sentence or paragraph."` |
| Too short | `"Input is too short. Please enter at least a full sentence."` |
| Too long | `"Input is too long (1523 characters). Maximum allowed is 1000 characters."` |
| Non-English text | `"The input does not appear to be English. ..."` |
| Invalid CEFR level | `"Invalid CEFR level 'X9'. Use one of: A1, A2, B1, B2, C1, C2."` |
| Missing API key | `"API key is not configured. ..."` |
| API failure | `"API call failed: Connection refused"` |
| Bad model response | `"The AI model returned an unreadable response. ..."` |

---

## 8. Complete Streamlit Example

```python
import streamlit as st
from analyzer import analyze_text

st.title("English Grammar Learning Assistant")

user_input = st.text_area("Enter an English sentence or paragraph:")

cefr_level = st.selectbox(
    "Your CEFR level (optional):",
    ["", "A1", "A2", "B1", "B2", "C1", "C2"],
)

if st.button("Analyse"):
    if not user_input.strip():
        st.warning("Please enter some text to analyse.")
    else:
        with st.spinner("Analysing your text..."):
            result = analyze_text(
                text=user_input,
                cefr_level=cefr_level if cefr_level else None,
            )

        if not result["success"]:
            st.error(result["message"])
        else:
            # -- Summary message --
            st.success(result["message"])

            # -- Corrected text --
            st.subheader("Corrected Text")
            st.write(result["corrected_text"])

            # -- Errors --
            if result["errors"]:
                st.subheader("Corrections")
                for i, err in enumerate(result["errors"], 1):
                    with st.expander(f"Error {i}: \"{err['original']}\" → \"{err['corrected']}\""):
                        st.write(err["explanation"])

            # -- Grammar explanations --
            if result["grammar_explanations"]:
                st.subheader("Grammar Explanations")
                for exp in result["grammar_explanations"]:
                    st.write(f"• {exp}")

            # -- Vocabulary --
            if result["vocabulary"]:
                st.subheader("Vocabulary")
                for item in result["vocabulary"]:
                    st.write(f"**{item['word']}** – {item['meaning']}")

            # -- CEFR estimate --
            if result["cefr_estimate"]:
                st.subheader("CEFR Estimate")
                st.write(f"**Level:** {result['cefr_estimate']}")
                st.info(result["cefr_note"])
```

---

## 9. CEFR Disclaimer

Every successful response includes `cefr_note` which contains this disclaimer:

> *"Note: The CEFR estimate is approximate and generated by an AI model.
> It is not an official CEFR assessment."*

Display this to the user whenever you show the CEFR estimate.

---

## 10. Running Tests (Optional)

```bash
# Offline tests (no API key needed):
pytest test_backend.py -v

# Live smoke test (requires real API key in .env):
pytest test_backend.py -v --run-live
```

---

## 11. Known Limitations

1. **Mixed-language text** – Text that is primarily English but contains a
   few non-Latin characters (loanwords, proper nouns) is accepted. Text
   where more than 30 % of alphabetic characters are non-Latin is rejected.

2. **Very short input** – Single characters are rejected; the user must
   provide at least a full sentence.

3. **API latency** – The first call may take 2–5 seconds depending on the
   provider. Use `st.spinner()` to show a loading indicator.

4. **Model may occasionally produce non-JSON** – The backend handles this
   gracefully and returns `success: False`.
