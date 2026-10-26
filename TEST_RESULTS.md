## Test Case Results

Command: `python -m pytest -q -p no:cacheprovider`

Latest run: **37 passed, 1 skipped in 1.22s**.
All default checks are offline. The live backend smoke test is opt-in and skipped.
No real model call was made during this final submission verification.

## Interface coverage

| Scenario | Evidence and outcome |
| --- | --- |
| Incorrect sentence | Real UI and real backend parse a simulated model response; correction and explanation displayed |
| Correct sentence | No-mistakes message and corrected text displayed |
| Empty, whitespace, one-letter, numbers-only, punctuation-only, Chinese input | Validation shown; no provider request |
| Multiple mistakes | Both correction cards and explanations displayed |
| Long paragraph | Text and results displayed without UI exceptions |
| Character limit | Streamlit limits input to 1,000 characters |
| HTML-like text | Original and corrected wording rendered literally using st.text |
| Rerun | Results preserved without another provider request |
| Later invalid submission or provider failure | Previous successful feedback removed |
| Missing key | Setup error displayed |
| Malformed model JSON | Backend failure displayed |
| Provider 401 / 403 / 404 / 429, connection and timeout errors | Actionable messages shown without raw diagnostics or simulated secret |

Simulated responses establish interface/backend integration; they do not measure actual AI accuracy.

## Live integration status

Earlier live checks reached the configured Alibaba Singapore endpoint. Model-list access returned HTTP 200 and included qwen-plus. Actual generation returned HTTP 403 with `AccessDenied.Unpurchased`. The UI displayed the failure without crashing.

The user subsequently submitted identity verification and the console shows it awaiting review. The cause has not been independently resolved; completing review does not by itself prove model access will work.

Successful live grammar analysis remains unverified. After provider access is enabled, run one short manual analysis before recording or claiming an end-to-end live demonstration.

## Live Testing Results

| Scenario | Cases | Results |
| --- | --- | --- |
| 1 mistake in sentence | "Our school have a busy elevator." | Mistake detected, corrected and epxlained |
| Empty sentence | "" | Detected locally without sending any API requests |
| Non-English entered| "Donde Estas?" | Detected by model and corrected user to use English instead of Spanish|
| More than 1000 characters entered | Lots of "How are you?" | Detected by locally and cannot enter more than 1000 characters in the text box |
| 3 mistakes in sentence| "We school have an busy elevator." | All mistakes detected, corrected and explained |
| Only numbers entered | "3.1415926 65536" | Detected locally and prompts user to enter English characters |
| Incomprehensible text | "epvqnwuvv9sduibqwo" | "This text is not a recognizable English word or sentence, so there are no English grammar mistakes to correct. Normal English grammar rules cannot be applied because the text does not contain clear English words or sentence structure." |
| Attemped SQL injection | "" OR COUNT(*) NOT NULL" | No security issues, input treated as normal English |

## Scope and attribution

Added the Streamlit UI, dependency, offline UI integration tests, setup documentation, and handoff evidence. Analyzer.py and backend tests are included unchanged to make the package runnable. No CEFR dataset or additional language support has been added.
