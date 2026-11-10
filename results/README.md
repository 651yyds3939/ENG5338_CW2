# Experiment evidence

- `submitted/`: actual member exports with separate provenance. `member3/run1/` is earlier tuning; `member3/latest/` is depth 14. These are never overwritten by notebook reruns.
- `development/`: current integrated fresh-kernel selected-configuration validation, shared data/split/protocol/runtime records, saved per-observation validation predictions, high-CO diagnostics and feasibility.
- `costs/`: executed Codex integration reference measurements of all four pipelines on one machine. Raw repeated timings, RSS sampling caveats and runner identity are retained. Member 5 must review or remeasure before final reporting.
- `experiment_status.csv`: generated current run state.
- `member_runs/` and `search_reruns/` (created only when used): independent personal or optional full-grid reruns. They do not automatically replace approved submitted configurations.

No final test artifact exists. Cost results concern fixed selected pipelines; different-machine search wall times are not used to compare efficiency. All current models miss the coverage target, and RF/Extra Trees also miss the single-row latency target on the measured reference runtime. No final recommendation is encoded by the comparison order.
