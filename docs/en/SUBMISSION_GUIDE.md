# GAS4 course submission

Upload one group set using these filenames:

- ENG5338_CW2_report_GAS4.pdf
- ENG5338_CW2_presentation_GAS4.pdf
- ENG5338_CW2_notebook_GAS4.ipynb

## Report and presentation

The [course brief](../coursework/coursework%20brief2.pdf) requires the report to follow the supplied template: [LaTeX source](../coursework/template_cw2_ENG5.tex) and [template PDF](../coursework/template_cw2_ENG5.pdf). The report has four sections: Engineering Question & Constraints; Experimental Design; Comparative Analysis; Recommended Pipeline. The limit is eight main pages plus a one-page appendix; the contribution statement is counted separately. Put the repository link on the first page.

The group maintains the final report in the official LaTeX template and the slides separately. Use the same figures, model settings and numbers in the report, slides and notebook. Three shared figures are in figures/submission/: temporal_validation.png, accuracy_cost.png and final_diagnostics.png.

Plan a 10-minute presentation followed by 10 minutes of Q&A. Explain each member's distinctive contribution. Every member prepares questions on the entire notebook. Confirm the contribution statement and complete Moodle peer evaluation.

Course files and editable drafts are shared in the group. The local submission/ directory holds Wenyi's draft package and is ignored by Git. Use the group's reviewed report and slides for the final upload. Check the Moodle deadline and save the submission receipt.

## Results to align

Extra Trees is the accuracy-first recommendation. Development MAE is 0.7226 mg/m³ and coverage 81.76%; Member 5 Windows single-row latency is 19.03 ms. The 2014–2015 assessment gives MAE 0.8011 mg/m³, RMSE 1.3654 mg/m³, R² 0.6111 and coverage 73.36%. The project coverage target is 90% within ±1 mg/m³.

HGB was assessed earlier: MAE 0.8998 and coverage 70.00%. The accuracy-first revision then chose Extra Trees using existing development scores and assessed the same 2014–2015 observations. CW1 also used these years. Both saved assessment records retain their parameters, predictions and input hashes. A new future period supplies the next confirmation stage.

## Reproduction

Run `python run_notebook.py` with requirements.lock.txt installed, from the complete project root. Use `python scripts/verify_integration.py` to check saved metrics, settings, portable member entries and timing samples. See [the notebook guide](NOTEBOOK_GUIDE.md).
