"""Integrated development experiments. This module never evaluates the hold-out."""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
from pathlib import Path
from datetime import datetime, timezone
from importlib.metadata import version
import gc, hashlib, json, pickle, platform, sys, threading, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import psutil
from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from threadpoolctl import threadpool_info, threadpool_limits
from cw2_common import (SEED, FEATURES, DATA_SHA256, PROTOCOL, PROTOCOL_ID,
                        load_development, public_metadata, run_experiment)
ROOT = Path(__file__).resolve().parents[1]
MODELS = ['linear_reference', 'random_forest', 'extra_trees', 'hist_gradient_boosting']
SUBMITTED = {'random_forest': 'member2/latest', 'extra_trees': 'member3/latest',
             'hist_gradient_boosting': 'member4/latest'}


def write_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(public_metadata(value), indent=2, default=str) + '\n')


def runtime_record():
    cpu_path = Path('/proc/cpuinfo')
    cpu = platform.processor()
    if cpu_path.exists():
        cpu = next((s.split(':', 1)[1].strip() for s in cpu_path.read_text().splitlines()
                    if s.startswith('model name')), cpu)
    record = public_metadata({'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
        'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
        'cpu': cpu, 'logical_cpus': os.cpu_count(), 'ram_gib': psutil.virtual_memory().total / 1024**3,
        'seed': SEED, 'numerical_threads': 1, 'search_workers': 1, 'accelerator': 'CPU only',
        'versions': {p: version(p) for p in ['numpy','pandas','scipy','scikit-learn','matplotlib',
                                           'psutil','threadpoolctl','nbformat','nbclient']},
        'thread_pools': threadpool_info()})
    record['runtime_id'] = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()[:12]
    return record


def data_check(output_dir):
    """Full-file structure only; all target-distribution analysis stays in development."""
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    path = ROOT/'data/gas-turbine-emissions.csv'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == DATA_SHA256
    raw = pd.read_csv(path)
    assert raw.shape == (36733, 12) and raw.columns.tolist() == ['year', *FEATURES, 'co', 'nox']
    assert raw.year.is_monotonic_increasing and np.isfinite(raw.to_numpy()).all()
    schema = pd.DataFrame({'field': raw.columns, 'dtype': raw.dtypes.astype(str).values,
                           'missing': raw.isna().sum().values})
    schema.to_csv(output_dir/'schema.csv', index=False)
    pd.DataFrame({'source_row': raw.index, 'partition': np.where(raw.year<=2013, 'development', 'sealed_holdout')}).to_csv(output_dir/'split_manifest.csv', index=False)
    record = {'data_sha256': DATA_SHA256, 'shape': list(raw.shape),
              'missing_values': int(raw.isna().sum().sum()), 'duplicate_complete_rows': int(raw.duplicated().sum()),
              'rows_by_year': {str(k):int(v) for k,v in raw.groupby('year').size().items()},
              'prior_cw1_test_exposure': True, 'cw2_final_test_run': False}
    write_json(output_dir/'data_checks.json', record)
    del raw
    return schema, record


def model_spec(name):
    if name == 'linear_reference':
        return LinearRegression(), {}, True, {}
    folder = ROOT/'results/submitted'/SUBMITTED[name]
    spec = json.loads((folder/'model_spec.json').read_text())
    cls = {'random_forest': RandomForestRegressor, 'extra_trees': ExtraTreesRegressor,
           'hist_gradient_boosting': HistGradientBoostingRegressor}[name]
    estimator = cls(**spec['initial_estimator_params'])
    return estimator, spec['grid'], spec['scale'], spec['best_params']


def pipeline_for(name):
    estimator, grid, scale, selected = model_spec(name)
    steps = [('impute', SimpleImputer(strategy='median'))]
    if scale: steps.append(('scale', StandardScaler()))
    return Pipeline(steps + [('model', estimator)]).set_params(**selected)


