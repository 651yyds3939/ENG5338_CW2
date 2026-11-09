# Contribution and AI-assistance record

This is a living record, not the final agreed statement. Proposed ownership is not
evidence of completed human work. Replace placeholders with names and student IDs.

| Member | Assigned responsibility | Actual implementation | Actual writing/review | Notebook location | Evidence/date |
|---|---|---|---|---|---|
| 1 — Wenyi | Framework, OLS, validation and integration | AI-assisted framework available; record actual human review/adaptation | To record | Sections 1–4, 7–8 and integration | Executed shared notebook and results; human evidence to record |
| 2 — Kiki | Random Forest | Progress reported in chat; artifacts not yet integrated/verified | To record | Section 6, Random Forest entry | To receive |
| 3 — name/ID to supply | Extra Trees | To record | To record | Section 6, Extra Trees entry | To supply |
| 4 — name/ID to supply | Histogram gradient boosting | To record | To record | Section 6, HGB entry | To supply |
| 5 — name/ID to supply | Cost and final testing | To record | To record | Sections 5 and 9 | To supply |

## AI assistance

2026-11-07 — OpenAI Codex/ChatGPT:

- Read the supplied CW2 brief and report templates, course dataset guide, existing
  CW1 notebook and supplied Moodle screenshot.
- Inspected schema, missingness and development-period distributions; proposed a
  CO virtual-sensor question, provisional deployment constraints, candidate models,
  shared chronological validation protocol and team allocation.
- Generated the common English notebook, execution/build scripts and Chinese study
  notes; ran data checks, linear-reference cross-validation and cost measurements.
- Checked recorded notebook outputs and exported development results. Candidate
  tuning, extended diagnostics and final held-out evaluation have not been run.

Human review, adaptation and agreement are pending. No member is credited with
implementation simply because the AI generated code in their proposed section.
Append later AI use, model experiments and human review with dates and locations.

Additional assistance — OpenAI Codex/ChatGPT explained candidate regression models,
checked scikit-learn official documentation, and consolidated the explanation into
`候选模型说明与选型建议_zh.md` at the user's request. This added study material only;
the model configurations and experiment results were not changed.

Additional assistance — At the user's request, OpenAI Codex/ChatGPT reread the local
CW1/CW2 briefs, the actual CW1 notebook and current CW2 status/protocol artifacts,
then wrote `项目全解读_CW1与CW2对照_zh.md`. The document explains the end-to-end
project, principles, methods, intended deliverables, current evidence, member roles
and the differences/connections between the two courseworks. No new model fits,
final-test evaluations or experiment configuration changes were performed.

Additional assistance — In response to the user's request to simplify team handoff,
OpenAI Codex/ChatGPT created `member_handoff/cw2_common.py`, three independent model
scripts and individual ZIP starter packages. The shared protocol and five OLS
metrics were checked against the executed main notebook. Candidate experiments and
final testing remain unrun. This is collaboration scaffolding, not completed human
model-owner work; the main notebook configuration was not changed.

Additional assistance — OpenAI Codex/ChatGPT added individual notebook entry points
and cross-platform/Jupyter/Colab instructions, and refreshed the starter ZIPs.
Default notebook execution and ZIP extraction were checked with fresh local Linux
IPython kernels; Windows, macOS and Colab were not directly tested. Candidate fitting
stays disabled by default. Official Colab and IPython documentation informed the
instructions. The main submission notebook and experimental protocol were unchanged.

Additional assistance — At the user's request, OpenAI Codex/ChatGPT shortened the
handoff instructions to notebook UI steps without terminal commands, kept member 2's
instructions in Chinese, and translated members 3 and 4's instructions into English.
The individual ZIPs were refreshed without changing model code or notebook contents.

Model-pool decision — Wenyi explicitly instructed the team to execute the existing
model plan: member 2 owns RandomForestRegressor, member 3 ExtraTreesRegressor, and
member 4 HistGradientBoostingRegressor, with LinearRegression as the reference.
Codex removed provisional model-selection wording from handoff materials, refreshed
the individual packages, and updated the allocation/master notebook model-pool
description. This decision does not imply completed candidate experiments, a final
recommended pipeline, or final contribution-statement agreement by all members.

Additional assistance — Codex clarified that each supplied `.ipynb` is the existing
notebook to edit, and that analysis belongs in its existing Markdown/text cell;
no new notebook or separate TXT/Markdown analysis file is required. Member 2's
instructions remain Chinese; members 3 and 4's instructions remain English.

2026-11-09 — Repository preparation requested by Wenyi: Codex added English editions
of Chinese project, requirements, model and notebook guides; made the main README
and allocation English; retained Chinese originals under `docs/zh/`; added an English
copy alongside member 2's Chinese instructions; and refreshed the handoff archives.
Removed byte-identical extracted-package/image duplicates, generated Python caches,
and the obsolete initial master-notebook generator. Original course material, the
dataset, actual experiment results, and candidate code were retained. No candidate
fitting, final testing, Git initialisation or GitHub publication was performed.

## Change log template

| Date | Name/ID or tool | Actual change/review | File/section | Evidence | AI support, if any |
|---|---|---|---|---|---|
| 2026-11-07 | Codex/ChatGPT | Shared framework, OLS execution, study material | Notebook 1–10; notes | Executed notebook; results CSV/JSON | As recorded above |

Final statement approval: **not yet obtained**. All five members must read and
agree the actual contribution statement before submission.

2026-11-09 — Pre-publication audit requested by Wenyi: Codex checked tracked files,
archives, notebook outputs, Git author metadata, dependencies and standalone execution.
Personal screenshots and the unrelated machine-wide package inventory were excluded
from publication but backed up locally. Home-directory identities were redacted in
saved/future runtime records; numerical experiment evidence was retained. Personal
entries were made to locate the one shared CSV in a Git checkout, as well as their
standalone package CSV. The unpublished initial commit was replaced with the cleaned
snapshot and a GitHub no-reply author address. No GitHub publication was performed.
