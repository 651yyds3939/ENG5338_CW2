# GAS4 project explained: purpose, principles, methods, outcomes and CW1/CW2 links

English edition of the [Chinese project explanation](../zh/项目全解读_CW1与CW2对照_zh.md), for learning, group coordination and Q&A rather than the final report.

Sources: local CW1/CW2 briefs, CW2 templates, course dataset guide, the completed CW1 notebook, current CW2 notebook/results, and task allocation. **The assigned model pool is fixed; the final recommended pipeline is not yet selected.** Engineering thresholds must be justified from use, while results must come from actual runs.

## 1. The project in plain language

A gas turbine has historical measurements of ambient conditions and operating state, alongside measured CO emissions. We ask a computer to learn which combinations of readings correspond to which CO concentrations. After training, it takes a set of current readings and estimates CO.

CW2 goes further than fitting a model: act as an engineering team, specify a purpose and acceptable requirements, fairly compare at least three candidates with linear regression, then recommend a complete pipeline using prediction, overfitting and cost evidence.

The coursework values rigorous experiments and supported reasoning, not just the smallest error number.

## 2. Engineering use

### A virtual CO sensor

A virtual sensor estimates a quantity from other available measurements:

```text
Existing temperature, pressure and process readings
                         ↓
                  Trained pipeline
                         ↓
                 Estimated current CO
                         ↓
              Operator monitoring support
```

This gives practical reasons to inspect input availability, error, latency and resource use. The coursework is an offline historical-data study. It does not require connecting to a turbine, installing sensors, building a website or deploying a production service.

| Question | Current implementation |
|---|---|
| Task | Regression: a continuous number |
| Inputs | Nine contemporaneous ambient/process readings |
| Output | CO concentration, mg/m³ |
| Use | Research into monitoring support |
| Timing | Current observation, not next-hour prediction |

CO and NOx are permitted targets; TEY is prohibited as target. Switching target would require redefined tolerances and complete reruns, not just a relabelled table.

### Why not simply read the CO column?

During training, measured CO is the answer used to learn and evaluate. At use time, only the inputs are supplied. Feeding CO into its own predictor is like handing out the exam answers.

NOx is excluded so that the proposed application does not depend on another pollutant analyser; this is an engineering choice, not an explicit course ban on that input. TEY is allowed as an input only if the corresponding measurement is available when CO must be estimated. If it is not, remove it consistently and rerun all models.

## 3. The dataset

Use the course CSV, not a replaced online version.

| Checked property | Value |
|---|---:|
| Rows | 36,733 |
| Columns | 12 |
| Years | 2011–2015 |
| Missing cells | 0 |
| Non-finite values | 0 |
| Exact duplicate complete rows | 7 |

| Group | Fields | Meaning |
|---|---|---|
| Time | `year` | Temporal split/diagnosis |
| Ambient | `at`, `ap`, `ah` | Temperature, pressure, humidity |
| Process | `afdp`, `gtep`, `tit`, `tat`, `tey`, `cdp` | Filter differential pressure, exhaust pressure, temperatures, energy yield, compressor pressure |
| Emissions | `co`, `nox` | Permitted prediction targets |

Current inputs are the three ambient and six process fields. Year is not an input, CO is the target, NOx is excluded.

Development observations matter for design:

- Many CO values are low, with a small high-concentration tail.
- Near-zero targets make ordinary percentage errors unstable.
- Strongly correlated process variables share information.
- 380 development humidity readings exceed 100%, at most 100.2%. Retain them without recording-error evidence.
- Duplicate readings can reflect stable operating conditions; do not delete on appearance alone.
- The guide describes hourly averages, but the CSV lacks full timestamps. Ordered rows are not verified one-hour steps.

## 4. Learning as practice and examinations

### One record is one answered exercise

- `X`: nine sensor measurements.
- `y`: measured CO.
- Model: a rule estimating `y` from `X`.
- Training: adjust the rule to reduce historical errors.

Linear regression adjusts weights; a tree learns questions; a forest averages trees; boosting improves predictions sequentially. They solve the same input-to-answer task using different representations.

### Why training performance is insufficient