def check_search_evidence(name, folds):
    folder = ROOT/'results/submitted'/SUBMITTED[name]
    spec = json.loads((folder/'model_spec.json').read_text())
    summary = json.loads((folder/'summary.json').read_text())
    protocol = json.loads((folder/'protocol.json').read_text())
    assert protocol == {**PROTOCOL, 'protocol_id': PROTOCOL_ID}
    search = pd.read_csv(folder/'search_results.csv')
    assert len(search) == summary['configurations']
    expected = pd.DataFrame([{'fold':i+1,'train_n':len(tr),'validation_n':len(va),
        'train_last_row':int(tr[-1]),'validation_first_row':int(va[0]),
        'validation_last_row':int(va[-1])} for i,(tr,va) in enumerate(folds)])
    pd.testing.assert_frame_equal(pd.read_csv(folder/'folds.csv'), expected)
    best = search.loc[search.mean_test_mae.idxmax()]
    import ast
    assert ast.literal_eval(best['params']) == spec['best_params'] == summary['best_params']
    assert np.isclose(-best.mean_test_mae, summary['validation_mae'], atol=1e-12, rtol=0)
    return {'model':name, 'configurations':len(search), 'cv_fits':len(search)*len(folds),
            'submitted_validation_mae': summary['validation_mae'],
            'source':str(folder.relative_to(ROOT)), 'selected_params':spec['best_params']}


def metrics(actual, predicted):
    error = np.asarray(predicted) - np.asarray(actual)
    return {'mae':float(mean_absolute_error(actual,predicted)),
            'rmse':float(root_mean_squared_error(actual,predicted)),
            'r2':float(r2_score(actual,predicted)),
            'coverage':float(np.mean(np.abs(error)<=PROTOCOL['tolerance'])),
            'negative_fraction':float(np.mean(np.asarray(predicted)<0))}


def evaluate_selected(name, output_dir):
    """Re-run selected settings on the common folds; do not search or open test data."""
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    with threadpool_limits(limits=1):
        X, y, folds = load_development(ROOT/'data/gas-turbine-emissions.csv')
        pipe = pipeline_for(name)
        rows, predictions = [], []
        for i,(tr,va) in enumerate(folds,1):
            fitted = clone(pipe).fit(X.iloc[tr],y.iloc[tr])
            train = metrics(y.iloc[tr],fitted.predict(X.iloc[tr])); pred=fitted.predict(X.iloc[va])
            valid = metrics(y.iloc[va],pred)
            row={'model':name,'fold':i,'protocol_id':PROTOCOL_ID}
            row.update({f'train_{k}':v for k,v in train.items()})
            row.update({f'validation_{k}':v for k,v in valid.items()})
            row['mae_gap']=valid['mae']-train['mae']; rows.append(row)
            predictions.append(pd.DataFrame({'source_row':X.index[va], 'fold':i,
                'actual_co':y.iloc[va].to_numpy(),'predicted_co':pred,
                'training_q75':float(y.iloc[tr].quantile(.75)),
                'training_q95':float(y.iloc[tr].quantile(.95))}))
            print(f'{name}: completed development fold {i}/5', flush=True)
        detail=pd.DataFrame(rows); oof=pd.concat(predictions,ignore_index=True)
        detail.to_csv(output_dir/'fold_metrics.csv',index=False)
        oof.to_csv(output_dir/'validation_predictions.csv',index=False)
        summary={'model':name,'status':'RUN: selected configuration, development only',
            'protocol_id':PROTOCOL_ID,'best_params':model_spec(name)[3],
            **{k:float(detail[k].mean()) for k in detail if k.startswith(('train_','validation_')) or k=='mae_gap'},
            'validation_mae_sd':float(detail.validation_mae.std(ddof=0)),
            'worst_fold_coverage':float(detail.validation_coverage.min()), 'final_test_run':False}
        write_json(output_dir/'summary.json',summary)
        return summary, detail, oof


def make_diagnostics(name, detail, oof, figure_dir):
    figure_dir=Path(figure_dir);figure_dir.mkdir(parents=True,exist_ok=True)
    fig,axes=plt.subplots(1,3,figsize=(14,3.8))
    axes[0].plot(detail.fold,detail.train_mae,'o-',label='Training')
    axes[0].plot(detail.fold,detail.validation_mae,'o-',label='Validation')
    axes[0].set(xlabel='Chronological fold',ylabel='MAE (mg/m³)');axes[0].legend()
    axes[1].plot(detail.fold,detail.validation_coverage,'o-')
    axes[1].axhline(.9,color='red',linestyle='--',label='Project target')
    axes[1].set(xlabel='Chronological fold',ylabel='Coverage within ±1 mg/m³',ylim=(0,1));axes[1].legend()
    axes[2].scatter(oof.actual_co,oof.predicted_co,s=5,alpha=.18)
    lo=min(oof.actual_co.min(),oof.predicted_co.min());hi=max(oof.actual_co.max(),oof.predicted_co.max())
    axes[2].plot([lo,hi],[lo,hi],'k--');axes[2].set(xlabel='Actual CO (mg/m³)',ylabel='Predicted CO (mg/m³)',xlim=(lo,hi),ylim=(lo,hi))
    fig.suptitle(name);fig.tight_layout();fig.savefig(figure_dir/f'{name}_validation.png',dpi=160)
    return fig


