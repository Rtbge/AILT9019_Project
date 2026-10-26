# AILT9019 English Grammar Assistant

A learning tool for English grammar corrections and beginner-friendly explanations.
The Streamlit interface calls Person 1's `analyze_text()` backend directly.

## Run locally

Use Python 3.10 or later. After downloading the repository as .zip and decompressing, open Terminal and run:

```bash
cd AILT9019_Project-main
cd AILT9019_Project-main
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Open `.env` in a text editor and fill in provider settings:

```dotenv
OPENAI_API_BASE=https://your-provider-endpoint/v1
OPENAI_API_KEY=your-own-api-key
OPENAI_MODEL=your-provider-model-name
```
Start the application:

```bash
python -m streamlit run app.py
```

Open the local address printed in Terminal (usually http://localhost:8501).
To stop the app, press Control+C in Terminal. Restart it after changing API settings.

## Use the application

1. Enter an English sentence or short paragraph (up to 1,000 characters).
2. Select **Analyse** and wait for feedback.
3. Read the original text, corrected text, and each correction's explanation.

Example input: `She go to school every day.`
An expected correction is `She goes to school every day.`, with an explanation
of subject–verb agreement. Actual feedback comes from the configured AI service
and may vary. Correct text receives a no-mistakes message.

Empty input and input without words receive a validation message. Backend
validation also rejects text that is predominantly in a non-Latin script.
Missing API settings or service failures appear as an error in the interface.
No API key is required to open the page; successful AI analysis requires valid settings.

## Current scope and limitations

- This version focuses on English grammar corrections and explanations.
- Text is sent to the configured external AI provider; avoid personal or confidential information.
- AI feedback can be incorrect and is for learning, not official assessment.
- The backend's language check uses scripts, so other languages written with Latin letters may pass it.
- The backend also returns vocabulary and an AI-generated CEFR estimate. This interface does not display those features, and no fixed CEFR reference dataset is integrated.
- Corrections appear in separate cards; inline highlighting, additional languages, and saved history are not implemented.
- Analysis results persist in the current Streamlit session and are replaced on the next submission. The interface does not save submissions to files.

## Checks

With the virtual environment activated:

```bash
python -m pytest -q
```

Default tests run offline. Interface tests use simulated provider responses and
the real backend to check the input-to-output connection. They do not establish
live model accuracy. A live backend smoke test is available separately:

```bash
python -m pytest test_backend.py -v --run-live
```

Live tests require valid API credentials and can incur provider charges.
See `INTEGRATION.md` for the backend return format.

## Person 2 delivery status

Offline validation: **37 passed, 1 skipped**. See `TEST_RESULTS.md` and `PERSON2_NOTES.md`.
Live generation remains blocked by the provider's `AccessDenied.Unpurchased` response;
model-list access alone does not verify inference access. Identity verification is awaiting review.

For that specific provider error the interface now displays an account activation/access message.
The private .env file and local delivery archives are excluded from Git.
