"""Member 4's experiment. Edit estimator/grid and add your own analysis."""
from pathlib import Path
from cw2_common import SEED, run_experiment
from sklearn.ensemble import HistGradientBoostingRegressor

ESTIMATOR = HistGradientBoostingRegressor(random_state=SEED, early_stopping=False, max_iter=200)
GRID = {
    "model__learning_rate": [.05, .1],
    "model__max_leaf_nodes": [15, 31],
    "model__l2_regularization": [0., 1.],
}

if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    run_experiment("hist_gradient_boosting", ESTIMATOR, GRID,
                   folder / "gas-turbine-emissions.csv", folder / "member4_results")
