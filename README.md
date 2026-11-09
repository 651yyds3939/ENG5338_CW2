# ENG5338 CW2 — GAS4

Predict contemporaneous gas-turbine CO concentration from nine ambient/process measurements, compare three tuned scikit-learn models with linear regression, and recommend a pipeline using predictive performance, deployment constraints and computational cost.

**The model allocation is fixed:** member 1 (Wenyi) maintains the framework and linear reference; member 2 (Kiki) owns Random Forest; member 3 owns Extra Trees; member 4 owns histogram gradient boosting; member 5 owns common cost measurement and final testing. See [task allocation](TASK_ALLOCATION.md).

## Start here

| Purpose | English | Chinese |
|---|---|---|
| Project, principles, workflow, deliverables, CW1/CW2 comparison | [Project guide](docs/en/PROJECT_GUIDE.md) | [项目全解读](docs/zh/项目全解读_CW1与CW2对照_zh.md) |
| Coursework requirements and experiment plan | [Requirements and plan](docs/en/REQUIREMENTS_AND_PLAN.md) | [需求与实验设计](docs/zh/需求检查与周一讨论_zh.md) |
| Notebook sections, measured baseline and Q&A | [Notebook guide](docs/en/NOTEBOOK_GUIDE.md) | [Notebook 解读](docs/zh/Notebook解读与问答_zh.md) |
| Model principles, strengths and limitations | [Model guide](docs/en/MODEL_GUIDE.md) | [模型说明](docs/zh/候选模型说明与选型建议_zh.md) |
| Team responsibilities | [Task allocation](TASK_ALLOCATION.md) | [中文分工](docs/zh/TASK_ALLOCATION.md) |
| Model-owner starter packages | [Handoff](member_handoff/README.md) | [交接说明](member_handoff/交接说明.md) |

The original Chinese overview is retained [here](docs/zh/README.md). Early study notes include alternative model proposals; the task allocation above is the current execution plan.

## Current evidence

The [master notebook](ENG5338_CW2_notebook_GAS4.ipynb) has completed a fresh-kernel run of its 15 code cells without errors. Data checks, chronological folds, linear-reference validation and linear-reference cost measurements have run. Candidate switches remain disabled in the checked-in starters. Member 2 has reported progress in chat; their experimental artifacts have not yet been integrated or verified here.

| Linear reference, development CV | Recorded value |
|---|---:|
| Mean validation MAE | 0.907319 mg/m³ |
| Mean validation RMSE | 1.689245 mg/m³ |
| Coverage within ±1 mg/m³ | 71.80% |
| Median single-row prediction | 1.024 ms on the recorded runtime |

Extended diagnostics, scalability, final model selection and the CW2 held-out evaluation are not complete. No final report or presentation has been generated. Run state is recorded in [experiment status](results/experiment_status.csv); machine-readable outputs are in `results/`.

## Working together

Model owners edit their own files under `member_handoff/`, not the master notebook. Each owner returns the edited notebook with outputs, result files and analysis written in the existing analysis cell. Wenyi reviews and integrates them. The `.py` entry is an alternative to the personal notebook; do not maintain two conflicting model definitions.

Individual starter ZIPs are under `member_handoff/packages/`. The master notebook remains the final reproducibility entry point. On GitHub, work on personal branches, open pull requests and let Wenyi review before merging. This CW2 folder is a local Git repository on branch `main`; it has not been connected or published to GitHub. The sibling CW1 folder is outside this repository.

## Run

**Jupyter/JupyterLab:** open the notebook with a Python kernel that has the recorded dependencies. Start a fresh kernel and run cells in order.

**Colab model owners:** follow the short instructions in the personal package; upload the personal notebook and its matching ZIP. Save/download results before the runtime is recycled.

For a scripted master-notebook run, use a Python environment with `requirements.lock.txt` installed and run `run_notebook.py` from this folder. That script uses its own interpreter as the kernel, without globally registering a kernelspec. The first measured run used the existing sibling CW1 environment; CW1 files were not changed, and collaborators do not need the CW1 folder. Direct dependency versions are in `requirements.lock.txt`; hardware, Python/package versions and thread pools are recorded in [runtime.json](results/runtime.json). Home-directory prefixes are redacted as `<home>`. The original machine-wide package inventory included unrelated software and is retained only in an ignored local backup. Identical builds may not install on every platform.

In a Git checkout, personal notebooks locate the shared CSV in `data/`; standalone starter ZIPs include their own identical CSV. Both routes use the same data hash and numerical protocol.

## Shared protocol and hold-out

Current numerical configuration: CO target, nine inputs, development years 2011–2013, reserved years 2014–2015, five expanding time folds, 24-row gap, seed 42, MAE tuning. The measured coverage and latency budgets are engineering assumptions: they require application justification, not a claim of regulatory authority. All candidates must be rerun together if the numerical protocol changes.

`data/gas-turbine-emissions.csv` is an unchanged, SHA-256-verified copy of the course CSV. Structural checks read the full file; distribution analysis and model evaluation use development data only. No held-out prediction call exists in the current framework. The future final-test step requires a fixed model/parameter record and repeat-execution protection.

**Historical exposure:** CW1 already evaluated the same 2014–2015 period. It is isolated during CW2 development, but cannot be described as historically unseen. Do not use CW1 test rankings to select CW2 models.

## Repository contents

- `ENG5338_CW2_notebook_GAS4.ipynb`: master experiment and submission notebook.
- `member_handoff/`: shared model-owner module, personal entries, instructions and ZIPs.
- `data/`: course CSV; `results/`: genuine recorded experiment outputs.
- `docs/en/` and `docs/zh/`: English editions and retained Chinese study notes.
- `notes/contributions_and_ai.md`: actual contribution and AI-use record.
- `figures/`: allocation figure sources and Chinese figure; the shareable English figure is [at the root](GAS4_Team_Task_Allocation_EN.png).
- Original brief/template files remain at the root. The personal Moodle screenshot and machine-wide package inventory are local-only; they are not part of the published repository.

Do not regenerate or overwrite another member's edited notebook. `member_handoff/build_browser_starters.py` is for initial starter generation; the checked-in notebooks are the files members actually edit.

Dataset: Kaya, H., Tüfekci, P. and Uzun, E. (2019), *Gas Turbine CO and NOx Emission Data Set*, UCI Machine Learning Repository, DOI: 10.24432/C5WC95. Use the course-supplied CSV.

The repository retains member display names for allocation and contribution attribution. The intended publication is a private group repository; course materials are not a claim of permission to redistribute them publicly. See [publication audit](docs/PUBLICATION_AUDIT.md).
