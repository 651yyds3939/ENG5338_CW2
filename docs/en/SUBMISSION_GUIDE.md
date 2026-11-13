# GAS4 submission guide

Upload one group set:

- `ENG5338_CW2_report_GAS4.pdf`
- `ENG5338_CW2_presentation_GAS4.pdf`
- `ENG5338_CW2_notebook_GAS4.ipynb`

The local `submission/` directory contains these files, editable PowerPoint, presenter/Q&A notes, report source and a complete reproducibility ZIP. It is excluded from Git because it contains student IDs.

## Selected pipeline

Extra Trees: median imputation, 400 trees, depth 14, minimum leaf size 10, max_features=0.8, bootstrap=False, seed 42 and one worker. Development-validation MAE is 0.7226 mg/m³, coverage 81.76%; Windows single-row latency is 19.03 ms. The project coverage target is 90% within ±1 mg/m³.

## Experiment history

HGB was assessed first, giving MAE 0.8998 and coverage 70.00%. After reviewing it, Wenyi prioritised predictive MAE over the original 10 ms gate and chose Extra Trees from the existing development ranking. Extra Trees was assessed on the same 2014–2015 observations: MAE 0.8011 and coverage 73.36%. CW1 also used these years. Both model settings and assessment records are retained under `results/final/` and `results/final_extra_trees/`. A new future period supplies the next confirmation stage.

## Reproduction and document build

Use a Python environment with `requirements.lock.txt`, then run `python run_notebook.py` from the project root. Keep `src/`, data and result evidence together. The default runs common validation and verifies searches, timing samples and saved assessments. Grid and fixed-model replay switches are available. `scripts/verify_integration.py` checks the numerical exports.

Build documents with `scripts/build_submission.py` and optional `requirements.build.txt`; the local identity file supplies names/IDs. `scripts/package_submission.py` copies the notebook and creates the supporting archive. The report follows the course's four sections, A4, 2.5 cm margins and 11 pt body. It has seven main pages, one appendix and a contribution page. Slides contain 11 pages with a 10-minute speaking plan.

## Upload preparation

All five student IDs are filled in using seven digits. All members should confirm the contribution statement, review the whole notebook and practise Q&A. Upload one group set and complete the Moodle peer evaluation. Publication status: local changes ready for GitHub push and Moodle upload. Use the live Moodle page for the deadline and submission receipt.
