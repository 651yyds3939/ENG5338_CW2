# Integration — 10 November 2026

The root master notebook is the current entry point. Three member-supplied tuned configurations and OLS are re-evaluated under the same chronological folds. Source searches remain under `results/submitted/`; new selected-configuration outputs remain under `results/development/`. Search evidence is audited, not silently represented as a freshly repeated full search.

Original returned notebooks and ZIPs are preserved byte-for-byte under ignored `.local_private/submissions/`, with their hashes in `notes/received_manifest.json`. Attributed member analysis is under `notes/`. Portable entries under `experiments/` use one shared implementation in `src/`, with no member-local drive paths. Original HGB graphs remain in the preserved local ZIP; current plots are regenerated consistently. Export cells follow plotting.

Latest Extra Trees uses depth 14, 400 trees, minimum leaf size 10 and max_features=0.8. The depth-12 run is archived as earlier tuning evidence. RF uses 600 trees, depth 11, minimum leaf size 20, max_features=0.5 and max_samples=0.9. HGB uses 200 iterations, learning_rate=0.05, max_leaf_nodes=15, L2=1, early_stopping=False. OLS uses training-fold median imputation and scaling.

No candidate meets the 90% coverage target. The target is a project assumption, not a course-imposed minimum accuracy. Final recommendation remains a group decision; costs and failure to meet constraints must be discussed. No final held-out prediction is enabled. Report and slides remain pending as requested.

Common cost measurement is available through member 5's notebook and `scripts/benchmark_models.py`. Integration reference measurements, if present, are agent-executed and require member 5's review. Raw timings and runtime records identify what actually ran; no one is credited with another person's or an AI's work.

Superseded starter packages, baseline-only outputs and dated reviews are preserved in the ignored local backup, outside the upload tree. See the root README for the active directory map. Chinese explanations: [integration guide](../zh/整合说明与下一步_zh.md).

Executed integration reference costs (same machine, one numerical thread): median full-development fits OLS 0.016 s, RF 23.82 s, Extra Trees 5.46 s, HGB 0.334 s; median single-row predictions approximately 1.02, 38.18, 26.66 and 2.55 ms respectively. RF and Extra Trees miss the 10 ms target on this runtime. All four miss the coverage target. These are local Python pipeline costs, not production-service guarantees. Raw samples, execution identity and runtime are in `results/costs/`; member 5 review remains pending.
