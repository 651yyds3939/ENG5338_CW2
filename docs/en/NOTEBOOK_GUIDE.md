# GAS4 notebook and reproduction

Open [the master notebook](../../ENG5338_CW2_notebook_GAS4.ipynb) from the full project checkout. Its eight code cells have saved execution outputs. The notebook contains nine sections:

1. Runtime, data checks and common protocol.
2. Submitted tuning evidence and selected configurations.
3. Common five-fold validation of OLS, RF, Extra Trees and HGB.
4. Training gaps, chronological performance and high-CO diagnostics.
5. Model-owner interpretation and actual contributions.
6. Member 5 computational costs.
7. Accuracy-first model selection and target comparison.
8. Extra Trees assessment and experiment history.
9. Conclusions, contributions and sources.

## Run the project

Use a Python environment with the packages in [requirements.lock.txt](../../requirements.lock.txt). From the project root:

```sh
python -m pip install -r requirements.lock.txt
python run_notebook.py
```

A fresh notebook kernel executes the common five-fold validation, checks source search records and their saved replays, verifies Member 5 timing samples and loads the saved assessments. `RUN_FULL_SEARCHES=True` repeats the latest candidate grids; the fixed-model replay switch reproduces the saved Extra Trees predictions. Both switches default to False.

For Jupyter or VS Code, select the environment, restart the kernel and run all cells. For Colab, extract the complete project and set its root as the working directory. Keep `src/`, `data/` and `results/` together with the notebook.

## Protocol and evidence

- Dataset: 36,733 rows; development 2011–2013 has 22,191 rows; later assessment 2014–2015 has 14,542 rows.
- Five expanding chronological folds; gap 24 rows; seed 42; one numerical thread; each validation block has 3,698 rows.
- Scores: training and validation MAE, RMSE, R², coverage within ±1 mg/m³ and negative-prediction fraction. MAE selects tuning parameters.
- Original tuning exports: `results/submitted/`; common search replays: `results/search_reproduction/`.
- Common validation and per-row predictions: `results/development/`.
- Member 5 Windows cost samples: `results/member5_local_py310/`; earlier Linux reference measurements: `results/costs/`.
- Original HGB assessment: `results/final/`; revised Extra Trees assessment: `results/final_extra_trees/`.
- Combined document evidence and execution audit: `results/submission/`.

The assessed Extra Trees pipeline has MAE 0.8011 and coverage 73.36%. HGB was assessed earlier on the same 2014–2015 observations; CW1 also used those years. Both records retain their parameters, input hashes and prediction vectors.

## Check existing outputs

```sh
python scripts/verify_integration.py
```

This recalculates metrics from saved prediction vectors, checks model settings, receipt hashes when local originals are present, portable notebook setup and Member 5 timing samples. It checks both saved assessments. Individual model notebooks write reruns to ignored `results/member_runs/`.

[Model guide](MODEL_GUIDE.md) · [Submission guide](SUBMISSION_GUIDE.md) · [Main README](../../README.md)