A student can memorise practice answers without solving new questions. A model can similarly fit noise and fail on later records. Some answers must therefore remain unused during training so that prediction can be assessed.

| Partition | Analogy | Purpose |
|---|---|---|
| Training part | Practice exercises | Learn preprocessing and model parameters |
| Validation part | Mock exam | Compare settings and diagnose generalisation |
| Final test | Final examination | Evaluate one fixed final recommendation |

Validation is used to make decisions and can itself be overused; this motivates a separate final test. Our validation records are supplied by five temporal folds inside development data, not a separate permanent file.

### Overfitting and underfitting

Overfitting means learning accidental detail. Underfitting means a rule is too limited to capture useful structure.

| Pattern | Possible cause | Next evidence |
|---|---|---|
| Both train and validation poor | Insufficient model/input capacity | Appropriate features or flexibility |
| Train excellent, validation worse | Variance or temporal distribution changes | Complexity controls, fold patterns, drift |
| Both good | Encouraging preliminary evidence | Constraints and final test |

A train/validation gap alone does not prove overfitting: later operating conditions can differ from earlier ones.

## 5. Full workflow

### Step 1: define the question and success criteria

Explain who uses the estimate and when inputs are available. Specify one or two application-based deployment requirements.

| Budget in current configuration | Motivation |
|---|---|
| At least 90% of records within absolute CO error 1 mg/m³ | Per-reading usefulness rather than mean error alone |
| Single-row complete-pipeline median no more than 10 ms on the recorded single-thread CPU | Explicit computation budget |

These numbers are engineering assumptions, not course-mandated, manufacturer or legal standards. Their application rationale must be documented. The brief permits one justified constraint; efficiency must still be compared. Do not lower thresholds after seeing failure to manufacture success.

### Step 2: inspect and fix the inputs

Check schema, missingness, repeats, ranges and order. Explain retention/exclusion. Candidates receive the same raw inputs; model-appropriate preprocessing may differ, such as scaling linear models but not trees.

### Step 3: reserve later years

```text
2011–2013: 22,191 development rows
    → Training, temporal CV, tuning, diagnosis, development-input cost measurement

2014–2015: 14,542 reserved rows
    → One evaluation of the fixed final recommendation
```

This matches learning from history for later deployment. Random mixing may expose future/neighbouring regimes during training and overestimate performance.

**Historical exposure limitation:** CW1 already evaluated the same test years. CW2 isolation does not make them historically unseen. Disclose that fact and avoid selecting from old test rankings. New blind evidence would require approved later/external data; resplitting old records cannot erase exposure.

### Step 4: five chronological CV folds

Train on an early prefix, validate on the next block, expand the prefix, and repeat five times. Current `TimeSeriesSplit(n_splits=5, gap=24)` leaves 24 rows between each training endpoint and validation start. This may reduce neighbouring dependence but does not guarantee independence or a 24-hour gap.

Gap 0/24/168 and whole-year sensitivity checks are development-only extensions, not completed findings. All candidates must use the same fold list.

### Step 5: complete pipelines and leakage prevention

```text
Linear reference: raw inputs → median imputer → standardisation → OLS → CO
Tree candidate:   raw inputs → median imputer → model → CO
```

An imputer currently replaces nothing but makes future missing-input handling explicit. Every fold learns medians, means and standard deviations from its own training records. Global preprocessing before CV leaks future information. Feature selection or transformations chosen using held-out answers can also leak information even without including the answer as an input.

### Step 6: run the linear reference

A fast and explainable baseline anchors the comparison. Judge whether complex-model improvements justify added cost. OLS has no regularisation-strength grid, but still goes through the common folds and scoring as one fixed configuration.

### Step 7: tune the assigned candidates

| Owner | Model | Intuition | Tuning directions |
|---|---|---|---|
| Member 2 | Random Forest | Average different trees | Trees, depth, leaf sample size |
| Member 3 | Extra Trees | More random split thresholds | Same dimensions; inspect randomisation trade-offs |
| Member 4 | Histogram gradient boosting | Sequential corrections | Rate, leaves, L2 |

The earlier study guide discussed quadratic Ridge as an alternative for methodological diversity; it is not the adopted execution plan. See [model guide](MODEL_GUIDE.md).

