"""Read-only checks on executed exports, preserved originals and portable entries."""
from pathlib import Path
import hashlib
import json
import os
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from cw2_project import MODELS, PROTOCOL_ID, metrics, SUBMITTED


def main():
    raw_manifest = json.loads((ROOT / 'notes/received_manifest.json').read_text())
    checked_raw = 0
    for item in raw_manifest:
        raw = ROOT / item['local_location']
        # Local originals intentionally do not travel with a Git clone.
        if raw.exists():
            assert hashlib.sha256(raw.read_bytes()).hexdigest() == item['sha256']
            checked_raw += 1
    for name in MODELS:
        folder = ROOT / 'results/development' / name
        pred = pd.read_csv(folder / 'validation_predictions.csv')
        details = pd.read_csv(folder / 'fold_metrics.csv')
        summary = json.loads((folder / 'summary.json').read_text())
        assert len(pred) == 18490 and pred.source_row.is_unique
        assert pred.source_row.min() == 3701 and pred.source_row.max() == 22190
        assert len(details) == 5 and summary['protocol_id'] == PROTOCOL_ID
        for fold, block in pred.groupby('fold'):
            calculated = metrics(block.actual_co, block.predicted_co)
            supplied = details.loc[details.fold == fold].iloc[0]
            for key, value in calculated.items():
                np.testing.assert_allclose(value, supplied[f'validation_{key}'], atol=1e-12, rtol=0)
        np.testing.assert_allclose(summary['validation_mae'], details.validation_mae.mean(), atol=1e-12, rtol=0)
        if name in SUBMITTED:
            spec = json.loads((ROOT / 'results/submitted' / SUBMITTED[name] / 'model_spec.json').read_text())
            assert summary['best_params'] == spec['best_params']
        assert summary['final_test_run'] is False
    # Execute setup only; do not repeat model training or benchmarking.
    for location in [ROOT, ROOT / 'experiments', ROOT.parent]:
        os.chdir(location)
        for path in (ROOT / 'experiments').glob('*.ipynb'):
            nb = json.loads(path.read_text())
            setup = next(cell for cell in nb['cells']
                         if cell['cell_type'] == 'code'
                         and 'PROJECT = next' in ''.join(cell['source']))
            scope = {}
            exec(compile(''.join(setup['source']), str(path), 'exec'), scope)
            assert scope['PROJECT'] == ROOT
    os.chdir(ROOT)
    if (ROOT / 'results/final/metrics.json').exists():
        from cw2_submission import verify_member5, verify_final, FINAL_DIR
        verify_member5()
        lock = json.loads((ROOT / 'results/final/decision_lock.json').read_text())
        verify_final(lock)
        if (FINAL_DIR/'metrics.json').exists():
            verify_final(json.loads((FINAL_DIR/'decision_lock.json').read_text()))
        final_status = 'Original HGB and revised Extra Trees evidence and Member 5 raw timings verified.'
    else:
        final_status = 'Final assessment not yet run.'
    print(f'Passed: four-model prediction exports, latest settings, portable setup and {checked_raw} local original hashes. {final_status}')


if __name__ == '__main__':
    main()
