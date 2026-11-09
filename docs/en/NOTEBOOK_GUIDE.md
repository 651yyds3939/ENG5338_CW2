# Shared notebook: purpose, measured evidence and Q&A

English edition of the [Chinese notebook guide](../zh/Notebook解读与问答_zh.md). Model allocation follows [the current task file](../../TASK_ALLOCATION.md).

## 1. Data flow

```text
Course CSV
  ├─ Whole-file structural checks: schema, missingness, finiteness, repeats, year counts
  ├─ Development 2011–2013
  │    ├─ Same five temporal folds → tuning → training/validation tables
  │    ├─ Full-development refit → cost using development inputs only
  │    └─ Evidence and constraints → later final selection
  └─ Reserved 2014–2015: row IDs retained; no CW2 test predictions
```

Each fold fits its own imputer/scaler/model using training records, then processes later validation records. Preprocessing the entire file before CV would leak information.

The shared notebook ran from a fresh kernel. Executing a disabled candidate cell only prints `NOT RUN`; it does not mean the candidate model has been trained.

## 2. Sections and functions

| Section | Purpose | What to explain |
|---|---|---|
| 1 Runtime | Threads, seed, imports, Python/packages/CPU/RAM/interpreter/runtime ID | Reproducibility needs more than a random seed |
| 2 Data | Hash/schema, structural checks, temporal partitions, removal of whole-data object, development overview | A hash identifies the file, not its truth; structural reading is different from tuning on test error |
| 3 Protocol | Target, nine inputs, budgets, gap, one saved fold list | A protocol change requires consistent reruns |
| 3 Metrics | `tolerance_coverage`, `negative_fraction`, `regression_metrics` | MAE, RMSE, R² and coverage answer different questions |
| 3 Pipeline/search | `pipeline_for`, `run_search`, exports | Fold-local fit; estimator cloning; full-development refit is not used to invent validation scores |
| 4 OLS | Single fixed configuration through common search; fold outputs and plots; first-fold preprocessing audit | Reference uses validation too; OLS has no alpha |
| 5 Cost | `sample_seconds`, `benchmark_pipeline`, memory and size | Warm-up/repeats; throughput versus latency; memory limitations |
| 6 Candidates | Three assigned models, 8 configurations each, individual owner entries | Disabled is unrun; do not invent performance |
| 7 Comparison | Join completed accuracy/cost results and feasibility screen | Currently only OLS; no all-model winner yet |
| 8 Extensions | Curves, gap sensitivity, tail errors, scalability placeholders | Planned work is not a finding |
| 9 Final test | Selection-lock/single-test description and sealing checks | No executable held-out prediction step currently |
| 10 Contributions | Ownership, actual work, AI use | Everyone can be asked about any section |

In scikit-learn search columns, `split0_test_mae` and `mean_test_mae` refer to **CV validation**, not the reserved 2014–2015 set. Shared tables use `validation` terminology.

`best_estimator_` is refitted on all development data for later deployment/cost. Its reported validation metrics still come from independent fold-specific fits.

## 3. Recorded linear-reference results

Protocol: CO, nine inputs, development 2011–2013, five expanding folds, gap 24 rows, seed 42. Sources: `results/linear_reference_summary.json`, `linear_reference_fold_metrics.csv`, and the benchmark JSON at the project root.

| Metric | Recorded value | Meaning |
|---|---:|---|
| Mean training MAE | 0.673202 mg/m³ | Fit on each fold's known records |
| Mean validation MAE | 0.907319 mg/m³ | Mean absolute error in later periods |
| Validation MAE fold SD | 0.151111 mg/m³ | Temporal variation, not CI |
| Mean validation RMSE | 1.689245 mg/m³ | Greater sensitivity to large errors |
| Mean validation R² | 0.480491 | Mean fold R², not 48.05% classification accuracy |
| Coverage within ±1 mg/m³ | 71.80097% | Below the 90% engineering budget |
| Worst-fold coverage | 57.38237% | Mean coverage can conceal weak periods |
| Mean MAE gap | 0.234117 mg/m³ | Generalisation gap also affected by time changes |
| Full-development fit median | 0.014909 s | 3 repeats after warm-up, preprocessing included |
| Single-call prediction median | 1.023609 ms | 100 warmed-up complete-pipeline calls |
| Single-call p95 | 1.089774 ms | Descriptive microbenchmark percentile, not service SLA proof |
| 1,000-row batch median | 1.152398 ms | 10 repeats; not single-call latency |
| Pickle size | 1.627930 KiB | Artifact size only |
| Sampled fit RSS increment | 0 MiB | Can miss short peaks/reuse memory; not zero memory use |

