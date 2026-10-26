"""Streamlit interface for the AILT9019 English grammar assistant."""

import logging

import streamlit as st

from analyzer import analyze_text

logger = logging.getLogger(__name__)
MAX_TEXT_LENGTH = 1000


def friendly_error(message: str) -> str:
    """Explain known provider failures without displaying raw API diagnostics."""
    if not message.startswith("API call failed:"):
        return message
    if "AccessDenied.Unpurchased" in message:
        return (
            "The AI provider has not enabled model access for this account. "
            "Complete Model Studio activation and any required account verification "
            "in the region matching your API key. If this persists, contact provider support. "
            "Reference: AccessDenied.Unpurchased."
        )
    if "401" in message or "AuthenticationError" in message or "InvalidApiKey" in message:
        return "The AI provider could not authenticate the API key. Check the key and its matching regional endpoint."
    if "403" in message or "PermissionDenied" in message or "AccessDenied" in message:
        return "This account or workspace does not have permission to use the selected model. Check model access with your provider."
    if "429" in message or "RateLimit" in message:
        return "The AI provider reports a usage or rate limit. Check your quota and billing status before trying again."
    if "404" in message or "model_not_found" in message:
        return "The selected model or API endpoint was not found. Check the model identifier and regional endpoint."
    if "Connection" in message or "connection" in message or "SSL" in message:
        return "Cannot connect to the AI provider. Check your internet connection, endpoint, and certificate configuration."
    if "Timeout" in message or "timeout" in message or "timed out" in message:
        return "The AI service took too long to respond. Please try again later."
    return "The AI service could not complete the request. Please try again later or check the API configuration."

st.set_page_config(page_title="English Grammar Assistant", page_icon="📘", layout="centered")

st.title("English Grammar Assistant")
st.write("Check an English sentence or short paragraph and learn from its corrections.")
st.caption("Enter your text → Select Analyse → Read the corrections and explanations.")
st.caption("Your text is sent to an external AI service. Avoid entering personal or confidential information.")

with st.form("grammar_form"):
    user_text = st.text_area(
        "English text",
        height=180,
        max_chars=MAX_TEXT_LENGTH,
        placeholder="Example: She go to school every day.",
        help="Enter a sentence or short paragraph, up to 1,000 characters. English only.",
    )
    submitted = st.form_submit_button("Analyse", type="primary")

if submitted:
    # A new submission replaces previous feedback, including on validation failure.
    st.session_state.pop("analysis", None)
    st.session_state.pop("analysed_text", None)
    cleaned_text = user_text.strip()
    if not cleaned_text:
        st.warning("Please enter an English sentence or short paragraph.")
    elif len(cleaned_text) < 2 or not any(character.isalpha() for character in cleaned_text):
        st.warning("Please enter an English sentence containing words.")
    elif len(cleaned_text) > MAX_TEXT_LENGTH:
        st.warning("Please shorten your text to 1,000 characters or fewer.")
    else:
        try:
            with st.spinner("Analysing your text…"):
                result = analyze_text(cleaned_text)
            if not result["success"]:
                # The backend's API error may contain provider details; use a friendly message.
                message = result.get("message", "Analysis could not be completed. Please try again.")
                st.error(friendly_error(message))
            else:
                st.session_state["analysis"] = result
                st.session_state["analysed_text"] = cleaned_text
        except Exception:
            logger.exception("Grammar analysis could not be completed")
            st.error("Analysis could not be completed. Please try again or ask the team to check the backend.")

if "analysis" in st.session_state:
    result = st.session_state["analysis"]
    st.divider()
    st.subheader("Original text")
    st.text(st.session_state["analysed_text"])
    st.subheader("Corrected text")
    # Render submitted and generated text literally, without interpreting Markdown or HTML.
    st.text(result["corrected_text"])
    st.subheader("Grammar feedback")
    errors = result["errors"]
    if not errors:
        st.success("The analyser found no grammar mistakes in this text.")
    else:
        count = len(errors)
        st.info(f"{count} grammar {'issue' if count == 1 else 'issues'} found.")
        for number, error in enumerate(errors, start=1):
            with st.container(border=True):
                st.write(f"Correction {number}")
                st.caption("Original wording")
                st.text(error["original"])
                st.caption("Suggested correction")
                st.text(error["corrected"])
                st.caption("Explanation")
                st.text(error["explanation"])
    if result.get("grammar_explanations"):
        st.subheader("Grammar notes")
        for explanation in result["grammar_explanations"]:
            st.text(explanation)

st.divider()
st.caption("AI feedback may contain mistakes. Use it for learning; it is not an official language assessment.")
with st.expander("Setup and scope"):
    st.write("This first version focuses on English grammar corrections and explanations.")
    st.write("To enable analysis, configure your own API key in the local .env file using .env.example. See README.md for setup steps.")
    st.write("Vocabulary tools, CEFR assessment, additional languages, and saved history are outside this interface's current scope.")
