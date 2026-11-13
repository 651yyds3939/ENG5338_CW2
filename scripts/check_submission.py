"""Independent artifact checks: page limits, metrics, notebook errors, final evidence."""
from pathlib import Path
import json,hashlib,sys
import pymupdf as fitz
import nbformat
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'submission'
sys.path.insert(0,str(ROOT/'src'))
from cw2_submission import verify_final,verify_member5,metrics,FINAL_DIR,PRIOR_FINAL_DIR
lock=json.loads((FINAL_DIR/'decision_lock.json').read_text())
final,pred=verify_final(lock);verify_member5()
assert lock['locked_at_utc'] < final['evaluated_at_utc']
assert final['authoritative_cw2_test_prediction_calls']==1 and not final['retuned_after_test']
assert final['model']=='extra_trees' and final['cw2_distinct_models_assessed_on_this_period']==2
assert final['selection_policy_revised_after_prior_test'] and not final['independent_confirmatory_test']
verify_final(json.loads((PRIOR_FINAL_DIR/'decision_lock.json').read_text()))
for year,block in pred.groupby('year'):
 saved=next(r for r in final['by_year'] if r['year']==year)
 for k,v in metrics(block.actual_co,block.predicted_co).items():np.testing.assert_allclose(v,saved[k],atol=1e-12,rtol=0)
report=fitz.open(OUT/'ENG5338_CW2_report_GAS4.pdf');slides=fitz.open(OUT/'ENG5338_CW2_presentation_GAS4.pdf')
assert len(report)==9
assert 'Appendix' in report[7].get_text() and 'Statement of Contribution' in report[8].get_text()
assert len(slides)==11
full_report='\n'.join(p.get_text() for p in report);full_slides='\n'.join(p.get_text() for p in slides)
for metric in ['mae','rmse','r2']:
 value=f'{final["test"][metric]:.4f}'
 assert value in full_report and value in full_slides
coverage=f'{100*final["test"]["coverage"]:.2f}%'
assert coverage in full_report and coverage in full_slides
assert 'same 2014–2015' in full_report and 'same 2014–2015' in full_slides
assert 'HGB' in full_report and '0.8998' in full_report and '70.00%' in full_report
for phrase in ['1. Engineering Question','2. Experimental Design','3. Comparative Analysis','4. Recommended Pipeline','AI tools']:
 assert phrase in full_report,phrase
for path in [ROOT/'ENG5338_CW2_notebook_GAS4.ipynb',OUT/'ENG5338_CW2_notebook_GAS4.ipynb']:
 nb=nbformat.read(path,as_version=4);nbformat.validate(nb)
 cells=[c for c in nb.cells if c.cell_type=='code']
 assert all(c.execution_count is not None for c in cells)
 assert not any(o.output_type=='error' for c in cells for o in c.outputs)
assert (ROOT/'ENG5338_CW2_notebook_GAS4.ipynb').read_bytes()==(OUT/'ENG5338_CW2_notebook_GAS4.ipynb').read_bytes()
for doc in [report,slides]:
 for p in doc:
  for x0,y0,x1,y1,*rest in p.get_text('blocks'):
   assert x0>=0 and y0>=0 and x1<=p.rect.width+1 and y1<=p.rect.height+1,(p.number,x0,y0,x1,y1)
print('PASS: exact course filenames, report page allocation, slides, cross-document scores, executed notebook, timing samples and separate preserved HGB and revised Extra Trees assessments, with exposure disclosed.')
