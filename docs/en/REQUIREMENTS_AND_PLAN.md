# GAS4: coursework requirements, experiment design and discussion checklist

English edition of the [Chinese planning document](../zh/需求检查与周一讨论_zh.md). This is study/planning material, not the final report. Submission-facing notebook explanations are English.

Sources are the local `coursework brief2.pdf`, `template_cw2_ENG5.pdf`, `template_cw2_ENG5.tex`, the course dataset guide in CW1, the supplied Moodle screenshot and the actual final CW1 notebook. CW1 source material is read-only.

The original document was prepared for Monday 9 November 2026. The subsequently adopted pool is Random Forest, Extra Trees and HGB plus OLS, using member numbers 1–5 in [the current allocation](../../TASK_ALLOCATION.md), rather than the old A–E proposal. Numerical deployment thresholds are engineering assumptions needing an application rationale, not regulatory limits.

## 1. Mandatory requirements

“Incomplete” below distinguishes future work from missing planning.

| Item | Requirement | Current evidence / remaining work |
|---|---|---|
| Group and data | Use the assigned dataset; one submission per group | GAS4, GAS dataset |
| Source | Use the Moodle course CSV, not a substituted original download | Unchanged copy in `data/`, verified hash |
| Target | For GAS, choose CO or NOx; TEY may not be the target | Implementation uses CO |
| Engineering question | State a clear engineering question | Contemporaneous CO virtual sensor |
| Constraints | One or two realistic deployment requirements with application-based reasons | Coverage and latency budgets specified; rationale must be strengthened |
| Models | At least three suitable scikit-learn models plus linear/logistic reference | Assigned RF/Extra Trees/HGB and OLS; only OLS verified here |
| Common protocol | Same split, folds and metric; tune each model first | Shared functions and saved folds; OLS has no regularisation parameter |
| Overfitting | Show training beside validation and analyse/mitigate overfitting | OLS folds available; candidate analysis outstanding |
| Efficiency | Training and prediction times with the measured runtime | OLS measurements available; all-model benchmark outstanding |
| Recommendation | Recommend a full pipeline under the constraints, justify trade-offs | No final selection yet |
| Test | Evaluate the recommendation on the test set once | No CW2 test prediction has run |
| Report length | Template, at most 8 main pages and 1 appendix page; contribution statement excluded | Final report not written |
| Report sections | Question/constraints, experiment design, comparison, recommendation; optional appendix and contribution statement | Follow provided template later |
| First page | Group, names/IDs, dataset; repository link if using one | GAS4 and Wenyi known; other identity details to be supplied |
| Dataset citation | Cite dataset in every report | Notebook includes authors/DOI; retain in report |
| Presentation | 10-minute presentation plus 10-minute Q&A | To prepare |
| Presentation content | Question, constraints, predictive performance, efficiency, overfitting and recommended pipeline | Needs candidate findings |
| Teamwork | Explain distinctive member contributions; speaking in turns is not required | Roles allocated; actual work must be logged |
| Q&A | Any member may be asked about any notebook part | Everyone must understand the whole workflow |
| Notebook | One group notebook reproduces every report result; checked but not marked separately | Master framework runs; integrate remaining experiments |
| Contributions | Per-member implementation, writing and notebook location; all members read/agree | Living record, not final approval |
| AI use | Allowed for tutoring/coding; identify tools and use in contribution statement | Actual assistance recorded |
| Peer evaluation | Moodle peer evaluation, statement and Q&A may affect individual marks | Follow course arrangements; roles are not proof of contribution |
| Filenames | `ENG5338_CW2_report_GAS4.pdf`, `ENG5338_CW2_presentation_GAS4.pdf`, `ENG5338_CW2_notebook_GAS4.ipynb` | Notebook name correct |

The brief lists group report 20% and oral presentation 20% of the course; these are different from the internal rubric weights below. The supplied screenshot shows **Friday 13 November 2026, 12:00** as the deadline and GAS4 as the group. This is screenshot evidence, not a live Moodle recheck.

## 2. Rubric-based delivery checks

Report categories each carry 25% of the report mark. Strong design and supported interpretation matter more than a raw accuracy ranking.

| Category | Evidence to prepare | Checklist |
|---|---|---|
| Experiment/pipeline design, 25% | Question, constraints, model reasons, partition/fold diagram, preprocessing, grids | [ ] Deployable question; [ ] justified constraints; [ ] common inputs/folds/metrics; [ ] tuned candidates; [ ] fold-local preprocessing |
| Accuracy/overfitting, 25% | Main train/validation MAE, RMSE, R², coverage table; fold and parameter plots | [ ] Generalisation gaps; [ ] drift; [ ] complexity controls; [ ] tail errors; [ ] SD not presented as CI |
| Efficiency, 25% | Search wall time, repeated final fit, single/batch inference, runtime, size/resource experiments | [ ] Common hardware/threads; [ ] warm-up/repeats; [ ] search versus fit; [ ] scalability evidence; [ ] RSS versus artifact size |
| Recommendation, 25% | Feasibility screen, trade-offs, fixed selection record, single test, limitations | [ ] Constraints actually checked; [ ] report no feasible model if necessary; [ ] no test tuning; [ ] what changes the recommendation |

