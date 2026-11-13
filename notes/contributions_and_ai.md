# Contribution and AI-assistance record

This is a living record, not the final agreed statement. Student IDs remain in original local submissions for members to verify. Historical log entries below describe their dates, not current outstanding files. Proposed ownership is not
evidence of completed human work. Replace placeholders with names and student IDs.

| Member | Assigned responsibility | Actual implementation | Actual writing/review | Notebook location | Evidence/date |
|---|---|---|---|---|---|
| 1 — Wenyi | Framework, OLS, validation and integration | AI-assisted framework available; record actual human review/adaptation | To record | Sections 1–4, 7–8 and integration | Executed shared notebook and results; human evidence to record |
| 2 — Jiaqi Chen (Kiki) | Random Forest | Latest three-setting search, selected parameters and validation plotting supplied | Member analysis received; ChatGPT coding/writing assistance disclosed | Master sections 2–5; member 2 experiment | Original receipt hashes; submitted/member2/latest |
| 3 — Sirawich Anantapong (Poon) | Extra Trees | Initial and latest search, selected pipeline and plot supplied | Member analysis received; Claude assistance disclosed | Master sections 2–5; member 3 experiment | Submitted/member3/run1 and latest |
| 4 — Hansini Devaraja | Histogram gradient boosting | Eight-configuration search, fold metrics, graphs and notebook supplied | Member analysis received; ChatGPT learning/troubleshooting disclosed | Master sections 2–5; member 4 experiment | Submitted/member4/latest |
| 5 — Sauhandikaa | Cost review/measurement and final testing | Independent four-pipeline Windows benchmark and accuracy–cost interpretation supplied | Received benchmark method, interpretation and limitations text | Master sections 6–8; member 5 experiment | Original Member5_Results.zip and results/member5_local_py310 |

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

2026-11-10 — Codex reviewed the raw member 2 RF notebook/starter ZIP and member 4
HGB notebook/results ZIP supplied by Wenyi, plus the provided chat screenshots.
Checked protocol/fold boundaries, exported-score consistency, actual code changes
and contribution/AI explanations. Reproduced member 2's fixed final configuration
on five development folds (not the multi-round search), reran member 4's supplied
eight-setting search and selected folds, and computed a shared training-quantile
high-CO validation diagnostic. Recorded small RF cross-version discrepancies and
missing member-2 result/weighted-experiment artifacts. No final test or master
integration was performed. Raw returns remain unchanged and locally excluded from
Git; privacy-safe review evidence is in `reviews/2026-11-10/`.

### 2026-11-10 — Member 3 received-work review

AI assistance checked the supplied Extra Trees archive, matched protocol and numerical fold boundaries, verified search/summary consistency and reproduced the selected five-fold configuration. All summary metrics match within 1e-12. The full 24-configuration search was not repeated. Added separate review evidence and next-step notes; the master notebook remains unchanged. No final test, commit or push was performed. Member 3's personal notebook is still outstanding.

### 2026-11-10 — Member 2 results ZIP received

AI assistance checked archive integrity, protocol and folds, three search configurations, selected parameters, fold-summary arithmetic and agreement with the previously received notebook. Checked the screenshot's weighted arithmetic without treating it as verified analysis code. Saved review evidence; no further training, final test, master-notebook integration, commit or push occurred.

### 2026-11-10 — Latest Member 3 notebook and results received

AI assistance matched the latest notebook to member3_results (1).zip, verified the 27-configuration search record and protocol, and independently reproduced the selected depth-14 configuration on all five development folds. Updated the review comparison while preserving earlier evidence. Member-written analysis and AI disclosure are present. No final test, master integration, commit or push occurred.

### 2026-11-10 — Comprehensive integration requested by Wenyi

