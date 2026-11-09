# Member 2: Random Forest Regression (Model 1)

**Your model: Random Forest regression (`RandomForestRegressor`).** It averages predictions from decision trees to estimate CO. Tune `n_estimators`, `max_depth` and `min_samples_leaf`.

## Which file to open

The notebook is the existing **`member2_model1.ipynb`** inside this package. Open this file directly.

## How to run

**Jupyter / JupyterLab:** Extract the package, open `member2_model1.ipynb` in that folder and select a Python kernel.

**Google Colab:** Open `member2_model1.ipynb` and upload `GAS4_member2_starter.zip` using the Files panel. The first cell extracts it.

1. Run cells from top to bottom and check package versions. Send missing-package or error messages to Wenyi.
2. Edit the estimator and grid in "Your model and search grid".
3. Set `RUN_EXPERIMENT` to `True` and run the experiment cell.
4. Find "Your analysis and contribution". Double-click that text cell, replace placeholders with your analysis, press `Shift + Enter` to render it, and save.
5. Run the final export cell and download the results ZIP.

## What to return

- Your edited `member2_model1.ipynb`, saved with outputs.
- The exported `member2_results.zip`.

Write the rationale, training/validation gap, limitations, actual contribution and AI use in the notebook's analysis cell.

Edit your model and analysis only. Keep `cw2_common.py`, data, splits and scoring unchanged. Do not evaluate the final hold-out. The `.py` file is an alternative entry; do not edit both entries independently.
