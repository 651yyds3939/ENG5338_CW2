# Member-reported analysis — received 10 November 2026

Historical author text retained for attribution. Current integrated findings are in the master notebook.


## Analysis and contribution

##### Name : Hansini Devaraja/ Student ID:[ID retained in original submission]
##### 1. What I implemented

I implemented a Histogram Gradient Boosting Regressor (HGBR) using Scikit-learn. The model was integrated into the shared experimental framework using a Pipeline with median imputation.

I performed hyperparameter tuning using GridSearchCV with 5-fold TimeSeriesSplit cross-validation. A total of 8 parameter configurations and 40 cross-validation fits were evaluated.

##### 2. Model selection and hyperparameter settings

Histogram Gradient Boosting was selected because it builds an ensemble of decision trees sequentially, with each new tree attempting to improve the predictions of the previous ensemble.

The hyperparameter search considered:
- Learning rate: 0.05 and 0.1
- Maximum leaf nodes: 15 and 31
- L2 regularisation: 0.0 and 1.0

The best configuration selected by GridSearchCV was:
- Learning rate: 0.05
- Maximum leaf nodes: 15
- L2 regularisation: 1.0

##### 3. Training and validation performance

The model achieved the following results:

| Metric              | Result |
|---------------------|--------|
| Training MAE        | 0.4111 |
| Validation MAE      | 0.7655 |
| Validation RMSE     | 1.4657 |
| Validation R²       | 0.5974 |
| Validation coverage | 79.15% |
| Worst-fold coverage | 66.96% |

The validation MAE is higher than the training MAE, with a difference of 0.3544. This indicates a performance gap and suggests possible overfitting.

The validation MAE varied across the five folds. Fold 1 achieved the lowest MAE (0.5713), while Fold 4 had the highest MAE (0.8869).

Fold 2 recorded the highest RMSE (1.7072), while Fold 4 recorded the lowest RMSE (1.2521).

##### 4. Coverage and limitations

The required coverage threshold was 90%. The average validation coverage was 79.15%, meaning the model did not meet the required threshold overall.

Only Fold 1 achieved coverage above 90%. Fold 4 recorded the lowest coverage at 66.96%.

The variation in performance across the time-series folds suggests that the model may not generalise consistently across different time periods.

Further investigation could explore alternative hyperparameter ranges, stronger regularisation and different model configurations. Any additional tuning should follow the same shared evaluation protocol.

##### 5. AI tools used

ChatGPT was used as a learning medium to understand the HGBR algorithm, explain the experimental framework and troubleshoot implementation issues. The implementation was executed and tested locally using the provided coursework framework.