def high_co_diagnostics(oof):
    """Thresholds from each training fold; diagnostic groups, not deployable routing rules."""
    err=oof.predicted_co-oof.actual_co
    masks={'all_validation':np.ones(len(oof),dtype=bool),
           'above_training_q75':oof.actual_co>oof.training_q75,
           'above_training_q95':oof.actual_co>oof.training_q95}
    return pd.DataFrame([{'group':key,'rows':int(np.sum(mask)),
        'mae':float(np.abs(err[mask]).mean()), 'coverage':float((np.abs(err[mask])<=1).mean()),
        'mean_prediction_minus_actual':float(err[mask].mean())} for key,mask in masks.items()])


def rerun_submitted_search(name, output_dir):
    estimator, grid, scale, _ = model_spec(name)
    return run_experiment(name,estimator,grid,ROOT/'data/gas-turbine-emissions.csv',output_dir,scale)


def benchmark_all(output_dir, measured_by="Unspecified runner; record before final reporting"):
    """Member 5 entry: all four complete pipelines on one runtime, development only."""
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    with threadpool_limits(limits=1):
        runtime=runtime_record();runtime['measured_by']=measured_by;write_json(output_dir/'runtime.json',runtime)
        X,y,_=load_development(ROOT/'data/gas-turbine-emissions.csv')
        batch=X.iloc[-1000:].copy();single=batch.iloc[[0]].copy();records=[]
        def sample(operation,repeats,warmups=1):
            for _ in range(warmups):operation()
            vals=[]
            for _ in range(repeats):
                start=time.perf_counter();operation();vals.append(time.perf_counter()-start)
            return vals
        for name in MODELS:
            pipe=pipeline_for(name)
            fits=sample(lambda:clone(pipe).fit(X,y),3)
            fitted=clone(pipe).fit(X,y)
            batches=sample(lambda:fitted.predict(batch),10,3)
            singles=sample(lambda:fitted.predict(single),100,5)
            gc.collect();process=psutil.Process();baseline=process.memory_info().rss;peak=[baseline];stop=threading.Event()
            def watch():
                while not stop.is_set():
                    peak[0]=max(peak[0],process.memory_info().rss);stop.wait(.005)
            watcher=threading.Thread(target=watch,daemon=True);watcher.start()
            try:
                memory_fit=clone(pipe).fit(X,y);peak[0]=max(peak[0],process.memory_info().rss)
            finally:stop.set();watcher.join()
            record={'model':name,'protocol_id':PROTOCOL_ID,'runtime_id':runtime['runtime_id'],
                'measured_by':measured_by,
                'fit_median_s':float(np.median(fits)), 'single_median_ms':float(np.median(singles)*1000),
                'single_p95_ms':float(np.quantile(singles,.95)*1000),
                'batch_1000_median_ms':float(np.median(batches)*1000),
                'batch_amortised_us_per_row':float(np.median(batches)*1e6/len(batch)),
                'fit_sampled_rss_increment_mib':(peak[0]-baseline)/1024**2,
                'serialized_pipeline_kib':len(pickle.dumps(fitted))/1024,
                'fit_samples_s':fits,'single_samples_s':singles,'batch_samples_s':batches,
                'train_rows':len(X),'batch_rows':len(batch),'best_params':model_spec(name)[3],
                'memory_method':'RSS increment, separate fit, ~5 ms sampling; allocator reuse may hide peaks',
                'final_test_run':False}
            write_json(output_dir/f'{name}.json',record);records.append(record)
            print(f'Cost measurement complete: {name}',flush=True)
            del fitted,memory_fit
        table=pd.DataFrame(records).drop(columns=['fit_samples_s','single_samples_s','batch_samples_s','best_params'])
        table.to_csv(output_dir/'comparison.csv',index=False)
        return table
