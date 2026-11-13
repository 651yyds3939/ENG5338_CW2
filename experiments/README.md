# Current member entries

Open these notebooks from the project checkout; the complete repository (including `src/`, `data/` and `results/submitted/`) is required.

- `member2_random_forest.ipynb`: latest Random Forest settings, optional latest-grid rerun, fold validation, plot and final result export.
- `member3_extra_trees.ipynb`: latest depth-14 Extra Trees settings; earlier depth-12 search remains historical.
- `member4_hist_gradient_boosting.ipynb`: latest HGB settings, portable plotting and export after plots.
- `member5_benchmark.ipynb`: received Member 5 notebook, with independent Windows costs and contribution analysis. Loads preserved `results/member5_local_py310/` measurements on rerun; the raw original is kept in the ignored submission archive.

Model notebooks actually train the selected configuration when run; full search is off by default. The main notebook already contains executed four-model comparison. Individual reruns write under `results/member_runs/`, so they do not overwrite submitted evidence or the integrated comparison. Export cells run after graphs. Save the notebook with outputs if sending a new result. Retain analysis and AI-use details in the member notes.

Submitted files remain attributed to their authors. These portable entries were rebuilt during AI-assisted integration and use the shared project implementation. Original returned files are preserved locally; the receipt manifest records their hashes. Old standalone starter packages are preserved in the ignored local backup and are not needed to run this repository.
