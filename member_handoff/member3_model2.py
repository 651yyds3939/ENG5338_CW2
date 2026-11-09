"""Member 3's experiment. Edit estimator/grid and add your own analysis."""
from pathlib import Path
from cw2_common import SEED, run_experiment
from sklearn.ensemble import ExtraTreesRegressor

ESTIMATOR = ExtraTreesRegressor(random_state=SEED, n_jobs=1, max_features=.8)
GRID = {
    "model__n_estimators": [100, 300],
    "model__max_depth": [8, None],
    "model__min_samples_leaf": [2, 10],
}

if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    run_experiment("extra_trees", ESTIMATOR, GRID,
                   folder / "gas-turbine-emissions.csv", folder / "member3_results")