Tuning means comparing justified configurations using shared validation, not only running defaults. Each initial candidate grid contains 8 settings, giving 40 CV fits plus a development refit. Extra benchmark fits are additional, so 40 is not the total number of fits in the project.

### Step 8: common scores and overfitting diagnosis

Regression does not have an undefined “90% accuracy”. A percentage must state exactly what is counted.

| Metric | Plain meaning | Interpretation |
|---|---|---|
| MAE | Average absolute miss | Lower is better, target units |
| RMSE | Error with greater penalty for large misses | Lower; sensitive to tails |
| R² | Improvement relative to the evaluated sample's mean predictor | Can be negative; not classification accuracy |
| Tolerance coverage | Fraction within ±1 mg/m³ | Higher; fix tolerance in advance |
| Train/validation MAE gap | Known-versus-later-period difference | Interpret alongside drift |
| Negative prediction fraction | Physically questionable outputs | Diagnose; do not invent post-hoc clipping rules |

Illustration only: absolute errors 0.2, 0.4, 1.2 have MAE 0.6; with tolerance 1, coverage is 2/3. These are not measured GAS4 values.

Inspect each fold, not just the mean. Fold SD describes period variation, not an independent-sample confidence interval. Tuning and reporting on the same folds is selection-optimistic. Nested temporal CV is an option, not an implemented result.

### Step 9: fair computational measurements

| Cost | Question |
|---|---|
| Total search time | What did finding the settings cost? |
| Final fit | What does refreshing the chosen model cost? |
| Single prediction | How long does one complete call take? |
| Batch prediction | How long for 1,000 records together? |
| Memory and artifact size | Is the target machine suitable? |
| Size scaling | What happens as the dataset grows? |

Use the same runtime, threads and inputs, warm-up and repeated samples. The framework uses 3 fit repeats, 100 single calls and 10 batch calls. Full preprocessing is included; sensor acquisition, networking and service overhead are excluded. Batch amortised cost is not single-call latency.

A separate fit samples process RSS increase; short peaks and allocator reuse can obscure actual memory. A zero increment is not no memory. Serialized bytes are not runtime RAM. Different members' local milliseconds cannot establish speed rankings: member 5 runs all candidates together.

### Step 10: recommend, freeze, then test once

Screen constraints and reason about accuracy, robustness and cost. Lowest MAE need not mean highest coverage or deployability. Current family tuning minimises mean MAE before feasibility screening; a coverage-first tuning rule would be a protocol change, to be declared consistently rather than changed after testing.

Final sequence:

1. Complete candidates and development diagnostics.
2. Fix requirements, full pipeline and parameters from that evidence.
3. Save the selection record: data hash, protocol, parameters, rationale and approval evidence.
4. Fit all development records.
5. Produce one test prediction vector.
6. Calculate predeclared scores/diagnostics, retaining row IDs and runtime/model-lock provenance.
7. Report failure honestly; do not retune or switch using this test.

The current notebook documents sealing and this future workflow; the guarded final prediction code is not yet implemented.

## 6. What the final outcome should be

### A model and supported claims

The intended output is a fitted pipeline that accepts one valid nine-measurement record, applies fixed training-derived preprocessing, and outputs estimated CO. Evidence should establish:

- Later-period validation improvement and weak periods.
- Whether predefined coverage and cost requirements pass.
- Training, prediction and resource cost on recorded hardware.
- One final-test evaluation and limitations.
- Conditions under which the recommendation would change.

Complexity is not a promise of improvement, and 90% coverage is not guaranteed. If nothing satisfies the constraints, report no feasible candidate and what additional data/requirements work is needed.

### Course deliverables

| Deliverable | Requirement |
|---|---|
| English report | Template; main body ≤8 pages, appendix ≤1 page; contribution statement excluded |
| Presentation PDF | 10-minute presentation plus 10-minute Q&A |
| One group notebook | Reproduce every report score/figure and identify contributions |
| Contribution/AI statement | Actual member implementation/writing/locations; tools/use; all members read and agree |

Filenames:

- `ENG5338_CW2_report_GAS4.pdf`
- `ENG5338_CW2_presentation_GAS4.pdf`
- `ENG5338_CW2_notebook_GAS4.ipynb`