Codex preserved raw returns byte-for-byte under ignored local submissions; organised coursework, starters and historical evidence; extracted submitted numerical records; integrated latest member configurations into shared portable code and master/personal notebooks; retained member analysis and AI disclosures; added same-runtime benchmark entry and Chinese study explanations. Default master execution regenerates selected-configuration development results and figures. Full-grid reruns are explicit optional switches. Final test, final recommendation, report and slides remain pending. Human review and member 5's own measurement/interpretation must be recorded separately. Run completion and exact environment are recorded in result artifacts, not inferred from this log. No Git commit or push is performed by this integration.

Integration execution evidence — All four selected configurations completed chronological validation, each with 18,490 validation predictions. Codex also executed the common four-pipeline reference cost measurement, with three timed full-development fits per model and repeated single/batch predictions. Costs are labelled as Codex reference measurements, not member 5 work. Fresh-kernel master execution, portable bootstrap checks, original-return hashes and saved prediction consistency are checked by the integration verification scripts. Full supplied-grid reruns are not claimed in this integration execution. Final test remains sealed.

### 2026-11-10 — Pre-update cleanup

At Wenyi's request, Codex moved superseded starter packages, baseline-only framework outputs, old audit/review documents and redundant allocation/figure-generation assets out of the upload tree into an ignored local backup. Current code, member numerical searches, development prediction exports, cost samples, course materials and bilingual study guides were retained. Fixed links and the Chinese entry guide. Original member returns remain untouched. No model retuning, final testing, Git commit or GitHub push was performed in this cleanup.


### 2026-11-13 — Submission finalisation commissioned by Wenyi

Wenyi explicitly instructed Codex to complete integration, decision, final testing, report, slides and reproducibility checks. Member 5's received archive was preserved unchanged with its receipt hash; its independent Windows benchmark, environment and interpretation were integrated separately from the older AI reference run. Codex replayed the latest owner grids, executed common selected-configuration validation, recorded HGB as the lowest-validation-MAE candidate within the unchanged 10 ms budget, and withheld deployment approval because no candidate meets the coverage target. The decision lock precedes one authoritative fixed-model CW2 assessment; no test-driven retuning or alternative final-test comparison is authorised by this workflow. Execution artifacts establish completed runs.

Codex generated the report, presentation PDF/editable PPTX, speaking/Q&A notes and supporting reproducibility package from Notebook exports. This final assessment and drafting are not falsely attributed to independently completed Member 5 work or all-member human writing. AI coding, analysis and drafting assistance are disclosed. At Wenyi's request, Member 5's as-yet unknown student ID remains blank. All-member reading/agreement to the contribution statement remains a human requirement and is not fabricated. No Moodle submission, GitHub push, peer evaluation or oral presentation is performed.


### 2026-11-13 — Explicit accuracy-first revision to Extra Trees

After reviewing why HGB had been selected and seeing its assessment result, Wenyi explicitly requested switching to the model with higher predictive accuracy. Codex selected Extra Trees using the already available development-validation MAE/coverage ranking, with the exact unchanged Member 3 settings. The original 10 ms hard gate lacked actual application evidence and is now a descriptive historical reference; the 90% coverage target is unchanged. This is a disclosed post-exposure revision of selection policy, not a preregistered blind choice or unanimous group endorsement.

The original HGB `results/final/` record is retained unchanged. A separate revision lock and secondary Extra Trees assessment are in `results/final_extra_trees/`. The original submission files and source are preserved in the ignored `.local_private/submission_v1_hgb/` backup. Two CW2 models have now been assessed on the same 2014–2015 period, which was also used in CW1. The revised assessment is not independent confirmation and does not meet a strict one-model/one-untouched-test design; further confirmation requires new data. No Extra Trees parameter retuning or subsequent assessment-driven winner selection is performed.

Codex updated and checked the report, slides, master notebook, guides, Q&A notes and reproducibility package. Generated text and assessment work remain AI-assisted under Wenyi's direction, not Member 5's independent work. Member 5 ID and all-member contribution review remain pending. No GitHub push or Moodle upload is performed.


### Student identity update — 2026-11-13

Wenyi supplied all five student IDs and requested seven-digit numeric formatting. The local identity file and generated report now include all five IDs. The report cover and contribution table use the same identity data.
