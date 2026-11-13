# ENG5338 CW2 — GAS4

Estimate contemporaneous gas-turbine CO from nine ambient/process measurements. Compare Linear Regression with Random Forest, Extra Trees and Histogram Gradient Boosting using one chronological protocol.

## Submission and finalisation

The local `submission/` directory contains the course report PDF, presentation PDF and executed notebook, plus editable slides, presenter/Q&A notes and a complete reproducibility ZIP. It is ignored by Git because the report contains student IDs. See [submission instructions](docs/en/SUBMISSION_GUIDE.md) or [中文提交说明](docs/zh/提交与答辩说明_zh.md). All five student IDs are filled in using seven digits; all members must review the contribution statement before upload. Publication status: local changes await GitHub push and Moodle upload.

## Open these files

- [Master notebook](ENG5338_CW2_notebook_GAS4.ipynb): data checks, tuning/replay audit, actual four-model validation, Member 5 timings, feasibility, locked final assessment and contribution records. Run all cells with a Python kernel from the project root.
- [Member 5 benchmark notebook](experiments/member5_benchmark.ipynb): received Member 5 notebook, with independently measured Windows costs and the member's interpretation. Saved measurements are under `results/member5_local_py310/`; earlier integration measurements are kept separately.
- [Chinese integration guide](docs/zh/整合说明与下一步_zh.md): current state, directory map, running instructions and next steps.
- [Task allocation](TASK_ALLOCATION.md) and [contribution/AI log](notes/contributions_and_ai.md).

The three model owners have supplied their notebooks and result archives. Their latest configurations are integrated. Member 3's current version is depth 14, with 400 trees, minimum leaf size 10 and max_features=0.8. The original depth-12 run is retained as history.

## Run and reproduce

**Jupyter / VS Code:** open the whole project folder, select a Python environment with `requirements.lock.txt` installed, open the master notebook, restart its kernel and run all cells. `run_notebook.py` provides the same execution using its own Python interpreter. All required project assets are included in the reproducibility ZIP.

**Colab:** upload/extract the whole repository ZIP, set the working directory to its extracted project root, then open/run the notebook. Uploading the notebook alone is insufficient because it imports `src/` and reads the shared CSV. Save downloaded outputs before a temporary cloud runtime is discarded. The master notebook has been executed in a fresh Linux kernel; Member 5 supplied the Windows benchmark.

Default master execution re-runs five-fold validation of the four selected configurations and saves fresh results. It verifies the member-submitted searches and their recorded replays. Set `RUN_FULL_SEARCHES=True` to repeat the latest supplied grids. Optional switches clearly print whether work ran. Member notebooks under `experiments/` use the same configuration source; all model definitions come from the saved owner settings.

`requirements.lock.txt` records exact package versions for the integration environment. Python, hardware, threads and versions are recorded in `results/development/runtime.json`; the reported Member 5 benchmark runtime is recorded separately in `results/member5_local_py310/runtime.json`. Cross-version scores can differ slightly. Reproduce candidate comparisons in one environment.

## Current protocol and boundaries

CO target; inputs AT/AP/AH/AFDP/GTEP/TIT/TAT/TEY/CDP; development 2011–2013, reserved 2014–2015; five expanding folds, gap=24 rows, seed=42; MAE selects parameters. Imputation and OLS scaling fit within each training fold. NOx is excluded as a deployment input. Course CSV and protocol are hash checked.

**Recommended pipeline: Extra Trees**, with development-validation MAE 0.7226 mg/m³ and coverage 81.76%. Median single-row prediction is 19.03 ms on Member 5's Windows laptop. The project target is ≥90% within ±1 mg/m³. The final comparison prioritises MAE and reports computational cost alongside accuracy.

**Assessment history:** HGB was assessed first (MAE 0.8998, coverage 70.00%). After reviewing that result, Wenyi prioritised predictive MAE over the original 10 ms gate and selected Extra Trees from the existing development ranking. Extra Trees was assessed on the same 2014–2015 observations (MAE 0.8011, coverage 73.36%). CW1 also used those years. The two records are stored under `results/final/` and `results/final_extra_trees/`. A new future period supplies the next confirmation stage.

## Directory map

| Location | Purpose |
|---|---|
| `ENG5338_CW2_notebook_GAS4.ipynb` | Main integrated submission notebook |
| `src/` | Common protocol, latest model construction, validation, diagnostics and cost functions |
| `experiments/` | Portable member 2/3/4 entries and member 5 benchmarking |
| `data/` | One unchanged course CSV |
| `results/submitted/` | Members' numerical search evidence and environments; versions kept separate |
| `results/development/` | Fresh common-runtime validation, prediction vectors and diagnostic tables |
| `results/costs/` | Earlier Linux reference measurements, kept separate |
| `results/member5_local_py310/` | Member 5 independent Windows timings, raw samples and environment |
| `results/search_reproduction/` | Executed common-runtime replays of the three latest tuning grids |
| `results/final/` | Original HGB lock and assessment, preserved unchanged as history |
| `results/final_extra_trees/` | Accuracy-first decision revision and secondary Extra Trees assessment |
| `results/submission/` | Combined tables, document evidence and notebook execution audit |
| `submission/` | Local-only report/slides/notebook and supporting upload files |
| `figures/development/` | Reproducibly generated plots; allocation figure is under `figures/` |
| `notes/` | Member-reported analyses, receipt hashes and living contribution/AI log |
| `docs/coursework/` | Original brief and report templates |
| `docs/en/`, `docs/zh/` | English and Chinese project/study guides; early numerical examples are historical |
| `.local_private/pre_github_update_2026-11-10/` | Local-only backup of superseded starters, outputs and review history |
| `.local_private/submissions/` | Untouched original received files, local only and ignored by Git |

Original member files are archived locally. Redundant versions are preserved outside the active root. Raw returns include student IDs and local paths and are kept in ignored local storage. Submitted numerical evidence is published separately; original names and hashes are in `notes/received_manifest.json`.

For now, members may send notebook/ZIP files in the group and Wenyi integrates them. GitHub branches/PRs remain available; received files document the members’ model work. The public collaboration repository is `651yyds3939/ENG5338_CW2`. GitHub publication awaits a local commit and push.

## Study material

- [Requirements and experiment plan](docs/en/REQUIREMENTS_AND_PLAN.md) · [中文](docs/zh/需求检查与周一讨论_zh.md)
- [Project guide and CW1/CW2 relationship](docs/en/PROJECT_GUIDE.md) · [中文](docs/zh/项目全解读_CW1与CW2对照_zh.md)
- [Model explanations](docs/en/MODEL_GUIDE.md) · [中文](docs/zh/候选模型说明与选型建议_zh.md)
- [Current integration details](docs/en/INTEGRATION.md)

Report and slides are built from verified Notebook exports using `scripts/build_submission.py` (optional document dependencies in `requirements.build.txt`). `scripts/package_submission.py` copies the executed Notebook and packages supporting files. Student identity data is held only in the ignored local identity file. Final contribution wording must be reviewed by all members. Dataset: Kaya, Tüfekci and Uzun (2019), *Gas Turbine CO and NOx Emission Data Set*, DOI 10.24432/C5WC95.
