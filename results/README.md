# Experiment evidence

- submitted/: latest received model-owner searches, settings and environments.
- search_reproduction/: executed latest-grid replays in the common environment.
- development/: common five-fold scores, per-row predictions, high-CO diagnostics and runtime.
- member5_local_py310/: Member 5 Windows timing samples and environment.
- final/: original HGB decision, assessment and frozen input snapshots.
- final_extra_trees/: accuracy-first Extra Trees decision, assessment and frozen input snapshots.
- submission/: combined accuracy/cost table and main-notebook execution audit.

Each experiment directory retains its protocol and folds as part of the experiment record. Assessment snapshots are SHA-256 checked byte-for-byte. Extra Trees has development MAE 0.7226 and coverage 81.76%; the later assessment gives MAE 0.8011 and coverage 73.36%. HGB was assessed first on the same 2014–2015 observations, which were also used in CW1. Both records retain the assessment history.

Older searches, early Linux reference costs and superseded status summaries are archived locally. Generated intermediate tables, per-model plot exports and scratch reruns are ignored by Git; the notebook recreates these outputs.
