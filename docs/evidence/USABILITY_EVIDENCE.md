# Usability evidence for the English Grammar Assistant

Recorded 16 November 2026 for AILT9019 Team 26.

## Scripted first-use walkthrough

The walkthrough ran the current Streamlit interface locally in Chrome with
Playwright at a 1,190-pixel viewport. The environments used Python 3.14.7 and
Streamlit 1.66.1. The standard interface ran with an empty API key and the
offline demo used the two built-in fixtures. Both processes ran on localhost.

| Task | Observed result | Evidence |
| --- | --- | --- |
| Open the standard app | The form shows two tasks, an editable English text box, an optional CEFR selector and the Analyse button. | [Analysis form](../screenshots/analysis-form.png) |
| Select **Understand a text I found** in the offline demo, then show its feedback | The fixed example displays grammar notes, vocabulary and a CEFR estimate. The result reports no grammar mistakes. | [Reading guide example](../screenshots/reading-guide-example.png) |
| Switch to **Check my own writing** and show its feedback | The app removes the previous reading result when the task changes. The new example shows the correction, the struck-through original word, the underlined replacement and the reason for the change. | [Writing correction example](../screenshots/writing-correction-example.png) |
| Submit `12345` in the standard app | The form asks for an English sentence containing words. The validation branch stops before calling the backend. | [Invalid input warning](../screenshots/invalid-input-warning.png) |
| Submit an English sentence with no API key configured | The app displays a configuration message and leaves the form available. | [Missing API configuration](../screenshots/missing-provider-configuration.png) |

The offline captures show fixed educational examples and the interface marks
them as such. The walkthrough records scripted observations. Human participant
feedback and satisfaction scores have yet to be collected.

## Accessibility observations

- The app gives visible labels to the task controls and text fields. Standard
  Streamlit status components display input warnings and configuration errors.
- The writing diff uses strikethrough and underline along with colour. A text
  legend and correction cards identify the original and suggested wording.
- The project webpage has a skip link, descriptive links, semantic headings and
  screenshot alt text. Its layout supports both desktop and mobile widths.

## Blank peer-test form

Ask a non-technical learner to complete these tasks and record their
observations. Keep completed forms and identifying information in the team's
private materials.

```text
Participant role: ____________________
Date: ______________   Browser / device: ______________

Task A. Use Check my own writing. Find the corrected wording and its reason.
  Completed without help?  Yes / No
  Time taken: ______________
  What was confusing? ______________________________________

Task B. Use Understand a text I found. Find a vocabulary meaning and the
CEFR estimate.
  Completed without help?  Yes / No
  Time taken: ______________
  What was confusing? ______________________________________

Task C. Submit numbers only in the standard app.
  Did the message explain what to do next?  Yes / No
  Suggested improvement: ___________________________________

Overall ease of use (1 = very hard, 5 = very easy): ____ / 5
One thing to change first: __________________________________
```
