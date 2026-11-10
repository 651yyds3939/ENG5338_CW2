# GAS4 CW2 — Task allocation

Execute this model plan: **Linear Regression reference + Random Forest + Extra Trees + Histogram Gradient Boosting.** The coursework brief is authoritative for assessment requirements. Member numbers below supersede the earlier A–E draft.

## Member 1 — Wenyi: shared framework and notebook integration

- Check and load the GAS dataset.
- Implement the shared split, cross-validation and evaluation protocol.
- Reserve the final test period; do not use it for tuning or model selection.
- Implement and evaluate the linear regression reference.
- Provide consistent code interfaces and result formats to all model owners.
- Integrate contributions and ensure the final notebook runs from a fresh kernel and reproduces the results.
- Assemble model-comparison tables and figures.
- Write the common experimental-methods part of the report.

## Member 2 — Kiki: Random Forest Regression

Estimator: `RandomForestRegressor`.

- Train and tune the assigned model using the shared data, folds and metrics.
- Fit preprocessing within each training fold to prevent leakage.
- Record training and validation scores and analyse overfitting.
- Return runnable code, the search grid, best parameters, fold results and a short analysis.
- Write the model's methods and results text.

## Member 3 — Poon (Sirawich Anantapong): Extra Trees Regression

Estimator: `ExtraTreesRegressor`.

- Train, tune and analyse the assigned model.
- Meet the same preprocessing, validation, evidence and reporting requirements as member 2.

## Member 4 — Hansini Devaraja: Histogram Gradient Boosting Regression

Estimator: `HistGradientBoostingRegressor`.

- Train, tune and analyse the assigned model.
- Meet the same preprocessing, validation, evidence and reporting requirements as member 2.

## Member 5 — Sauhandikaa: Computational cost and final testing

- Define and apply one timing methodology.
- Measure all models' training and prediction cost in the same runtime.
- Record hardware, software versions and measurement conditions.
- Once the group fixes the final pipeline and parameters using development evidence and constraints, evaluate that pipeline on the test set once.
- Write computational-cost, final-test and limitations analysis.

## Everyone

- Explain the engineering question, target, and one or two application-based deployment constraints.
- Compare the assigned models and linear reference under the shared protocol.
- Recommend the final pipeline from validation evidence and constraints.
- Share report and presentation work; identify the report editor and slide coordinator.
- Review results and prepare Q&A. Every member should understand the entire notebook.
- Record actual individual contributions and AI tools/use truthfully.
- Agree internal handoff times and the final uploader.

## Working and submission rules

Wenyi maintains the master notebook. Model owners edit their individual experiment files and submit code, outputs and analysis for review; no shared editing of the master notebook is required. With GitHub, use personal branches and pull requests for review and merge.

The agreed model pool is not the final recommended pipeline: that recommendation requires completed comparative experiments. Do not invent missing results or completed contributions. Keep submission-facing notebook explanations in English. Final filename: `ENG5338_CW2_notebook_GAS4.ipynb`.

AI assistance supports tutoring, coding, inspection and documentation; members must review and understand their work. The final contribution statement must reflect actual work and be agreed by all members.

[Chinese source](docs/zh/TASK_ALLOCATION.md) · [Contribution record](notes/contributions_and_ai.md)

## Current handoff

All three model owners have submitted their notebooks and numerical results. Current portable notebooks are under `experiments/`; original starters are preserved in the ignored local backup. Wenyi integrates received files. Member 5 uses `experiments/member5_benchmark.ipynb` to review/measure costs. Final testing awaits group agreement. Group chat file delivery is accepted; GitHub PRs are optional.