| Fold | Training MAE | Validation MAE | Validation coverage |
|---|---:|---:|---:|
| 1 | 0.460571 | 0.717657 | 84.5592% |
| 2 | 0.631866 | 0.807250 | 75.3110% |
| 3 | 0.712354 | 1.082914 | 57.3824% |
| 4 | 0.759298 | 1.088565 | 64.2780% |
| 5 | 0.801923 | 0.840211 | 77.4743% |

The justified conclusion is that OLS passes the current latency budget but not coverage. No candidate winner or final-test performance can be inferred. Timings describe the initial actual run; after a rerun use the newly generated artifacts.

Recorded runtime: Python 3.12.9, Linux, AMD Ryzen 7 5800H, 16 logical CPUs, approximately 15.47 GiB total RAM, one numerical thread and no GPU used. NumPy 2.5.4, pandas 3.0.6, SciPy 1.18.1, scikit-learn 1.9.1, Matplotlib 3.11.2. Full versions/pools are in `results/runtime.json`. The interpreter came from CW1's existing environment; all new project code/data/results remain in CW2.

## 4. Q&A preparation

**Why CO?** It is a permitted real emissions target and supports a virtual-sensor question without another pollutant reading. Near-zero values and an upper tail motivate multiple error measures.

**Why not TEY as target, but use it as an input?** The course guide prohibits that target but allows the input. Deployment still requires it to be available at inference time; otherwise change all models coherently.

**Why not random 80/20?** The question is past-to-future use. Randomisation may mix neighbouring and future regimes into training. Time validation is more relevant but not proof of independence.

**Is gap 24 optimal?** Not established. It reduces immediate-neighbour proximity as an assumption. Missing full timestamps mean rows are not verified hours. Sensitivity analysis belongs in development.

**Why not MAPE or a fixed percentage tolerance?** Near-zero CO can amplify ratios. Absolute mg/m³ is interpretable. The selected tolerance/coverage still needs application justification; the dataset alone cannot establish its adequacy.

**Will MAE and coverage choose the same configuration?** Not necessarily. Current tuning minimises MAE within families, then screens feasibility. That can miss a higher-coverage configuration in the same family. A different selection rule must be declared consistently before candidate-driven changes, never after testing.

**Why imputation if there are no missing values?** It currently replaces nothing but defines future missing-input handling. Fit the median from the fold's training records only.

**Why keep humidity above 100% and high CO?** Slight violations may be measurement/rounding; high emissions may be important genuine conditions. Without evidence, deletion distorts the task. Any development sensitivity rule must be documented and shared.

**Does a train/validation gap prove overfitting?** No. Temporal operating changes also matter. Examine complexity/regularisation curves and fold patterns.

**Why three tree ensembles?** They are distinct estimators with nonlinear interactions and clear controls: RF and Extra Trees differ in randomisation; HGB uses sequential improvements. The brief does not require separate broad families.

**Why disable HGB's internal early stopping?** Default internal validation may be random. Fix iterations and select rate/leaves/L2 using the common chronological folds; time-aware early stopping would require a dedicated design.

**Why both search and fit time?** Search reflects model-development cost across many fits; one final fit reflects refresh cost. Equal grid counts do not equal equal work.

**Why can 1,000-row prediction take nearly as long as one row?** Python/dataframe checks have fixed overhead and vectorised arithmetic amortises it. Throughput and single-call waiting time are different measurements.

**Is the test genuinely unseen?** Not historically: CW1 evaluated the same years. Disclose this and keep CW2 operational isolation. Stronger fresh evidence needs approved new data.

**What if the final test fails constraints?** Report failure and drift/data/model limitations; do not switch models or retune using the same test. Further development needs new independent evaluation evidence.

**How can results be checked rather than trusted as AI claims?** Executed outputs, per-fold CSVs, parameters, raw timing samples, hashes and runtime records support reproduction. Mark unrun work explicitly, log AI assistance, and require human understanding/review.
