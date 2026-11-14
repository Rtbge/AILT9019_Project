# AILT9019 English Grammar Assistant

A learning tool for English grammar corrections, beginner-friendly explanations,
vocabulary notes and an approximate CEFR difficulty estimate. The Streamlit
interface (`app.py`) calls the team's `analyze_text()` backend (`analyzer.py`).

Public project webpage: `docs/index.html` (published with GitHub Pages at
`https://rtbge.github.io/AILT9019_Project/`).

## Run locally

Use Python 3.10 or later. After downloading the repository as a .zip and
decompressing it, open Terminal and run:

```bash
cd AILT9019_Project-main
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Open `.env` in a text editor and fill in your own provider settings:

```dotenv
OPENAI_API_BASE=https://your-provider-endpoint/v1
OPENAI_API_KEY=your-own-api-key
OPENAI_MODEL=your-provider-model-name
```

Use an OpenAI-compatible endpoint and a model that is enabled for your account.
The endpoint above is only a placeholder; see `.env.example` for concrete examples.
Keep `.env` private — it is excluded from Git. Never put credentials in `app.py`.
If `.env` already exists, edit it rather than copying over it.

Start the application:

```bash
python -m streamlit run app.py
```

Open the local address printed in Terminal (usually http://localhost:8501).
To stop the app, press Control+C. Restart it after changing API settings.
No API key is needed to open the page; a successful live analysis requires
valid settings and model access.

## Use the application

1. Choose **Understand a text I found** (explain grammar, vocabulary and
   difficulty of existing English text) or **Check my own writing** (correct and
   explain mistakes in a sentence you wrote).
2. Paste one English sentence or a short paragraph (up to 1,000 characters).
3. Optionally select your CEFR level (A1–C2) so explanations are written at a
   suitable level; leave it on "Not sure" otherwise.
4. Select **Analyse** and wait for the loading indicator to finish.
5. Read the original text, the corrected text, the highlighted word changes,
   each correction's explanation, grammar notes, vocabulary and the CEFR estimate.

Example input: `She go to school every day.`
An expected correction is `She goes to school every day.`, with an explanation
of subject–verb agreement. Actual feedback comes from the configured AI service
and may vary. Correct text receives a no-mistakes message.

Empty input, input without words, text that is predominantly non-Latin, and
overlong text receive a plain-language validation or refusal message. Missing
API settings, connection failures, rate limits and malformed model responses
appear as readable error messages rather than raw provider diagnostics.

### Offline demo mode (clearly labelled)

If the AI provider is unavailable, the interface can be shown against a fixed
sample response for demonstration and screenshot evidence:

```bash
AILT9019_OFFLINE_DEMO=1 python -m streamlit run app.py
```

A persistent banner states that the page is showing a **fixed sample response,
not a live AI model result**. Offline demo output must never be described as
live inference in reports, on the webpage or in recordings.

## Current scope and limitations

- English only, short texts (up to 1,000 characters). No saved history, no user
  accounts, no other languages, no full translation.
- The interface displays corrected text, word-level change highlighting,
  grammar explanations, vocabulary and the CEFR estimate plus its disclaimer.
  CEFR level selection is forwarded to the backend as `cefr_level`.
- The CEFR level is an **AI estimate, not an official CEFR assessment**. The
  backend currently generates it from the model; no fixed CEFR reference dataset
  is integrated in this version.
- The two use cases share one backend analysis path. The interface changes the
  guidance and the order of emphasis; the backend call is the same.
- Word-level highlighting is a token diff between the original and corrected
  text. It is an approximation and may not align exactly with the model's
  phrase-level `errors[]` entries. All displayed text is escaped so model or
  user text cannot inject markup into the page.
- The backend's language check uses character scripts, so other languages
  written with Latin letters may still be accepted.
- Text is sent to the configured external AI provider; do not enter personal or
  confidential information. AI feedback can be incorrect and is for learning,
  not official assessment.
- Analysis results persist only in the current Streamlit session and are
  replaced on the next submission; nothing is written to a file.

## Checks

With the virtual environment activated:

```bash
python -m pytest -q
```

Default tests run offline. Interface tests drive the real Streamlit app and the
real backend with simulated provider responses; they verify the
input-to-output connection, not live model accuracy. A live backend smoke test
is available separately:

```bash
python -m pytest test_backend.py -v --run-live
```

Live tests require valid API credentials and can incur provider charges.
See `INTEGRATION.md` for the backend return format,
`TEST_RESULTS.md` for the recorded test run and `PERSON2_NOTES.md` for the
frontend handoff.

## Person 2 delivery status

Final offline validation: **42 passed, 1 skipped** (`python -m pytest -q
-p no:cacheprovider`, 14 November 2026, Python 3.14 / Streamlit 1.66.1).
Person 2 deliverables: updated `app.py`, offline UI tests, the public webpage
in `docs/`, interface screenshots and usability evidence in `docs/evidence/`.

**Live inference is still unverified.** A call made on 14 November 2026 with a
configured key returned HTTP 403 `AccessDenied.Unpurchased` ("Access to model
denied"). Model-list access alone does not prove generation access. The
interface shows an account-activation message for this specific error. Re-run
`pytest test_backend.py --run-live` once model access is enabled, then record
the genuine live result before claiming end-to-end live execution.

The private `.env` file and local delivery archives are excluded from Git.
