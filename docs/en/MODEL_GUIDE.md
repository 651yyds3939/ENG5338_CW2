# GAS4 model comparison

The pipeline predicts contemporaneous CO (mg/m³) from AT, AP, AH, AFDP, GTEP, TIT, TAT, TEY and CDP. Year defines chronological partitions. All four models use median imputation; OLS also uses standardisation. Preprocessing is fitted separately inside each training fold.

## Executed development results

| Model | Training MAE | Validation MAE | Validation RMSE | Coverage within ±1 mg/m³ | Windows single-row latency |
|---|---:|---:|---:|---:|---:|
| OLS | 0.6732 | 0.9073 | 1.6892 | 71.80% | 0.70 ms |
| Random Forest | 0.4140 | 0.7372 | 1.5079 | 81.18% | 27.18 ms |
| Extra Trees | 0.4093 | 0.7226 | 1.4735 | 81.76% | 19.03 ms |
| Histogram Gradient Boosting | 0.4111 | 0.7655 | 1.4657 | 79.15% | 2.86 ms |

Accuracy uses five expanding chronological folds in the shared Linux environment. Member 5 measured costs on one Windows laptop. Numeric sources: [development comparison](../../results/development/comparison.csv) and [Windows timings](../../results/member5_local_py310/comparison.csv).

## Models and selected settings

- OLS fits a linear relation between standardised inputs and CO. It supplies the linear reference.
- Random Forest averages bootstrap-trained regression trees. Selected settings: 600 trees, maximum depth 11, minimum leaf size 20, max_features=0.5 and max_samples=0.9.
- Extra Trees averages trees with randomised split thresholds. Selected settings: 400 trees, maximum depth 14, minimum leaf size 10, max_features=0.8 and bootstrap=False.
- HGB adds histogram-based trees to reduce the remaining loss. Selected settings: 200 iterations, learning_rate=0.05, max_leaf_nodes=15, minimum leaf size 20, L2=1 and early_stopping=False.

All candidate settings and grids come from [model-owner exports](../../results/submitted/). The latest grids contain 3 RF, 27 Extra Trees and 8 HGB configurations. Their 190 CV fits were replayed in the common environment under [search_reproduction](../../results/search_reproduction/).

## Recommendation and assessment

Extra Trees is the accuracy-first recommendation: it has the lowest development MAE and highest development coverage. HGB has the lowest validation RMSE and the fastest nonlinear prediction. The comparison keeps both accuracy and cost visible.

Extra Trees assessment on 2014–2015 gives MAE 0.8011, RMSE 1.3654, R² 0.6111 and coverage 73.36%. HGB was assessed first, giving MAE 0.8998 and coverage 70.00%; the accuracy-first revision then selected Extra Trees from existing development scores and assessed it on the same years. CW1 also used these years. Both saved records are retained. A new future period supplies the next confirmation stage.

For high-CO validation observations above the training-fold 95th percentile, Extra Trees coverage is 26.68% and mean signed error is −1.9672 mg/m³. High-CO examples and temporal variation are priorities for further development. The project coverage target is 90% within ±1 mg/m³. The original 10 ms reference remains in the timing comparison; the current selection prioritises MAE.

[Notebook guide](NOTEBOOK_GUIDE.md) · [Submission guide](SUBMISSION_GUIDE.md) · [Task allocation](../../TASK_ALLOCATION.md)
