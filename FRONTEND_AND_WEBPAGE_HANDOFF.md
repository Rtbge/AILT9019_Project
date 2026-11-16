# Frontend and project webpage handoff

WU Tianxin · AILT9019 Team 26 · 16 November 2026

## Deliverables

| File | Purpose |
| --- | --- |
| [app.py](app.py) | Streamlit interface for the reading guide and writing check |
| [test_app.py](test_app.py) | Interface and backend integration checks with simulated responses |
| [README.md](README.md) | Setup, usage and limitations |
| [Project webpage](docs/index.html) | Public-facing project explanation and examples |
| [Interface screenshots](docs/screenshots/) | Captures of the standard interface, fixed examples and error handling |
| [Usability walkthrough](docs/evidence/USABILITY_EVIDENCE.md) | Scripted browser walkthrough and peer-test form |
| [Test record](TEST_RESULTS.md) | Automated results, coverage and live inference status |

## Frontend contribution for report Section 2

The Streamlit interface gives English learners two starting points. The reading
guide prioritises grammar explanations, contextual vocabulary and an approximate
CEFR estimate. The writing check prioritises the corrected text, word-level
changes and a reason for each suggested correction. Learners can optionally
select their own CEFR level to guide the difficulty of the explanations. The
CEFR level displayed in the result estimates the difficulty of the text.

The team built the task flow, word-level comparison, feedback layout, input
guidance and handling of provider failures. Streamlit supplies the widgets.
Both tasks call the same backend function,
`analyze_text(text, cefr_level=None)`, with the same response format. The
chosen task controls the presentation of the feedback. The configured language
model supplies the analysis through the OpenAI-compatible backend.

## Verification evidence

- Automated run on 16 November 2026 yielded **42 passed, 1 skipped**. The skipped
  test requires a real API configuration. The automated checks use simulated
  responses and cannot measure language feedback accuracy.
- The local Chrome walkthrough captured both fixed offline examples, rejection
  of numbers-only input and the missing API configuration message. The screenshots
  show the running interface and distinguish the fixed examples from live analysis.
- A previous real provider call on 14 November returned HTTP 403
  `AccessDenied.Unpurchased`. A successful live analysis and the educational
  accuracy score are pending verification.
- The scripted walkthrough records developer observations. The blank peer-test
  form is available for the team to collect feedback from a real participant.

## Publishing the project webpage

The GitHub Pages source is the `docs/` directory. After the team integrates the
reviewed changes into its release branch, a repository maintainer can select
**Settings → Pages → Deploy from a branch**, then select the release branch
and **/docs**. Verify the resulting project URL in a signed-out browser before
adding it to the submission links. Keep live API credentials in the app
host's secret settings or in a local, ignored `.env` file.

## AI-use record for the report

An AI assistant supported drafting and revising parts of the interface,
automated checks, webpage and documentation. Record the retained work, the
actual verification performed, the responsible reviewers and any limitations
in the team's AI-use disclosure.
