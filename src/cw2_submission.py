"""Submission evidence: verify member costs, lock a decision, evaluate it once.

The authoritative hold-out prediction is cached. Notebook reruns verify that cache;
an explicit reproducibility replay never changes the decision or original record.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import time
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import clone
from threadpoolctl import threadpool_limits
from cw2_project import (ROOT, MODELS, PROTOCOL, PROTOCOL_ID, DATA_SHA256,
                         FEATURES, pipeline_for, metrics, runtime_record, write_json)

LABELS = dict(zip(MODELS, ['OLS', 'Random Forest', 'Extra Trees', 'HGB']))
FINAL_MODEL = 'extra_trees'
FINAL_DIR = ROOT / 'results/final_extra_trees'
PRIOR_FINAL_DIR = ROOT / 'results/final'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_member5():
    folder = ROOT / 'results/member5_local_py310'
    costs = pd.read_csv(folder / 'comparison.csv')
    runtime = json.loads((folder / 'runtime.json').read_text())
    assert set(costs.model) == set(MODELS) and len(costs) == 4
    for name in MODELS:
        rec = json.loads((folder / f'{name}.json').read_text())
        row = costs.set_index('model').loc[name]
        assert rec['protocol_id'] == PROTOCOL_ID
        assert rec['runtime_id'] == runtime['runtime_id'] == row.runtime_id
        assert rec['train_rows'] == 22191 and rec['final_test_run'] is False
        for key, samples, factor in [
            ('fit_median_s', 'fit_samples_s', 1),
            ('single_median_ms', 'single_samples_s', 1000),
            ('batch_1000_median_ms', 'batch_samples_s', 1000)]:
            value = float(np.median(rec[samples]) * factor)
            np.testing.assert_allclose(value, rec[key], atol=1e-10, rtol=0)
            np.testing.assert_allclose(value, row[key], atol=1e-10, rtol=0)
        np.testing.assert_allclose(np.quantile(rec['single_samples_s'], .95)*1000,
                                   rec['single_p95_ms'], atol=1e-10, rtol=0)
        params = pipeline_for(name).get_params()
        assert all(params[k] == v for k, v in rec['best_params'].items())
    return costs, runtime


def comparison_table():
    perf = pd.read_csv(ROOT / 'results/development/comparison.csv')
    costs, runtime = verify_member5()
    cols = ['model', 'fit_median_s', 'single_median_ms', 'single_p95_ms',
            'batch_1000_median_ms', 'serialized_pipeline_kib',
            'fit_sampled_rss_increment_mib', 'runtime_id']
    table = perf.merge(costs[cols].rename(columns={'runtime_id':'cost_runtime_id'}),
                       on='model', validate='one_to_one')
    table['coverage_percent'] = 100 * table.validation_coverage
    table['coverage_pass'] = table.validation_coverage >= PROTOCOL['min_coverage']
    table['latency_pass'] = table.single_median_ms <= PROTOCOL['max_median_single_ms']
    table['both_pass'] = table.coverage_pass & table.latency_pass
    return table


def decision_lock():
    """Record the user's accuracy-first revision before the Extra Trees assessment.

