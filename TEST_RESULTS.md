## Automated test results

Command: `python -m pytest -q -p no:cacheprovider`

Final run (16 November 2026, Python 3.14.7, Streamlit 1.66.1, pytest 9.1.1):
**42 passed, 1 skipped**. All default checks are offline. The live backend
smoke test is opt-in and skipped. No real model call was made during this
verification run. Earlier midterm run: 37 passed, 1 skipped.

Five new interface checks were added for the final frontend: vocabulary and
CEFR rendering, optional CEFR level forwarding, the two use cases, explanatory
input refusals, and the labelled offline demo mode.

## Interface coverage

| Scenario | Evidence and outcome |
| --- | --- |
| Incorrect sentence | Real UI and real backend parse a simulated model response; correction, explanation and word-level diff displayed |
| Correct sentence | No-mistakes message, corrected text, grammar notes displayed |
| Empty, whitespace, one-letter, numbers-only, punctuation-only, Chinese input | Validation or explained refusal shown; no provider request for locally rejected inputs |
| Multiple mistakes | Both correction cards and explanations displayed |
| Vocabulary returned by backend | Each `word — meaning` pair rendered literally |
| CEFR returned by backend | Level metric, note and "not an official CEFR assessment" disclaimer displayed |
| Optional CEFR level selected | `cefr_level` forwarded to `analyze_text()` and verified by test |
| Both use cases | Selected task stored with the result. Reading prioritises vocabulary and writing prioritises corrections |
| Long paragraph | Text and results displayed without UI exceptions |
| Character limit | Streamlit limits input to 1,000 characters |
| HTML-like text | Original and corrected wording rendered literally; diff markup escapes all untrusted text |
| Rerun | Results preserved without another provider request |
| Later invalid submission or provider failure | Previous successful feedback removed |
| Missing key | Setup error displayed |
| Malformed model JSON | Backend failure displayed |
| Provider 401 / 403 / 404 / 429, connection and timeout errors | Actionable messages shown without raw diagnostics or simulated secret |
| Offline demo mode | Each task shows a fixed input and an explicit offline banner. Switching tasks hides the previous example feedback. No provider request is made |

The [local browser walkthrough](docs/evidence/USABILITY_EVIDENCE.md) also
records both examples, an invalid input warning and a missing configuration
message.

Simulated responses establish interface/backend integration; they do not
measure actual AI accuracy.

## Live integration status

A live call made on 14 November 2026 using a configured provider key returned
HTTP 403 `AccessDenied.Unpurchased` ("Access to model denied. Please make sure
you are eligible for using the model."). This reproduces the midterm blocker.
Earlier checks reached the configured endpoint and could list `qwen-plus`, but
model-list access does not prove generation access.

**Successful live grammar analysis remains unverified.** After model access is
enabled, run one short manual analysis and
`python -m pytest test_backend.py -v --run-live`, then record the output here
before claiming any live end-to-end execution. Do not present offline demo
output, simulated responses or the walkthrough rows below as live inference.

## Recorded manual walkthroughs (midterm submission)

The following rows were recorded in this file during the midterm submission.
Their live status is disputed: the same file's midterm "Live integration
status" section and the [frontend handoff](FRONTEND_AND_WEBPAGE_HANDOFF.md)
state that live analysis was blocked by
`AccessDenied.Unpurchased`. They are reproduced here as recorded observations,
not as independently verified live model runs, and need re-running once model
access is enabled.

| Scenario | Case | Recorded outcome |
| --- | --- | --- |
| 1 mistake in sentence | "Our school have a busy elevator." | Mistake detected, corrected and explained |
| Empty sentence | "" | Rejected locally without sending any API request |
| Non-English entered | "Donde Estas?" | Rejected / redirected to English |
| More than 1000 characters | Repeated "How are you?" | Rejected by the local character limit |
| 3 mistakes in sentence | "We school have an busy elevator." | All mistakes detected, corrected and explained |
| Only numbers | "3.1415926 65536" | Rejected locally, prompts for English words |
| Incomprehensible text | "epvqnwuvv9sduibqwo" | No English grammar mistakes reported; explanation that normal rules cannot be applied |
| Attempted SQL injection | `"" OR COUNT(*) NOT NULL` | Treated as ordinary text, no security issue observed |

## Scope and attribution

The frontend contribution covers the Streamlit UI, offline integration tests,
project webpage, interface screenshots and usability evidence. The test
fixtures retain non-Latin input coverage through escaped characters. The CEFR
estimate comes from the model. The private `.env` and local delivery archives
are excluded from Git.
