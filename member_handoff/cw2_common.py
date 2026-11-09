"""Shared GAS4 protocol. Model owners should edit their experiment file only."""
import os
for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[variable] = "1"

import hashlib
import json
import platform
import sys
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_info, threadpool_limits

SEED = 42
FEATURES = ["at", "ap", "ah", "afdp", "gtep", "tit", "tat", "tey", "cdp"]
DATA_SHA256 = "6295ecd391e757ab5e029bdb54aee607887374861f656a26281b5a0e4e524b85"
PROTOCOL = {
    "target": "co", "features": FEATURES, "data_sha256": DATA_SHA256,
    "development_years": [2011, 2012, 2013], "sealed_holdout_years": [2014, 2015],
    "seed": SEED, "folds": 5, "gap_rows": 24, "primary_metric": "MAE",
    "tolerance": 1.0, "min_coverage": 0.90, "max_median_single_ms": 10.0,
    "group_approved": False,
}
PROTOCOL_ID = hashlib.sha256(json.dumps(PROTOCOL, sort_keys=True).encode()).hexdigest()[:12]


def coverage(y_true, y_pred):
    return float(np.mean(np.abs(np.asarray(y_true) - y_pred) <= PROTOCOL["tolerance"]))


def negative_fraction(y_true, y_pred):
    return float(np.mean(np.asarray(y_pred) < 0))


SCORING = {
    "mae": "neg_mean_absolute_error", "rmse": "neg_root_mean_squared_error", "r2": "r2",
    "coverage": make_scorer(coverage),
    "negative_fraction": make_scorer(negative_fraction, greater_is_better=False),
}


def load_development(data_path):
    data_path = Path(data_path)
    if not data_path.is_file():
        # A Git checkout shares one CSV under data/; standalone ZIPs keep it beside this module.
        repository_data = Path(__file__).resolve().parent.parent / "data/gas-turbine-emissions.csv"
        if repository_data.is_file():
            data_path = repository_data
    assert hashlib.sha256(data_path.read_bytes()).hexdigest() == DATA_SHA256, "Unexpected dataset."
    raw = pd.read_csv(data_path)
    assert raw.shape == (36733, 12) and raw.year.is_monotonic_increasing
    assert raw.columns.tolist() == ["year", *FEATURES, "co", "nox"]
    assert np.isfinite(raw.to_numpy()).all()
    development = raw.loc[raw.year.isin(PROTOCOL["development_years"])].copy()
    del raw  # No held-out features or targets are returned.
    assert len(development) == 22191
    X, y = development[FEATURES], development[PROTOCOL["target"]]
    folds = list(TimeSeriesSplit(n_splits=5, gap=24).split(X))
    return X, y, folds


def public_metadata(value):
    """Keep runtime evidence while removing the local home-directory identity."""
    if isinstance(value, dict):
        return {key: public_metadata(item) for key, item in value.items()}
    if isinstance(value, list):
        return [public_metadata(item) for item in value]
    if isinstance(value, str):
        return value.replace(str(Path.home()), "<home>")
    return value


def save_json(path, value):
    Path(path).write_text(json.dumps(public_metadata(value), indent=2, default=str) + "\n")


def run_experiment(name, estimator, grid, data_path, output_dir, scale=False):
    """Tune on development data only and export artifacts for Wenyi to integrate.

    Local fit times are diagnostic. Member 5 must measure all models on one runtime
    before the group makes comparative computational-efficiency claims.
    """
    np.random.seed(SEED)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with threadpool_limits(limits=1):
        X, y, folds = load_development(data_path)
        steps = [("impute", SimpleImputer(strategy="median"))]
        if scale:
            steps.append(("scale", StandardScaler()))
        pipeline = Pipeline(steps + [("model", estimator)])
        search = GridSearchCV(pipeline, grid, cv=folds, scoring=SCORING,
                              refit="mae", return_train_score=True, n_jobs=1, error_score="raise")
        started = time.perf_counter()
        search.fit(X, y)
        elapsed = time.perf_counter() - started
        results = pd.DataFrame(search.cv_results_)
        results.to_csv(output_dir / "search_results.csv", index=False)
        best = results.iloc[search.best_index_]
        records = []
        for fold in range(len(folds)):
            record = {"model": name, "fold": fold + 1, "protocol_id": PROTOCOL_ID}
            for subset, key in [("train", "train"), ("validation", "test")]:
                for metric in SCORING:
                    sign = -1 if metric in {"mae", "rmse", "negative_fraction"} else 1
                    record[f"{subset}_{metric}"] = float(sign * best[f"split{fold}_{key}_{metric}"])
            record["mae_gap"] = record["validation_mae"] - record["train_mae"]
            records.append(record)
        details = pd.DataFrame(records)
        details.to_csv(output_dir / "fold_metrics.csv", index=False)
        summary = {
            "model": name, "protocol_id": PROTOCOL_ID, "status": "RUN: development only",
            "best_params": search.best_params_, "train_mae": details.train_mae.mean(),
            "validation_mae": details.validation_mae.mean(),
            "validation_mae_sd": details.validation_mae.std(ddof=0),
            "validation_rmse": details.validation_rmse.mean(), "validation_r2": details.validation_r2.mean(),
            "validation_coverage": details.validation_coverage.mean(),
            "worst_fold_coverage": details.validation_coverage.min(), "mae_gap": details.mae_gap.mean(),
            "configurations": len(results), "cv_fits": len(results) * len(folds),
            "search_wall_s_local_only": elapsed,
        }
        runtime = {
            "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
            "processor": platform.processor(), "logical_cpus": os.cpu_count(),
            "versions": {p: version(p) for p in ("numpy", "pandas", "scipy", "scikit-learn", "threadpoolctl")},
            "seed": SEED, "search_workers": 1, "numerical_threads": 1, "thread_pools": threadpool_info(),
        }
        save_json(output_dir / "summary.json", summary)
        save_json(output_dir / "runtime.json", runtime)
        save_json(output_dir / "protocol.json", {**PROTOCOL, "protocol_id": PROTOCOL_ID})
        save_json(output_dir / "model_spec.json", {
            "model": name, "estimator_class": f"{type(estimator).__module__}.{type(estimator).__name__}",
            "initial_estimator_params": estimator.get_params(deep=False), "scale": scale,
            "grid": grid, "best_params": search.best_params_, "protocol_id": PROTOCOL_ID,
            "shared_module_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        })
        manifest = []
        for number, (train, val) in enumerate(folds, 1):
            manifest.append({"fold": number, "train_n": len(train), "validation_n": len(val),
                "train_last_row": int(X.index[train[-1]]),
                "validation_first_row": int(X.index[val[0]]), "validation_last_row": int(X.index[val[-1]])})
        pd.DataFrame(manifest).to_csv(output_dir / "folds.csv", index=False)
    print(json.dumps(summary, indent=2, default=str))
    print(f"Results folder: {output_dir.name}; no final test evaluation performed.")
    return summary
