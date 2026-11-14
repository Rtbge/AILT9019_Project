# Person 2 contribution and handoff (final frontend, 14 November 2026)

Owner: WU Tianxin (Team 26). Scope: Streamlit frontend, public project
webpage, interface screenshots and usability evidence, plus the frontend
explanation used in report Section 2. The final report PDF and the two videos
are deliberately **not** produced by this handoff.

## 1. Deliverables in this delivery

| File | Purpose |
| --- | --- |
| `app.py` | Final Streamlit interface (rewritten by Person 2) |
| `test_app.py` | 42 offline interface/backend integration checks |
| `TEST_RESULTS.md` | Recorded test run, coverage, live status, disputed midterm rows |
| `README.md` | Frontend usage, two use cases, offline demo, scope and limits |
| `docs/index.html` | Public project webpage (GitHub Pages source) |
| `docs/screenshots/` | Interface screenshots, clearly labelled by mode |
| `docs/evidence/USABILITY_EVIDENCE.md` | First-use walkthrough, usability checklist, peer-test template |
| `PERSON2_NOTES.md` | This handoff |

Not modified by Person 2: `analyzer.py`, `test_backend.py`, `conftest.py`,
`INTEGRATION.md`, `.env.example`, `.gitignore`, `requirements.txt`.

## 2. What the final frontend adds

- Two explicit use cases: **Understand a text I found** and **Check my own
  writing**, with different guidance, placeholders and result emphasis.
- Corrected text plus a word-level, inline highlighted diff (removed wording
  struck through, new wording underlined). All untrusted text is HTML- and
  Markdown-escaped before rendering.
- Grammar feedback cards, grammar notes, **vocabulary** entries, and the
  **CEFR estimate** with its "not an official CEFR assessment" disclaimer.
- Optional **CEFR level selection** (A1–C2) forwarded as `cefr_level`.
- Plain-language input guidance, a loading spinner, explained input refusals,
  and readable messages for provider errors without raw diagnostics.
- A "Setup, privacy and what this tool does not do" panel for non-technical
  learners.
- An opt-in, visibly labelled **offline demo mode**
  (`AILT9019_OFFLINE_DEMO=1`) so the interface can be demonstrated and
  screenshotted when the provider is unavailable. It is never presented as a
  live model result.

## 3. Backend contract (important for final integration)

The frontend uses only the documented, unchanged contract in `INTEGRATION.md`:

```python
analyze_text(text: str, cefr_level: str | None = None) -> dict
```

Fields read: `success`, `original_text`, `corrected_text`, `errors[]`
(`original`, `corrected`, `explanation`), `grammar_explanations[]`,
`vocabulary[]` (`word`, `meaning`), `cefr_estimate`, `cefr_note`, `message`.

Every field is read with `.get()` and normalised with `str()`/empty defaults,
so **Person 1 can add new output fields without breaking the frontend**.
No new output field is required from Person 1 for this delivery. If the final
backend changes a field name or adds a `mode`/`task` parameter, tell Person 2
before integration; the only call site is `_run_analysis()` in `app.py`.

The two use cases currently share one backend analysis path. The frontend
changes guidance and emphasis; the backend call is identical. If Person 1 adds
task-specific prompting, this is the single place to wire it in.

## 4. Verification evidence

- `python -m pytest -q -p no:cacheprovider` → **42 passed, 1 skipped**
  (14 November 2026, Python 3.14.7, Streamlit 1.66.1, pytest 9.1.1). All
  default checks are offline; the live smoke test is opt-in.
- Screenshots in `docs/screenshots/` were produced from a local run of the
  same `app.py`. Each file name states whether it shows the offline demo mode
  or a validation/refusal state.
- `docs/evidence/USABILITY_EVIDENCE.md` records a scripted first-use
  walkthrough and provides a blank peer-test form. No real participant data is
  invented; the peer-test section must be completed by a real person.

## 5. Live inference status — do not overclaim

A live call on 14 November 2026 with the configured key returned HTTP 403
`AccessDenied.Unpurchased` ("Access to model denied..."). This reproduces the
midterm blocker. Model-list access is not proof of generation access.

Consequences for the team: the report, webpage, presentation and demo must say
that live end-to-end inference is **unverified** until someone runs one real
analysis plus `pytest test_backend.py --run-live` and saves the output. The
midterm "Live Testing Results" rows in `TEST_RESULTS.md` are explicitly
relabelled as recorded observations with disputed live status.

## 6. Public webpage and GitHub Pages

`docs/index.html` is a self-contained static page (no external assets except
the repository link and the screenshots in `docs/screenshots/`). It covers
rubric C1: target users, problem, workflow, team-built elements, domain
customisation, run instructions, repository link, a genuine run example,
results, failure/boundary cases and limitations, with simple navigation.

To publish, a repository admin enables **Settings → Pages → Deploy from a
branch → `main` / `docs`**. The resulting URL
`https://rtbge.github.io/AILT9019_Project/` is public without login. Verify it
in a signed-out browser and record the check in the links file. The course
announcement's optional GitHub Pro route is not needed: this repository is
already public.

## 7. Coordination notes

- **Person 1**: no frontend-blocking change is needed. Please confirm the final
  model/endpoint configuration (the current default example is `qwen-plus` on
  an OpenAI-compatible DashScope endpoint, while the task split mentions
  Qwen3/Ollama). The webpage describes the code as it is, not the target.
- **Person 3**: environment requirements, pinned dependencies and fresh-clone
  evidence are yours. `README.md` was updated only where it described the
  frontend; please extend the environment/install sections and update the test
  count if you add tests. `test_app.py` now contains 5 new interface checks.
- **Person 4**: the webpage's Evaluation section uses the verifiable evidence
  available at this date (42 offline checks, recorded midterm walkthroughs,
  the proposal's 30–50 case design and 90% correctness target). A clearly
  marked slot is reserved for your measured `evaluation_dataset.csv` results.
  Send the measured numbers and I will insert them; none were invented here.
- **Everyone**: Section 6 of the report needs every member's contribution to
  every section. This handoff is the evidence for WU Tianxin's frontend,
  webpage, screenshots and usability work.

## 8. Ethics / AI-use disclosure reminder

An AI assistant was used to draft parts of `app.py`, `test_app.py`, the public
webpage copy and this documentation. All generated code was executed against
the offline test suite and reviewed by the member responsible before being
kept. This assistance must be recorded honestly in Section 5's seven AI-use
fields (tools/models, tasks supported, representative prompts, outputs
retained, verification performed, known limitations, responsible members),
together with the human checks listed in Section 4 above.

## 可直接发给组员的贡献说明

我完成了 Person 2 的最终前端与公开网页：app.py 现在支持两种使用场景（分析已有文本／纠正自己的写作）、纠错文本与逐词高亮、语法解释、词汇解释、CEFR 估计与免责声明、可选 CEFR 等级、加载提示、输入引导与拒答说明，并加入明确标注的离线演示模式以便在没有模型权限时做界面演示。公开网页放在 docs/index.html，可由 GitHub Pages 发布；截图与首次使用走查证据放在 docs/。离线测试 42 项通过、1 项跳过。真实模型调用仍被 403 AccessDenied.Unpurchased 拒绝，因此所有材料都不得声称已完成真实端到端推理。报告 PDF 与两段视频本轮未制作。