Scalability, resource use and detailed diagnosis are high-band evidence; the brief does not prescribe a particular learning-curve algorithm or fixed memory limit. Do not mark candidate comparisons or final recommendation complete because the framework exists.

Presentation categories are also 25% each:

- [ ] Clear, logical, well-paced and accessible communication.
- [ ] Accurate terminology and evidence-based comparative content.
- [ ] Well-reasoned recommendation and trade-offs.
- [ ] All members can answer questions about the complete notebook.

## 3. Data and target inspection

The CSV is **36,733 × 12**, numeric throughout (`year` integer, other columns floating point), with zero missing cells, zero non-finite values and 7 exact duplicate complete rows. Year counts: 2011 7,411; 2012 7,628; 2013 7,152; 2014 7,158; 2015 7,384. Whole-file inspection is structural; distribution analysis uses development years only.

| Field | Meaning | Course-guide unit | Use |
|---|---|---|---|
| `year` | 2011–2015, chronological within year | Year | Partition/diagnosis, not input |
| `at` | Ambient temperature | °C | Input |
| `ap` | Ambient pressure | mbar | Input |
| `ah` | Ambient humidity | % | Input |
| `afdp` | Air-filter differential pressure | mbar | Input |
| `gtep` | Gas-turbine exhaust pressure | mbar | Input |
| `tit` | Turbine inlet temperature | °C | Input |
| `tat` | Turbine after temperature | °C | Input |
| `tey` | Turbine energy yield | MWh | Input if available; prohibited target |
| `cdp` | Compressor discharge pressure | mbar | Input |
| `co` | Carbon monoxide concentration | mg/m³ | Current target |
| `nox` | Nitrogen oxides concentration | mg/m³ | Alternative permitted target; excluded CO input |

Units follow the supplied course guide; verify the source before any physical conversion rather than changing units from the magnitudes alone.

Development-only observations:

- CO min 0.00038751, median 1.5242, mean 2.21439, 95th percentile 6.1675, max 44.103 mg/m³. The upper tail motivates RMSE/tail analysis; near-zero denominators make ordinary percentage error unstable.
- NOx median 67.096, 95th percentile 87.1325, range 27.765–119.91 mg/m³. Switching target would require redefining tolerances and rerunning every model.
- 380 development rows have humidity above 100%, max 100.2%; retain without recording-error evidence.
- Pearson correlation is about 0.994 for `gtep`/`cdp` and 0.989 for `tey`/`cdp`. Interpret OLS coefficients cautiously; correlation does not establish causality.
- No missing values, but a fold-local median imputer defines handling of future missing inputs.
- Repeats may reflect stable operating conditions; retain order and records unless an error is established and uniformly corrected.
- Hourly averages do not imply exact one-hour gaps between adjacent CSV rows; full timestamps are unavailable.

Engineering question: can nine contemporaneous ambient/process measurements estimate CO accurately and cheaply enough for operator monitoring, without another pollutant analyser? This is neither a future forecast nor a certified compliance system. TEY must be available at the intended inference time.

## 4. Measurable deployment assumptions

| Budget | Rationale | What the evidence does not establish |
|---|---|---|
| At least 90% of records with absolute CO error ≤1 mg/m³ | Per-observation usefulness; avoids unstable near-zero percentage errors | Not a manufacturer/regulatory tolerance; requires application justification |
| Complete-pipeline single-row median ≤10 ms on the recorded single-thread CPU | Explicit software computation budget for monitoring integration | Not a dataset-provided SLA or measured end-to-end service deadline |

Current screening uses mean CV coverage ≥90% and median single-row latency ≤10 ms, with worst-fold coverage separately shown. Requiring every fold to pass would be a different predeclared rule. Do not change thresholds after seeing candidates fail. A task with only one justified constraint is permitted, but efficiency still needs analysis. Tail diagnostics must not be described as legal exceedance detection without an authoritative threshold.

## 5. Shared design

### Split, metrics and leakage prevention

1. Development 2011–2013: 22,191 rows. Reserved test 2014–2015: 14,542 rows. This follows the dataset guide's author split and past-to-future application.
2. Five expanding `TimeSeriesSplit` folds, no shuffling, current `gap=24` rows. This may reduce neighbour dependence, not prove independence or a 24-hour interval. Gap 0/24/168 and whole-year sensitivity checks remain future development-only work.
3. Tune on MAE; also report RMSE, R², coverage and negative-prediction fraction. Equal-size validation blocks make mean coverage equal pooled validation coverage; earliest training-only records are not validation predictions. Fold SD is not an independent-sample SE or CI.
4. Fit imputation/scaling within each training fold. Trees may omit scaling while keeping raw inputs, folds and metrics identical. No global feature selection/scaling or test-residual tuning.
5. `GridSearchCV(refit='mae', return_train_score=True, n_jobs=1)` uses negative error for maximisation; export positive MAE/RMSE.
6. Seed 42 for random models; OLS is deterministic and has no `random_state`. Changing inputs, target, gap, seed or thresholds requires coherent reruns and protocol records.

