# Member-reported analysis — received 10 November 2026

Historical author text retained for attribution. Current integrated findings are in the master notebook.

## Your analysis and contribution

**Write your analysis here, in this existing Markdown/text cell.** Double-click
this cell, replace the placeholders below with your own text, then press
`Shift + Enter` to render it. Save the notebook with your code, outputs and analysis.
This is a text cell, not a code cell.

- Name / student ID: Sirawich Anantapong / [ID retained in original submission]
- What you actually implemented or changed: I experiment the Extra Trees Regression through Wenyi's shared framework. I tuned the model over three grid searches:

  - Run 1 : n_estimators [200, 400], max_depth [12, 20, None], min_samples_leaf [1, 3, 5, 10]. the best result came from the highest or lowest value I tried, so I wasn't sure if I'd tested far enough so I experiment more.
  - Run 2 : using the first experiment and extended the parameter from simpler trees, with max_depth [6, 8, 10, 12] and min_samples_leaf [10, 20, 40]. None of the new values did better, so the best settings didn’t change.
  - Run 3 : max_features [0.5, 0.8, 1.0], max_depth [11, 12, 14], min_samples_leaf [7, 10, 15]. max_features=0.8 remained the best result, and max_depth moved to 14, which only give a little improvement.

- Why this model and these settings: Extra Trees builds lots of trees and averages them, and each tree pick the split points in random. This makes the predictions more stable and allow the model pick up non-linear patterns between the conditions and CO. Each tree uses all the training data, so it can overfit easily. That's why I focused on max_depth and min_samples_leaf, which control how detailed each tree can get. I added max_features in run 3 so my tuning can compare with the Random Forest. I picked the final settings based on the lowest average validation MAE across the five folds.

- Training versus validation evidence: My final settings were max_depth=14, min_samples_leaf=10, max_features=0.8 and n_estimators=400.
  - The average Training MAE is 0.4093 and the average validation MAE was 0.7226 (SD 0.0866), so there's a gap of 0.3133. This shows some overfitting: the model does worse on later data it hasn't know yet.
  - Validation RMSE was 1.4735 and R square was 0.5955.
  - On average, 81.76% of predictions were within +/- 1 of the real CO value, and the worst fold dropped to 71.42%.
  - Run 3 only improved MAE by 0.0026 compared with runs 1 and 2, which is much smaller than the variation between folds, so more tuning probably don't improve the result anymore.

- Temporal limitations / parameter boundaries / next steps:
  - Results are from 2011–2013 only; 2014–2015 is keep for the final test.
  - when the real CO is high, the model predicts too low, and Almost no dots are above 12, even though the real values go up to 44. This is the main reason coverage stays below 90%.
  - I tested values above and below each final setting, and they all did worse, except n_estimators=400, which was the largest I tried.
  - Changing the settings might not helping anymore. To fix high CO, we might need to give the model more information.

- AI tools used and what for: I used Claude to explain the framework and models and help me understand the results, help me write the plotting graph and helped me with the some grammar wording. all results come from my own runs.
