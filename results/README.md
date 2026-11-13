# Experiment evidence

- `submitted/`: received model-owner searches and environments. Member 3 run1 records the earlier depth-12 search; latest uses depth 14.
- `search_reproduction/`: executed latest-grid replays in the integration environment.
- `development/`: common five-fold validation, per-row predictions, diagnostics and runtime.
- `member5_local_py310/`: Member 5 Windows timing samples, environment and interpretation table.
- `costs/`: earlier Codex Linux reference timing, with its own environment.
- `final/`: original HGB decision and assessment.
- `final_extra_trees/`: accuracy-first Extra Trees decision and assessment.
- `submission/`: combined report/slide evidence, tables and notebook execution audit.
- `member_runs/`, `search_reruns/`: ignored scratch reruns.

Extra Trees is selected by development MAE: 0.7226, with 81.76% coverage. Member 5 measured 19.03 ms single-row latency. The coverage target is 90%; 10 ms remains the original timing reference.

HGB was assessed first (MAE 0.8998, coverage 70.00%). Wenyi then prioritised accuracy and selected Extra Trees from the existing development ranking. Extra Trees was assessed on the same 2014–2015 observations (MAE 0.8011, coverage 73.36%); CW1 also used those years. Both records retain their decision inputs, hashes and predictions. A new future period supplies the next confirmation stage.