**Historical exposure:** CW1 already evaluated several models on the same 2014–2015 period. CW2 sealing does not make it historically unseen. Disclose exposure, avoid using CW1 test ranking to select CW2 settings, and recognise that truly new blind evidence requires course-approved later/external data.

### Assigned candidates and grids

| Model | Reason / risk | Search | Preprocessing |
|---|---|---|---|
| OLS reference | Fast/simple; misses nonlinearities; coefficients affected by collinearity | One fixed configuration | Median imputer + standardisation |
| Random Forest | Nonlinear interactions, variance control; size/extrapolation risks | Trees 100/300; depth 8/None; leaf size 2/10; `max_features=.8` fixed | Median imputer |
| Extra Trees | Extra split randomisation; do not assume superior speed/accuracy | Same 8-configuration grid as RF | Median imputer |
| HGB | Sequential corrections; learning-rate/complexity control | Rate .05/.1; leaves 15/31; L2 0/1; 200 iterations fixed | Median imputer |

Each candidate requires 8 × 5 = 40 search fits plus one full-development refit. HGB automatic early stopping is disabled to avoid random internal validation. Equal configuration count is not equal computational cost. Three ensemble estimators are permitted; reasons must follow from the application.

### Tuning and overfitting analysis

- Declare grids before results; tune each candidate. OLS has no regularisation strength to tune.
- Current rule selects each family's lowest mean validation MAE, then screens feasibility; never use test scores for this. A coverage-first tuning rule would need consistent declaration before candidate-driven changes.
- Boundary optima may justify a development-only grid extension, with extra search cost recorded; do not claim global optimality.
- Plot training and validation errors by fold/parameter. Separate potential model variance from temporal drift.
- Check whether depth, leaf size, L2 or learning-rate controls improve validation, not merely worsen training fit.
- Define high-CO cutoffs from each fold's training targets, then inspect later validation errors.
- Plan common chronological 25/50/100% prefixes for learning/cost experiments. Sample size also changes time coverage, so accuracy changes are not pure causal sample-size effects.
- Tuning-fold reporting is selection-optimistic. Nested chronological CV is an option, not an experiment already completed.

### Cost protocol

Use one numerical thread, one search worker, common runtime and fixed development prediction inputs. Record runtime/protocol IDs. Separate search wall time from final fitting. Warm up, then measure 3 fresh full-development fits; 100 single-row predictions after warm-up; 10 fixed 1,000-row batch predictions after warm-up. Save raw samples and medians; report p95 descriptively. Batch amortised cost is not single-call latency. Exclude sensor, network and service overhead explicitly.

A separate fit samples process RSS increment at approximately 5 ms intervals; short peaks/allocator reuse can cause undercounting. Zero increment is not zero memory. Pickle size is artifact size, not RAM. Full scalability experiments remain unrun.

### Final-test rule

Freeze the reviewed pipeline, parameters, protocol, data hash and decision rationale before opening the reserved period. Fit all development data, predict once, derive all predeclared diagnostics from that vector, and persist row IDs/model-lock hash/runtime. Reject a repeated final evaluation. Report failure without model switching or retuning. The framework describes but does not yet implement this final execution step.

## 6. Ownership and integration

Current member numbering supersedes the original A–E roles:

| Member | Main evidence |
|---|---|
| 1, Wenyi | Data/protocol/OLS, leakage audit, integration, common methods and tables |
| 2, Kiki | RF search, train/validation diagnosis, rationale/cost implications, model write-up |
| 3 | Equivalent Extra Trees evidence; distinguish it from RF |
| 4 | HGB evidence; explain rate/complexity and disabled random early stopping |
| 5 | Common benchmarking/resources, final lock/test, cost and limitations |

Background, writing, review and Q&A are shared. Keep actual names/IDs and dated evidence; proposed responsibility is not completed contribution. Owners submit independent experiment files; they do not independently alter shared folds/scorers. Add the repository link to the report if using one.

## 7. Notebook structure and discussion agenda

Sections: 1 runtime; 2 checks/sealing; 3 protocol/scoring/search; 4 OLS; 5 cost; 6 three owner entries; 7 comparison/feasibility; 8 extended diagnostics; 9 final-test workflow; 10 contributions/AI use.

Original Monday agenda, updated for the fixed model pool:

1. [ ] Explain the CO question and verify sensor/TEY availability.
2. [ ] Document tolerance, coverage/latency rationale and mean-fold versus every-fold feasibility.
3. [ ] Explain temporal folds, gap sensitivity and historical test exposure.
4. [ ] Record assigned-model grids, selection rule, search budget and consistent reruns.
5. [ ] Fill member names/IDs, handoff times, reviewers and actual contribution records.
6. [ ] Keep final testing sealed until selection; write report/slides from actual evidence.

The original suggested discussion pacing was 15 minutes on question/constraints, 15 on protocol/grids and 10 on ownership/integration, followed by each member explaining fold-local scaling and when the test may be opened. This is a suggestion, not a course requirement.
