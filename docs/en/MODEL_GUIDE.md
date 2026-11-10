# GAS4: model principles, strengths and selection rationale

> Status note: this study document records the earlier design/framework stage. Current integrated code, results and directory locations are described in [the integration guide](INTEGRATION.md) and the root README.

English edition of the [Chinese model guide](../zh/候选模型说明与选型建议_zh.md), prepared for group discussion and Q&A.

**Execution plan:** member 2 uses Random Forest, member 3 Extra Trees, and member 4 histogram gradient boosting, alongside the linear reference. Alternative methods below are background material, not a change to this allocation. Only the linear-reference results have been verified in the repository; candidate advantages are hypotheses to test, not measured rankings.

## 1. The prediction problem

The current experiment estimates contemporaneous CO concentration from nine ambient and process measurements. It is regression: the output is a number, not a class. The course permits CO or NOx as the target, but prohibits TEY as the target. NOx is excluded as an input so that the proposed CO virtual sensor does not require a second pollutant analyser. This is not a one-hour-ahead forecast.

Development data have correlated process variables, near-zero CO and a long upper tail. A useful comparison therefore asks whether models capture nonlinear interactions, generalise to later periods, handle large errors, and justify their computational cost.

## 2. Comparison at a glance

This table describes model behaviour, not measured performance on GAS4.

| Model | Intuition | Strength | Limitation |
|---|---|---|---|
| Linear regression | Add weighted sensor readings | Simple, fast, explainable | Limited functional form |
| Ridge | Penalise excessively large linear weights | Helps with correlated inputs | Still linear in the original features |
| Quadratic features + Ridge | Add squares/products, then regularise | Simple curvature and interactions | Limited higher-order structure; risky extrapolation |
| Decision tree | Follow a sequence of operating-condition questions | Intuitive and nonlinear | Unstable; can memorise training data |
| Random Forest | Average predictions from different trees | Nonlinear, often more stable than one tree | Size, latency and interpretation cost |
| Extra Trees | Average trees with more random thresholds | Alternative bias/variance and cost trade-off | Can miss fine boundaries |
| Histogram gradient boosting | Sequentially improve previous predictions | Flexible model for tabular data | Interacting hyperparameters |
| SVR | Fit a controlled-complexity surface with an error tube | Smooth nonlinear relationships | Scaling and potentially expensive tuning |

## 3. Linear regression: a weighted formula

A simple view is:

```text
Predicted CO = intercept + temperature weight × temperature
                        + pressure weight × pressure + ...
```

The model learns weights. A coefficient describes a conditional association, not a physical causal effect. The advantages are low computational cost, a small parameter set and an understandable reference. A more complex model must offer enough benefit to justify its extra cost.

Ordinary linear regression does not automatically express changing effects or interactions. For example, the effect of pressure might differ between low- and high-temperature operation. Correlated inputs can also make individual coefficients unstable: several different weight combinations can produce similar predictions.

