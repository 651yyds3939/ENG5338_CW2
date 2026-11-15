# ENG5338 CW2 — GAS4

Estimate contemporaneous gas-turbine CO (mg/m³) from nine ambient/process measurements. Compare OLS, Random Forest, Extra Trees and Histogram Gradient Boosting under one chronological protocol.

## Start here

- [Main notebook](ENG5338_CW2_notebook_GAS4.ipynb): executed data checks, tuning evidence, four-model validation, timing comparison, model selection and assessments.
- [Notebook guide](docs/en/NOTEBOOK_GUIDE.md): running instructions and evidence map.
- [Model comparison](docs/en/MODEL_GUIDE.md): settings, measured accuracy and costs.
- [Submission guide](docs/en/SUBMISSION_GUIDE.md): course files and report template.
- [Task allocation](TASK_ALLOCATION.md) and [contributions/AI use](notes/contributions_and_ai.md).

## Run

Keep the complete project together. In a Python environment, run from the project root:

```sh
python -m pip install -r requirements.lock.txt
python run_notebook.py
```

For Jupyter or VS Code, select that environment, open the main notebook, restart the kernel and run all cells. For Colab, extract the whole project and use its root as the working directory.

Default execution repeats five-fold validation of the four selected configurations, checks submitted searches and saved replays, verifies Member 5 timings, and loads the saved assessments. `RUN_FULL_SEARCHES=True` repeats the latest 38 supplied configurations (190 CV fits). The fixed-model replay switch reproduces the saved Extra Trees predictions. Both switches default to False.

Check existing results with `python scripts/verify_integration.py`. Numerical runtime and versions are in results/development/runtime.json; Member 5's Windows environment is in results/member5_local_py310/runtime.json.

## Protocol and results

CO is the target; inputs are AT, AP, AH, AFDP, GTEP, TIT, TAT, TEY and CDP. Development uses 2011–2013 (22,191 rows); later assessment uses 2014–2015 (14,542 rows). Five expanding folds use a 24-row gap, seed 42 and one numerical thread. MAE selects parameters. Each fold fits its own median imputer; OLS also fits a scaler.

**Current recommendation: Extra Trees**, with 400 trees, depth 14, minimum leaf size 10 and max_features=0.8. Development-validation MAE is 0.7226 mg/m³ and coverage is 81.76% within ±1 mg/m³. Member 5 measured 19.03 ms median single-row prediction on Windows. The project coverage target is 90%; the original 10 ms reference remains in the cost comparison. Current selection prioritises MAE.

HGB was assessed first: MAE 0.8998 and coverage 70.00%. Wenyi then requested accuracy-first selection from the existing development ranking. Extra Trees assessment on the same 2014–2015 observations gives MAE 0.8011, RMSE 1.3654, R² 0.6111 and coverage 73.36%. CW1 also used those years. Both assessment records retain their input snapshots, hashes and predictions. A new future period supplies the next confirmation stage.

## Repository layout

| Location | Purpose |
|---|---|
| src/ | Shared protocol, model construction, validation, diagnostics and cost functions |
| experiments/ | Member 2/3/4 model entries and Member 5 benchmark notebook |
| data/ | Unchanged course CSV |
| results/submitted/ | Latest model-owner search exports and settings |
| results/search_reproduction/ | Common-runtime search replays |
| results/development/ | Common validation metrics, per-row predictions and diagnostics |
| results/member5_local_py310/ | Member 5 Windows timing samples and runtime |
| results/final/ | Original HGB decision and assessment |
| results/final_extra_trees/ | Accuracy-first Extra Trees decision and assessment |
| results/submission/ | Combined comparison and notebook execution audit |
| figures/submission/ | Three report/presentation figures |
| notes/ | Attributed member analysis, receipt hashes and contribution record |
| docs/ | Course brief/templates and concise English guides |
| scripts/verify_integration.py | Recalculate metrics and check experiment records |

Course PDFs, editable drafts and group-review packages are shared separately. Local study material, document-generation tools, generated intermediate exports and archived experiments are ignored by Git. Member notebook reruns write to ignored results/member_runs/; optional searches write to results/search_reruns/.

Dataset: Kaya, Tüfekci and Uzun (2019), *Gas Turbine CO and NOx Emission Data Set*, DOI [10.24432/C5WC95](https://doi.org/10.24432/C5WC95). Course CSV SHA-256: 6295ecd391e757ab5e029bdb54aee607887374861f656a26281b5a0e4e524b85.
