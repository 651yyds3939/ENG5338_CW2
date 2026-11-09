# Member 3: Extra Trees Regression (Model 2)

**Your model: Extra Trees regression (`ExtraTreesRegressor`).**
It averages predictions from trees with randomized split thresholds to estimate CO. Tune `n_estimators`, `max_depth` and `min_samples_leaf`.

## Which file to open

**The notebook is the existing `member3_model2.ipynb` inside this package. Open it directly. Do not create a new notebook, TXT or Markdown file.**

## How to run

**Jupyter / JupyterLab:** Extract the package, open `member3_model2.ipynb` in that folder and select a Python kernel.

**Google Colab:** Open `member3_model2.ipynb` and upload `GAS4_member3_starter.zip` using the Files panel. The first cell extracts it.

1. Run cells from top to bottom and check package versions. Send any missing-package or error messages to Wenyi.
2. Edit the estimator and parameter grid in "Your model and search grid".
3. Set `RUN_EXPERIMENT` to `True` and run the experiment cell.
4. Find "Your analysis and contribution". Double-click that text cell and replace the placeholders with your analysis. Press `Shift + Enter` to render it, then save the notebook.
5. Run the final export cell and download the result ZIP.

## What to return

- Your edited `member3_model2.ipynb`, saved with outputs.
- The exported `member3_results.zip`.
Write your analysis directly in the notebook's "Your analysis and contribution" text cell: model rationale, training/validation gaps, limitations, actual contributions and AI use.

Edit your model and analysis only. Keep `cw2_common.py`, data, splits and scoring unchanged. Your assigned model is Extra Trees regression. Do not evaluate the final hold-out.

Use the notebook; the `.py` file is an alternative entry, so you do not need to edit both.
