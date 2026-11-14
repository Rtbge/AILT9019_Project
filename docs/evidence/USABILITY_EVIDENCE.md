# Usability evidence — English Grammar Assistant (Person 2)

Recorded 14 November 2026. Owner: WU Tianxin, Team 26.

## Honesty statement

This file contains a **scripted first-use walkthrough executed by the
developer with browser automation**, plus a **blank peer-test form**. No human
participant was observed, no satisfaction score was measured, and no
participant data is invented. A real non-technical peer test must be completed
using the form below before the team claims user-based usability evidence.
Screenshots are genuine captures of a local run of the submitted `app.py`;
those taken in offline demo mode show a visible "not a live AI model result"
banner.

## Environment

| Item | Value |
| --- | --- |
| Date | 14 November 2026 |
| Application | `app.py` from this repository, run locally with `python -m streamlit run app.py` |
| Python / Streamlit | 3.14.7 / 1.66.1 |
| Browser | Google Chrome (headless via Playwright), 1,280 px viewport |
| Local addresses used | `127.0.0.1:8501` (labelled offline demo mode), `127.0.0.1:8502` (real configuration) |
| Credentials | A local `.env` was used for the real-mode run; no key appears in screenshots, code, logs or this file |

## Scripted first-use walkthrough

The walkthrough follows the path a first-time, non-technical learner would
take. Each step was executed against the running application.

| # | Task | Observed result | Evidence |
| --- | --- | --- | --- |
| 1 | Open the page without an API key configured in the browser | Page loads; title, three-step instruction, two use cases, text box, CEFR selector and Analyse button are visible. No credential is requested in the interface. | `01-start.png` |
| 2 | Choose "Check my own writing" and type `She go to school every day.` | Use-case guidance changes to a writing-focused explanation and the example placeholder changes. The radio selection persists after submission. | `02-writing-correction.png` |
| 3 | Press Analyse | A loading spinner appears; the results page shows original text, corrected text, a word-level highlighted diff (removed wording struck through, new wording underlined), one correction card with a plain-English reason, grammar notes, vocabulary pairs and a CEFR estimate with the non-official disclaimer. | `02-writing-correction.png` |
| 4 | Choose "Understand a text I found" and type an already-correct sentence | The app reports no grammar mistakes and still provides grammar notes, vocabulary and a CEFR estimate — the reading-oriented use case works without a correction. | `03-understand-correct.png` |
| 5 | Enter predominantly non-Latin text | A plain-language refusal explains that the tool only checks English and asks for an English sentence. No provider call is made. | `04-refusal.png` |
| 6 | Submit a normal English sentence with the real provider configuration | The provider returned 403 `AccessDenied.Unpurchased`; the app shows an actionable account-activation message and does not expose raw diagnostics or credentials. The application remains usable. | `05-provider-error.png` |
| 7 | Submit empty, one-character, numbers-only and punctuation-only input | Local validation warnings appear before any provider call (covered by `test_invalid_inputs_do_not_call_provider`). | `TEST_RESULTS.md` |

## Observations that can be stated from the walkthrough

- The interface uses plain-language labels ("What would you like to do?",
  "Step 1", "Why this changed") and avoids grammatical jargon in navigation.
- A distinct loading indicator separates submission from results.
- Error and refusal states are visibly different from successful results
  (yellow warning vs red error) and include an action the learner can take.
- All submitted and generated text is rendered literally, so HTML-like user
  input does not alter the page layout.
- Results persist when the page reruns and are replaced on the next submission.

These are **developer observations of interface behaviour**, not user
satisfaction findings.

## Accessibility checks performed

- The public webpage (`docs/index.html`) has semantic headings, a skip link,
  table headers, alt text for every screenshot, and no login requirement.
- Streamlit widgets are keyboard reachable and have visible labels and help
  tooltips for the use-case choice and CEFR selector.
- Status messages use Streamlit's native warning/error/info components rather
  than colour alone.
- Colour combinations in the diff (red struck-through / green underlined) are
  accompanied by a text legend and by per-correction cards, so meaning does not
  depend on colour alone.

## Blank peer-test form (to be completed by a real participant)

Complete one form per participant. Do not publish private contribution details
or personal data on the public webpage; keep completed forms in the team ZIP or
appendix only.

```
Participant role (e.g. "non-technical undergraduate"): ______________
Date: ______________   Browser / device: ______________

Task A — without any instructions beyond the page itself, use
"Check my own writing" on a sentence you wrote that contains one mistake.
  Completed without help?  Yes / No
  Time taken: ______________
  What was confusing? ______________________________________

Task B — use "Understand a text I found" on a correct sentence and find
the vocabulary meaning and the CEFR estimate.
  Completed without help?  Yes / No
  Time taken: ______________
  What was confusing? ______________________________________

Task C — deliberately enter a non-English sentence.
  Did the message explain what to do next?  Yes / No
  Suggested improvement: __________________________________

Overall (1 = very hard, 5 = very easy):  ____ / 5
One thing to change first: ____________________________________
Participant initials (optional): ______________
```

## Screenshot index

| File | Mode | Shows |
| --- | --- | --- |
| `01-start.png` | Real configuration, no demo banner | Start page, two use cases, CEFR selector, input guidance |
| `02-writing-correction.png` | Labelled offline demo | Writing check: correction, highlighted diff, explanation, vocabulary, CEFR |
| `03-understand-correct.png` | Labelled offline demo | Reading guide: no-mistakes case with grammar notes, vocabulary, CEFR |
| `04-refusal.png` | Real configuration | Explained refusal for non-English input |
| `05-provider-error.png` | Real configuration | Real 403 provider failure shown as an actionable message |

The offline demo screenshots must never be described as live AI inference.