[Official linear-model guide](https://scikit-learn.org/stable/modules/linear_model.html).

**Our role for it:** a common reference. Its recorded mean chronological validation MAE is 0.9073 mg/m³. Candidates must be compared using the same protocol, rather than unrelated historical scores.

## 4. Ridge and quadratic Ridge

### What Ridge changes

Two pressure measurements may contain almost the same information. OLS can assign large positive and negative coefficients that cancel. Ridge adds a penalty for large weights, balancing prediction fit against coefficient magnitude.

`alpha` controls the penalty:

- Too small: little restriction, approaching OLS.
- Too large: useful effects may be suppressed.
- Choose the strength with development cross-validation.

Ridge alone stabilises a linear model; it does not automatically learn nonlinear relationships.

### What quadratic features add

Add terms such as temperature squared, pressure squared and temperature × pressure. Squares express curvature; products express interactions. The prediction is nonlinear in the original readings but remains linear in the expanded-feature coefficients.

Nine inputs expanded to all degree-one and degree-two terms without a bias column produce **54 features**.

**Strengths:** builds on CW1 knowledge; makes the extra relationships explicit; offers a clear experiment on complexity versus benefit.

**Limitations:** second-order terms cannot represent every operating regime; expanded terms can remain correlated; scaling and regularisation matter. Outside the historical range, square terms can grow quickly. Being mathematically able to extrapolate does not establish engineering reliability.

[Official Ridge and polynomial-regression guide](https://scikit-learn.org/stable/modules/linear_model.html).

The original discussion suggested quadratic Ridge as an alternative to Extra Trees for greater methodological diversity. The group is executing the fixed three-tree-model plan instead; no replacement is implied here.

## 5. A single decision tree: a flowchart of conditions

A tree asks learned questions:

```text
Is inlet temperature below a learned threshold?
├─ Yes: inspect exhaust pressure
└─ No: inspect energy yield
```

It eventually reaches a leaf and estimates CO using the training records in that leaf. These are illustrative questions, not fitted GAS4 rules.

**Strengths:** no need to prescribe a straight-line relationship; interactions emerge naturally; a shallow tree can be drawn and explained.

**Limitations:** deep trees can memorise small groups; small changes in data can change the structure; predictions are step-like; extrapolation beyond historical regimes is limited.

| Parameter | Meaning |
|---|---|
| `max_depth` | Maximum number of successive decision levels |
| `min_samples_leaf` | Minimum records in a final group |

[Official decision-tree guide](https://scikit-learn.org/stable/modules/tree.html).

For this coursework a single tree is useful background, while ensembles deserve priority among the main candidates.

## 6. Random Forest: average different trees

Many trees independently predict the same record. If three example predictions are 1.8, 2.2 and 2.0, their average is 2.0 mg/m³. This is numerical averaging for regression.

Random sampling of records and random candidate-feature subsets encourage different trees to make different errors.

**Strengths:** learns nonlinear relationships and interactions; averaging generally improves stability relative to a single tree; standardisation is usually unnecessary; tuning parameters are relatively understandable.

**Limitations:** many deep trees can require substantial memory and inference work. A whole forest is less directly interpretable than a formula or shallow tree. It does not reliably project new trends far outside training conditions. Rare high-CO regimes may be pulled towards common values by leaf and ensemble averaging; verify that using validation errors rather than assuming it.

| Parameter | Purpose |
|---|---|
| `n_estimators` | Number of trees; adds cost, with diminishing predictive benefit |
| `max_depth` | Complexity of each tree |
| `min_samples_leaf` | Prevent overly specific rules for tiny groups |
| `max_features` | Candidate inputs per split; affects diversity |

More trees do **not** automatically mean more overfitting. Depth and leaf-size controls are more direct complexity controls.

[Official RandomForestRegressor documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html).

**Assigned owner:** member 2, Kiki. The experiment tests whether nonlinear averaging improves later-period predictions over the linear reference.

## 7. Extra Trees: additional randomisation

Both Extra Trees and Random Forest average trees. Random Forest searches for good thresholds among candidate features; Extra Trees generates random thresholds and chooses among those candidate splits.

Under scikit-learn defaults, Random Forest uses bootstrap sampling, while Extra Trees uses the full training sample. The report must describe the settings actually used, not assume defaults after parameters change.

**Strengths:** more diverse trees; less threshold-search work can reduce fitting cost; similar interfaces facilitate peer review and controlled comparisons.

**Limitations:** random thresholds can miss fine boundaries. It is not guaranteed to be faster or more accurate. Its methodology is closer to Random Forest than quadratic Ridge would be; it also shares forest limitations around size, interpretation and extrapolation.

[Official ExtraTreesRegressor documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html).

**Assigned owner:** member 3. The key question is whether extra randomisation improves validation or cost under the common protocol.

## 8. Histogram gradient boosting: successive corrections

Forest trees mainly learn separately and are averaged. Boosting builds models in sequence. Under squared-error training, an intuitive description is:

1. Produce an initial prediction.
2. Identify over- and underestimation.
3. Fit another tree to improve those errors.
4. Repeat with controlled updates.

An illustrative sequence is 2.0 + 0.4 − 0.1 = 2.3. These numbers are not experiment results.

Histogram binning places continuous readings into a finite set of intervals, reducing the split positions considered.

**Strengths:** progressively learns complex nonlinear structure; worth testing on a tabular dataset of this size; usually does not need standardisation; provides leaf-complexity and L2 controls.

**Limitations:** parameter interactions make tuning and explanation harder. Too many or overly strong updates can chase training noise. Rare emission regimes and future operating shifts remain difficult.

| Parameter | Meaning |
|---|---|
| `learning_rate` | Size of each update |
| `max_iter` | Number of boosting iterations |
| `max_leaf_nodes` | Complexity of each correction tree |
| `l2_regularization` | Restrict overly strong leaf updates |

Internal early-stopping validation needs attention in a chronological experiment. Our configuration disables automatic early stopping and uses the common time folds.

[Ensemble principles](https://scikit-learn.org/stable/modules/ensemble.html) · [Official HGB estimator](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html).

**Assigned owner:** member 4. This gives a clear averaging-versus-sequential-improvement comparison with the forests.

## 9. SVR: an error tube and controlled complexity

Support Vector Regression balances errors outside a tolerance tube against model complexity. Small errors inside the tube are not penalised by its epsilon-insensitive loss. An RBF kernel allows nonlinear relationships.

**Strengths:** a smooth nonlinear alternative with regularisation; methodologically different from trees.

**Limitations:** feature scaling is important; `C`, `gamma` and `epsilon` interact. Kernel SVR training cost grows rapidly with sample size; approximately 22,000 development rows multiplied by configurations and folds can make tuning expensive.

| Parameter | Intuition |
|---|---|
| `C` | Emphasis on training errors relative to complexity restriction |
| `gamma` | How local each training point's influence is |
| `epsilon` | Width of the training tolerance tube |

**`epsilon=1` does not guarantee errors within ±1.** Coverage must still be measured.

[Official SVR documentation](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html).

SVR is useful background for a member interested in kernels, but is not in the assigned pool.

## 10. Other possible methods

**KNN regression** finds similar historical conditions and averages their targets, optionally weighted by distance. It is intuitive and locally nonlinear, but needs scaling, retains training records for prediction, and can lack reliable neighbours for new regimes. Correlated features may repeatedly emphasise the same information. [Nearest-neighbour guide](https://scikit-learn.org/stable/modules/neighbors.html).

**MLP regression** learns through multiple computational layers. It can express interactions, but adds architecture, learning-rate and regularisation choices, scaling requirements, convergence issues and seed sensitivity. It also increases Q&A preparation work. [Neural-network guide](https://scikit-learn.org/stable/modules/neural_networks_supervised.html).

A rigorous comparison of a few justified models is more valuable here than a long list of complex models.

## 11. Selection and allocation

The coursework asks for at least three suitable scikit-learn candidates plus a linear/logistic reference. It does not require three completely different broad model families.

| Plan discussed in the original guide | Candidates, in addition to OLS | Main comparison |
|---|---|---|
| **A — adopted** | Random Forest, Extra Trees, HGB | Randomisation, averaging versus boosting, performance and cost |
| B — background alternative | Quadratic Ridge, Random Forest, HGB | Expanded linear formula versus tree ensembles |

The earlier recommendation to discuss B is historical study material. A is now the execution plan.

| Member | Responsibility |
|---|---|
| 1 — Wenyi | Shared framework, OLS and integration |
| 2 — Kiki | Random Forest |
| 3 | Extra Trees |
| 4 | HGB |
| 5 | Same-runtime cost measurement and final test |

Allocation does not imply completed human contributions.

## 12. Evidence every model must provide

Use identical time folds to answer:

1. How accurately does it predict later periods?
2. How large is the training/validation gap?
3. What are fitting, inference and storage costs?
4. Does it satisfy the predefined deployment constraints?

Lowest mean MAE does not guarantee highest tolerance coverage. Greater complexity does not guarantee improvement. Fix the metrics, constraints and selection rule before using candidate results; do not change rules using final-test feedback.

The repository currently verifies data checks, common folds, linear validation and linear cost. Candidate searches, extended diagnostics and final testing are not yet integrated as verified results. CW1 already exposed the same test years, so disclose that historical limitation.

## 13. AI assistance

OpenAI Codex/ChatGPT helped explain models, inspect official documentation and prepare this guide. No candidate performance was fabricated. The English edition preserves the Chinese guide's technical content while identifying the subsequently fixed model allocation. Members must review the material and record their actual work.
