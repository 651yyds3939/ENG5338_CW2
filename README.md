# ENG5338 CW2 — GAS4

Estimate contemporaneous gas-turbine CO from nine ambient/process measurements. Compare Linear Regression with Random Forest, Extra Trees and Histogram Gradient Boosting using one chronological protocol.

## Open these files

- [Master notebook](ENG5338_CW2_notebook_GAS4.ipynb): data checks, supplied-search audit, actual four-model validation, plots, high-CO diagnostics, feasibility and contribution records. Run all cells with a Python kernel from the project root.
- [Member 5 benchmark notebook](experiments/member5_benchmark.ipynb): review or measure all four complete pipelines on one runtime. Enable `RUN_BENCHMARK` to measure; existing integration measurements are not attributed as member 5's work.
- [Chinese integration guide](docs/zh/整合说明与下一步_zh.md): current state, directory map, running instructions and next steps.
- [Task allocation](TASK_ALLOCATION.md) and [contribution/AI log](notes/contributions_and_ai.md).

The three model owners have supplied their notebooks and result archives. Their latest configurations are integrated. Member 3's current version is depth 14, with 400 trees, minimum leaf size 10 and max_features=0.8. The original depth-12 run is retained as history.

## Run and reproduce

**Jupyter / VS Code:** open the whole project folder, select a Python environment with `requirements.lock.txt` installed, open the master notebook, restart its kernel and run all cells. `run_notebook.py` provides the same execution using its own Python interpreter. No CW1 folder is required by the project code. The local verification used an existing Python environment without changing CW1 files.

**Colab:** upload/extract the whole repository ZIP, set the working directory to its extracted project root, then open/run the notebook. Uploading the notebook alone is insufficient because it imports `src/` and reads the shared CSV. Save downloaded outputs before a temporary cloud runtime is discarded. Local Linux fresh-kernel execution is checked; Windows/macOS/Colab are supported by relative paths but have not been directly tested.

Default master execution re-runs five-fold validation of the four selected configurations and saves fresh results. It audits actual member-submitted search tables but does not automatically repeat all parameter searches. Set `RUN_FULL_SEARCHES=True` to repeat the latest supplied grids. Optional switches clearly print whether work ran. Member notebooks under `experiments/` use the same configuration source; there are no second model definitions to keep in sync.

`requirements.lock.txt` records exact package versions for the integration environment. Python, hardware, threads and versions are recorded in `results/development/runtime.json`; benchmark runtime is recorded separately in `results/costs/runtime.json` when measured. Cross-version scores can differ slightly. Reproduce candidate comparisons in one environment.

## Current protocol and boundaries

CO target; inputs AT/AP/AH/AFDP/GTEP/TIT/TAT/TEY/CDP; development 2011–2013, reserved 2014–2015; five expanding folds, gap=24 rows, seed=42; MAE selects parameters. Imputation and OLS scaling fit within each training fold. NOx is excluded as a deployment input. Course CSV and protocol are hash checked.

Project targets: at least 90% of predictions within ±1 mg/m³ and median single-row local prediction latency no greater than 10 ms. These are project engineering assumptions requiring justification, not coursework pass marks or legal requirements. Current candidates do not meet the coverage target. The final recommended model and group decision remain pending.

**Final test remains sealed.** There is no enabled held-out prediction entry. Choose and record one exact pipeline using development performance and costs before evaluating it once. No test-driven retuning or switching. CW1 already evaluated the same years, so describe this as an operationally isolated CW2 hold-out, not historically unseen data.

## Directory map

| Location | Purpose |
|---|---|
| `ENG5338_CW2_notebook_GAS4.ipynb` | Main integrated submission notebook |
| `src/` | Common protocol, latest model construction, validation, diagnostics and cost functions |
| `experiments/` | Portable member 2/3/4 entries and member 5 benchmarking |
| `data/` | One unchanged course CSV |
| `results/submitted/` | Members' numerical search evidence, environments and original HGB figures; versions kept separate |
| `results/development/` | Fresh common-runtime validation, prediction vectors and diagnostic tables |
| `results/costs/` | Common-runtime measurement records, when executed |
| `figures/development/` | Reproducibly generated plots; allocation figure is under `figures/` |
| `notes/` | Member-reported analyses, receipt hashes and living contribution/AI log |
| `docs/coursework/` | Original brief and report templates |
| `docs/en/`, `docs/zh/` | English and Chinese project/study guides; early numerical examples are historical |
| `.local_private/pre_github_update_2026-11-10/` | Local-only backup of superseded starters, outputs and review history |
| `.local_private/submissions/` | Untouched original received files, local only and ignored by Git |

No raw member file has been deleted. Redundant versions are preserved outside the active root. Raw returns include student IDs and local paths and are not automatically staged. Submitted numerical evidence is published separately; original names and hashes are in `notes/received_manifest.json`.

For now, members may send notebook/ZIP files in the group and Wenyi integrates them. GitHub branches/PRs remain available; a lack of Git commits does not imply a lack of model work. The private collaboration repository is `651yyds3939/ENG5338_CW2`. This integration does not commit or push changes.

## Study material

- [Requirements and experiment plan](docs/en/REQUIREMENTS_AND_PLAN.md) · [中文](docs/zh/需求检查与周一讨论_zh.md)
- [Project guide and CW1/CW2 relationship](docs/en/PROJECT_GUIDE.md) · [中文](docs/zh/项目全解读_CW1与CW2对照_zh.md)
- [Model explanations](docs/en/MODEL_GUIDE.md) · [中文](docs/zh/候选模型说明与选型建议_zh.md)
- [Current integration details](docs/en/INTEGRATION.md)

Report and slides are not assembled yet; they follow group agreement and final experiments. Final contribution wording must be reviewed by all members. Dataset: Kaya, Tüfekci and Uzun (2019), *Gas Turbine CO and NOx Emission Data Set*, DOI 10.24432/C5WC95.