The main comparison should place accuracy, overfitting and cost together. The notebook is checked rather than separately marked, but reproducibility still matters. Add a repository link to the report's first page when using one and retain the dataset citation.

### Assessment emphasis

Report categories: experiment/pipeline design, accuracy/overfitting, computational efficiency, and justified recommendation, each 25% of the report mark. Presentation categories: clarity, accurate/deep content, justified recommendation, and engagement/Q&A, each 25% of presentation. Course weighting is report 20% and oral presentation 20%; do not confuse it with internal rubric percentages.

## 7. CW1 versus CW2

### Official requirements

| Aspect | CW1 | CW2 |
|---|---|---|
| Working form | Individual | Engineering team |
| Core task | Apply linear/logistic regression and explain the pipeline | Engineering question/constraints, multi-model comparison, recommendation |
| Dataset | Individual choice within allowed set | Group-assigned dataset |
| Models | Linear/logistic core | At least three suitable candidates plus reference |
| Fairness | Appropriate validation/analysis | Explicit shared split/folds/metric, each tuned |
| Constraints | No explicit 1–2 deployment-constraint clause | One or two justified realistic requirements |
| Conclusion | Application, data, prediction and cost | Why a pipeline meets constraints and trade-offs |
| Test wording | Correct training/validation, not CW2's explicit one-test clause | Final recommendation tested once |
| Report | Template, maximum 5 pages | Maximum 8 main +1 appendix, statement excluded |
| Oral component | Not listed in supplied CW1 brief | 10-minute talk +10-minute Q&A |
| Notebook | Separate 20% clarity/reproducibility criterion | Not separately marked; results/contributions checked |
| Contributions | Individual | Distinct actual work; any member may be asked any section |

### Your actual CW1 went beyond one simple fit

The completed CW1 used the same GAS data, CO and nine inputs; the same year split; five time folds with `gap=0`; OLS, Ridge and quadratic Ridge; alpha searches; train/validation analysis; learning and size-cost curves; timing/memory/model size; and final testing after development selection. Its test analysis included more than one reference model.

CW2 adds explicit engineering constraints, broader common-protocol comparison and team recommendation/integration. It is not a group-ID rename of CW1.

### Actual implementation differences

| Aspect | Existing CW1 | CW2 framework |
|---|---|---|
| Target/inputs | CO, nine readings | Same implemented inputs |
| Years | 2011–2013 / 2014–2015 | Same, with historical-exposure disclosure |
| Gap | 0 rows | 24 rows |
| Scores | MAE main | MAE plus coverage/constraint screen |
| Candidates | Ridge and quadratic expansion | Assigned RF, Extra Trees, HGB |
| Selection | Lowest development CV MAE | Constraint-aware comparative recommendation required |
| Test | Already run, several reference outputs | Not run; one fixed final pipeline intended |
| Organisation | Individual workflow | Shared interfaces and three owner entries |
| Delivery state | Completed individual report/results | Framework phase; final group report/slides absent |

Do not directly rank scores from differing gaps, configurations or preprocessing. Even a reused CW1 method must be rerun under CW2's common protocol.

## 8. What transfers, what must be redone

Transfer understanding of fields/units, chronological splitting, fold-local pipelines, regression metrics, runtime/seed/cost recording, Ridge/polynomial concepts, clear interpretation and AI-use records.

Re-establish the group question, deployment rationale, shared protocol, three tuned candidates, common-runtime costs, constraint-based selection, final CW2 evaluation, team contributions, report and presentation.

CW1 offers methodological experience; its test ranking must not guide CW2 selection. A historically good quadratic-Ridge test result does not establish the final answer for the group.

## 9. Why a shared framework matters

It provides the same examination questions, marking rules and result form. Owners change the predictive method, not the examination.

| Object/function | Role |
|---|---|
| `X_dev`, `y_dev` | Common development inputs/targets |
| `FOLDS` | Common chronological indices |
| `SCORING` | Common scores |
| `pipeline_for` | Full preprocessing/model pipeline |
| `run_search` | Common tuning and result exports |
| `benchmark_pipeline` | Shared fit/inference/resource measurements |
| `SUMMARIES`, `COSTS` | Completed evidence collections |
| `RUN_MODELS` | Candidate execution switches, default disabled |