HGB's earlier outcomes are already visible. This is explicitly not a new blind test.
The original protocol/timing benchmark is retained rather than silently rewritten.
    """
    path = FINAL_DIR / 'decision_lock.json'
    if path.exists():
        record = json.loads(path.read_text())
        assert record['model'] == FINAL_MODEL
        return record
    table = comparison_table()
    assert not table.coverage_pass.any(), 'Reassess decision before opening the test.'
    assert table.sort_values('validation_mae').iloc[0].model == FINAL_MODEL
    name = FINAL_MODEL
    prior_lock = json.loads((PRIOR_FINAL_DIR/'decision_lock.json').read_text())
    prior_result, _ = verify_final(prior_lock)
    params = pipeline_for(name).get_params()['model'].get_params(deep=False)
    inputs = {
        'results/development/comparison.csv':'development_comparison.csv',
        'results/member5_local_py310/comparison.csv':'windows_cost_comparison.csv',
        'results/submitted/member3/latest/model_spec.json':'extra_trees_model_spec.json'}
    evidence_dir = path.parent/'selection_inputs'
    evidence_dir.mkdir(parents=True, exist_ok=True)
    for source, filename in inputs.items():
        shutil.copy2(ROOT/source, evidence_dir/filename)
    record = {
        'locked_at_utc': datetime.now(timezone.utc).isoformat(),
        'model': name, 'protocol_id': PROTOCOL_ID, 'data_sha256': DATA_SHA256,
        'estimator_params': params, 'preprocessing': 'median imputer; no scaling',
        'selection_authority': 'Wenyi explicitly requested switching to the model with better predictive accuracy after reviewing the HGB choice and result on 2026-11-13',
        'group_endorsement_claimed': False,
        'decision': 'Extra Trees has the lowest existing development-validation MAE and highest development coverage. Accuracy now has priority; 10 ms is retained as a historical reference, not a hard acceptance gate. The 90% coverage target remains unchanged and unmet in development; deployment approval is withheld.',
        'selection_metric': 'existing development-validation MAE',
        'constraints_changed': True, 'holdout_consulted_for_selection': True,
        'selection_policy_revised_after_prior_test': True,
        'original_latency_gate_replaced_by_descriptive_cost_comparison': True,
        'prior_hgb_result_visible': True,
        'prior_hgb_metrics_sha256': digest(PRIOR_FINAL_DIR/'metrics.json'),
        'prior_hgb_evaluated_at_utc': prior_result['evaluated_at_utc'],
        'exposure_disclosure': 'The policy was revised after HGB results were known. Extra Trees is chosen from pre-existing development scores, but the reused 2014–2015 period is not an independent confirmatory test. Prior CW1 exposure also applies.',
        'prior_cw1_test_exposure': True,
        'decision_inputs_sha256': {
            str((evidence_dir/filename).relative_to(ROOT)):digest(ROOT/source)
            for source, filename in inputs.items()},
        'original_selection_input_paths': list(inputs),
        'development_evidence': table.drop(columns=['runtime_id']).to_dict('records')}
    write_json(path, record)
    return record


def verify_final(record):
    folder = (PRIOR_FINAL_DIR if record['model']=='hist_gradient_boosting' else FINAL_DIR)
    saved = json.loads((folder/'metrics.json').read_text())
    assert saved['decision_lock_sha256'] == digest(folder/'decision_lock.json')
    assert saved['predictions_sha256'] == digest(folder/'predictions.csv')
    assert saved['model'] == record['model']
    for source, sha in record['decision_inputs_sha256'].items():
        assert digest(ROOT/source) == sha
    assert digest(ROOT/'data/gas-turbine-emissions.csv') == record['data_sha256']
    pred = pd.read_csv(folder/'predictions.csv')
    assert len(pred) == 14542 and pred.source_row.is_unique
    assert set(pred.year) == {2014, 2015}
    for k,v in metrics(pred.actual_co,pred.predicted_co).items():
        np.testing.assert_allclose(v, saved['test'][k], atol=1e-12, rtol=0)
    current = pipeline_for(record['model']).named_steps['model'].get_params(deep=False)
    assert current == record['estimator_params'], 'Locked model configuration changed.'
    if record['model'] == FINAL_MODEL:
        assert digest(PRIOR_FINAL_DIR/'metrics.json') == record['prior_hgb_metrics_sha256']
        assert saved['selection_policy_revised_after_prior_test'] is True
        assert saved['independent_confirmatory_test'] is False
    return saved, pred


def evaluate_final_once():
    record = decision_lock()
    folder = FINAL_DIR
    if (folder/'metrics.json').exists():
        result, pred = verify_final(record)
        print('Verified saved assessment metrics and loaded predictions.')
        return result, pred
    if (folder/'evaluation_started.json').exists():
        raise RuntimeError('An evaluation was already started. Inspect saved evidence before rerunning.')
    for source, sha in record['decision_inputs_sha256'].items():
        assert digest(ROOT/source) == sha, f'Changed selection input: {source}'
    assert digest(ROOT/'data/gas-turbine-emissions.csv') == DATA_SHA256
    with threadpool_limits(limits=1):
        runtime = runtime_record()
        write_json(folder/'runtime.json', runtime)
        write_json(folder/'evaluation_started.json', {
            'started_at_utc':datetime.now(timezone.utc).isoformat(),
            'decision_lock_sha256':digest(folder/'decision_lock.json'),
            'performed_by':'Codex, under Wenyi\'s explicit completion instruction; not a Member 5 run'})
        raw = pd.read_csv(ROOT/'data/gas-turbine-emissions.csv')
        dev = raw[raw.year.isin(PROTOCOL['development_years'])]
        test = raw[raw.year.isin(PROTOCOL['sealed_holdout_years'])]
        assert len(dev)==22191 and len(test)==14542
        pipe = clone(pipeline_for(record['model']))
        start=time.perf_counter();pipe.fit(dev[FEATURES], dev.co);fit_s=time.perf_counter()-start
        # One Extra Trees assessment after the revised lock; HGB was assessed earlier.
        predicted = pipe.predict(test[FEATURES])
        pred = pd.DataFrame({'source_row':test.index,'year':test.year,
            'actual_co':test.co,'predicted_co':predicted})
        pred.to_csv(folder/'predictions.csv',index=False)
        q95 = float(dev.co.quantile(.95))
        tail = pred.actual_co > q95
        yearly = [{'year':int(year),'rows':len(block),**metrics(block.actual_co,block.predicted_co)}
                  for year, block in pred.groupby('year')]
        pd.DataFrame(yearly).to_csv(folder/'by_year.csv',index=False)
        result = {
            'model':record['model'],'protocol_id':PROTOCOL_ID,
            'evaluated_at_utc':datetime.now(timezone.utc).isoformat(),
            'performed_by':'Codex under Wenyi\'s instruction; Member 5 supplied development cost measurements',
            'decision_lock_sha256':digest(folder/'decision_lock.json'),
            'predictions_sha256':digest(folder/'predictions.csv'),
            'runtime_id':runtime['runtime_id'],'development_rows':len(dev),'test_rows':len(test),
            'training':metrics(dev.co,pipe.predict(dev[FEATURES])),
            'test':metrics(test.co,predicted),'by_year':yearly,
            'training_q95':q95,'tail_rows':int(tail.sum()),
            'tail_test':metrics(pred.loc[tail,'actual_co'],pred.loc[tail,'predicted_co']),
            'test_mean_prediction_minus_actual':float((pred.predicted_co-pred.actual_co).mean()),
            'tail_mean_prediction_minus_actual':float((pred.loc[tail,'predicted_co']-pred.loc[tail,'actual_co']).mean()),
            'negative_predictions':int((pred.predicted_co<0).sum()),
            'fit_s_single_run_not_benchmark':fit_s,
            'authoritative_cw2_test_prediction_calls':1,'retuned_after_test':False,
            'prediction_count_scope':'One Extra Trees assessment; original HGB assessment is separately preserved',
            'cw2_distinct_models_assessed_on_this_period':2,
            'selection_policy_revised_after_prior_test':True,
            'independent_confirmatory_test':False,
            'prior_hgb_result_visible':True,
            'assessment_status':'Secondary assessment on previously exposed 2014–2015 data; no independent confirmation available',
            'deployment_approved':False,'prior_cw1_test_exposure':True}
        write_json(folder/'metrics.json',result)
    print('Completed Extra Trees assessment and saved metrics. HGB history is retained.')
    return verify_final(record)


def replay_fixed_final():
    """Explicit reproducibility replay; never overwrite the authoritative evidence."""
    record = json.loads((FINAL_DIR/'decision_lock.json').read_text())
    result, original = verify_final(record)
    with threadpool_limits(limits=1):
        raw = pd.read_csv(ROOT/'data/gas-turbine-emissions.csv')
        dev=raw[raw.year<=2013]; test=raw[raw.year>=2014]
        fitted=clone(pipeline_for(record['model'])).fit(dev[FEATURES],dev.co)
        np.testing.assert_allclose(fitted.predict(test[FEATURES]), original.predicted_co,
                                   rtol=1e-10,atol=1e-10)
    print('Explicit replay reproduced the same fixed-model test predictions; original evidence unchanged.')


def submission_figures(table, pred):
    folder=ROOT/'figures/submission';folder.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(8.4,4.1))
    for row in table.itertuples():
        ax.scatter(row.single_median_ms,row.validation_mae,s=110,
                   color='#168879' if row.model==FINAL_MODEL else '#275878')
        ax.annotate(LABELS[row.model],(row.single_median_ms,row.validation_mae),
                    xytext=(7,6),textcoords='offset points')
    ax.axvline(10,c='#b55145',ls='--',label='Original 10 ms reference')
    ax.set(xlabel='Member 5 Windows median single-row latency (ms)',
           ylabel='Mean development-validation MAE (mg/m³)',xlim=(-1,34),ylim=(.69,.94))
    ax.legend(loc='upper right');fig.tight_layout();fig.savefig(folder/'accuracy_cost.png',dpi=190);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(9.2,3.6))
    for name in MODELS:
        d=pd.read_csv(ROOT/f'results/development/{name}/fold_metrics.csv')
        axes[0].plot(d.fold,d.validation_mae,'o-',label=LABELS[name])
        axes[1].plot(d.fold,100*d.validation_coverage,'o-')
    axes[0].set(xlabel='Expanding chronological fold',ylabel='Validation MAE (mg/m³)')
    axes[0].legend(fontsize=8);axes[1].axhline(90,c='#b55145',ls='--')
    axes[1].set(xlabel='Expanding chronological fold',ylabel='Coverage within ±1 mg/m³ (%)',ylim=(50,100))
    fig.tight_layout();fig.savefig(folder/'temporal_validation.png',dpi=190);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(9.2,3.8))
    axes[0].hexbin(pred.actual_co,pred.predicted_co,gridsize=44,mincnt=1,bins='log',cmap='viridis')
    hi=max(pred.actual_co.max(),pred.predicted_co.max());axes[0].plot([0,hi],[0,hi],'k--',lw=1)
    axes[0].set(xlabel='Measured CO (mg/m³)',ylabel='Extra Trees prediction (mg/m³)',xlim=(0,hi),ylim=(0,hi))
    residual=pred.predicted_co-pred.actual_co
    axes[1].scatter(pred.actual_co,residual,s=4,alpha=.2,color='#275878')
    axes[1].axhline(0,c='black',lw=1);axes[1].axhline(-1,c='#b55145',ls='--');axes[1].axhline(1,c='#b55145',ls='--')
    axes[1].set(xlabel='Measured CO (mg/m³)',ylabel='Prediction − measured (mg/m³)')
    fig.tight_layout();fig.savefig(folder/'final_diagnostics.png',dpi=190);plt.close(fig)
    return folder