Owners work independently, Wenyi aligns their evidence. Scikit-learn's internal `test` CV columns mean fold validation, not the final reserved period. The master [notebook](../../ENG5338_CW2_notebook_GAS4.ipynb) remains the integrated submission entry.

## 10. Five members and Wenyi's remaining work

Use [current member numbering](../../TASK_ALLOCATION.md), not historical A–E labels.

| Member | Main task | Evidence |
|---|---|---|
| 1, Wenyi | Framework, OLS, integration, common methods/tables | Reproducible common code and final integration |
| 2, Kiki | RF | Code, grids, best settings, train/validation folds, analysis |
| 3 | Extra Trees | Equivalent evidence |
| 4 | HGB | Equivalent evidence |
| 5 | Costs, final test, limitations | Same-runtime raw timings, environment, model lock and one test |
| Everyone | Question, constraints, recommendation, report/slides/Q&A | Reviewed decisions and truthful contributions/AI use |

Wenyi has the initial shared code and reference, but still needs to distribute the protocol, review fold-local processing and consistency, integrate owners' artifacts, run the full master fresh, assemble comparisons with member 5, and write final common methods. Existing timing utilities do not mean member 5's work is complete. AI-generated scaffolding needs actual human review and understanding.

## 11. Current progress and actual numbers

Completed: requirement/template/data/CW1 inspection; structural/development checks; partitions/sealing; temporal folds, metrics/search; OLS validation and costs; candidate definitions/grids/entries; comparison scaffolding; runtime/version/AI records; 15 master code cells executed without error.

| Recorded OLS result | Value |
|---|---:|
| Mean train MAE | 0.6732 mg/m³ |
| Mean validation MAE | 0.9073 mg/m³ |
| Mean validation RMSE | 1.6892 mg/m³ |
| Mean validation R² | 0.4805 |
| Coverage within ±1 mg/m³ | 71.80% |
| Single-row median | 1.024 ms |

These are development CV, gap-24 results, not final test. Local timing is not universal. OLS meets the configured latency budget but not coverage. Member 2 has subsequently reported progress in chat, but those artifacts must be received and verified before updating the repository comparison.

Sources: [OLS summary](../../results/linear_reference_summary.json), [benchmark](../../results/linear_reference_benchmark.json), [runtime](../../results/runtime.json), [verification](../../results/framework_verification.json).

Outstanding: application rationale; verified candidate search/analysis; common costs and scalability; overfitting/tail/sensitivity comparison; final selection/test; final English report/presentation; complete actual contribution statement with all-member agreement.

## 12. How to describe the project

**Thirty seconds:** We estimate gas-turbine CO from historical ambient/process data. We define monitoring requirements, compare three candidates and linear regression using identical chronological folds, inspect error and overfitting, and measure cost. After fixing one suitable full pipeline we test it once. The shared framework and reference are verified; candidate evidence is being collected.

**CW1 connection:** CW1 taught the end-to-end pipeline. CW2 turns it into a shared engineering decision: same evidence for all models, explicit requirements, and a justified recommendation. Prior work helps learning but does not replace new controlled comparison.

Ten points to remember:

1. Estimate contemporaneous CO, not next-hour CO.
2. Explain numerical deployment budgets using the application.
3. Keep OLS plus the three assigned candidates.
4. Use common inputs, folds and scores.
5. Learn preprocessing inside each training fold.
6. Inspect more than training scores or mean MAE.
7. Compare cost on one runtime.
8. Freeze model/settings before the one final test.
9. Report infeasibility rather than invent success.
10. Understand the entire notebook and record actual contribution/AI use.

## 13. Related documents and AI assistance

[Requirements and plan](REQUIREMENTS_AND_PLAN.md) · [Notebook Q&A](NOTEBOOK_GUIDE.md) · [Model guide](MODEL_GUIDE.md) · [Task allocation](../../TASK_ALLOCATION.md) · [Contribution/AI log](../../notes/contributions_and_ai.md).

OpenAI Codex/ChatGPT helped inspect local material and prepare Chinese and English study explanations. This translation/organisation does not claim new model fitting, final testing or report completion.
