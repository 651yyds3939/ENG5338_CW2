"""Assemble local course upload files, a reproducibility ZIP and hash audit."""
from pathlib import Path
import hashlib,json,shutil,zipfile
import nbformat
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'submission'
NOTE='ENG5338_CW2_notebook_GAS4.ipynb'
shutil.copy2(ROOT/NOTE,OUT/NOTE)
nb=nbformat.read(OUT/NOTE,as_version=4)
assert all(c.execution_count is not None for c in nb.cells if c.cell_type=='code')
assert not any(o.output_type=='error' for c in nb.cells if c.cell_type=='code' for o in c.outputs)
# IDs appear in the local report, not in code/results uploaded to public GitHub.
readme='''提交三份文件（每组一套）：
1. ENG5338_CW2_report_GAS4.pdf
2. ENG5338_CW2_presentation_GAS4.pdf
3. ENG5338_CW2_notebook_GAS4.ipynb

其他文件：
- .pptx：可编辑幻灯片，提交时用 PDF。
- presentation_notes.md：约 10 分钟讲稿。
- viva_preparation.md：问答准备。
- ENG5338_CW2_reproducibility_GAS4.zip：完整复现项目的支撑文件，Notebook 单独上传后若需重跑可解压此包。
- report_content.md：报告文字源。
- submission_audit.json：页数、执行、指标与哈希检查。

还需要你们自己完成：
- 五位成员学号已补齐，统一使用 7 位数字。
- 全员核对并确认贡献声明，再上传。
- Moodle 上传与同伴评价、现场展示和答辩。

发布状态：待推送 GitHub、待上传 Moodle。此文件夹保存含学号的课程提交文件。
'''
(OUT/'先看这里.txt').write_text(readme)
(OUT/'viva_preparation.md').write_text("# GAS4 — Q&A preparation\n\n1. **What is predicted?** Contemporaneous CO in mg/m³ from nine ambient/process inputs. TEY is an input; year determines the partition.\n2. **How is validation organised?** Five expanding chronological folds fit earlier rows and validate on 3,698 later observations each, with a 24-row gap. Preprocessing fits the training fold.\n3. **Why MAE and coverage?** MAE measures absolute error in physical units. Coverage measures the fraction within ±1 mg/m³. The project target is 90%.\n4. **Why Extra Trees?** It has the lowest development-validation MAE (0.7226) and highest coverage (81.76%). Its measured single-row latency is 19.03 ms.\n5. **What does the training–validation gap show?** Extra Trees training MAE is 0.4093 and validation MAE 0.7226. The difference is 0.3133. Error also varies across chronological periods.\n6. **What happens at high CO?** For validation rows above their training-fold 95th percentile, Extra Trees coverage is 26.68% and mean signed error is −1.9672 mg/m³. High-CO examples are a priority for further development.\n7. **How were costs measured?** Member 5 used one Windows laptop, one numerical thread, fixed inputs, warm-ups and repeated measurements: three fits, 100 single-row timings and ten batch timings. RSS was sampled about every 5 ms. Accuracy was computed on the shared Linux environment.\n8. **What is the assessment history?** HGB was assessed first: MAE 0.8998 and coverage 70.00%. After reviewing that result, the selection prioritised development MAE and chose Extra Trees. Both models were assessed on the same 2014–2015 rows; CW1 also used those years. Both records are saved. A new future period supplies the next confirmation stage.\n9. **What are the Extra Trees assessment results?** MAE 0.8011 mg/m³, RMSE 1.3654 mg/m³, R² 0.6111 and coverage 73.36%. The coverage gap to the target is 16.64 percentage points.\n10. **What are the next steps?** Collect representative high-CO data, test sensor/history features, assess a new future period, and measure robustness, drift and end-to-end timing.\n11. **How are results reproduced?** Run the whole project with requirements.lock.txt. The notebook performs common validation and verifies saved search, cost and assessment evidence. Switches enable grid and fixed-model replay.\n12. **Who contributed?** Wenyi coordinated the shared workflow; Jiaqi supplied RF experiments; Sirawich supplied Extra Trees experiments; Hansini supplied HGB experiments; Sauhandikaa supplied Windows costs. Codex/ChatGPT assisted code, assessments, analysis and document drafting. The report records each member's AI use and writing contribution.\n\nPrepare a 10-minute presentation and practise whole-notebook questions. Contribution review awaits all members. Sources: course brief/template, dataset DOI 10.24432/C5WC95, scikit-learn documentation.\n")
files=[ROOT/NOTE,ROOT/'README.md',ROOT/'requirements.lock.txt',ROOT/'run_notebook.py',ROOT/'model_plan.json',ROOT/'TASK_ALLOCATION.md']
for folder in ['src','data','results','figures','experiments','notes','docs/en','docs/zh']:
 for f in (ROOT/folder).rglob('*'):
  if f.is_file() and '__pycache__' not in f.parts and f.suffix not in {'.pyc','.pyo'}:files.append(f)
files.extend([ROOT/'scripts/verify_integration.py',ROOT/'docs/coursework/coursework brief2.pdf'])
archive=OUT/'ENG5338_CW2_reproducibility_GAS4.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for f in files:
  if any(s in f.parts for s in ['.git','.local_private','member_runs','search_reruns']):continue
  z.write(f,'ENG5338_CW2/'+str(f.relative_to(ROOT)))
 with_name='ENG5338_CW2/REPRODUCTION.txt'
 z.writestr(with_name,'Install requirements.lock.txt in a Python environment, then execute python run_notebook.py from ENG5338_CW2/. Keep this whole directory; notebook imports src and reads data/results. Cached final evidence is checked by default. Windows timing evidence retains original measurements.\n')
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
execution=json.loads((ROOT/'results/submission/notebook_execution.json').read_text())
assert execution['notebook_sha256']==hashlib.sha256((OUT/NOTE).read_bytes()).hexdigest()
audit={'course_files':[f'ENG5338_CW2_{kind}_GAS4.{suffix}' for kind,suffix in [('report','pdf'),('presentation','pdf'),('notebook','ipynb')]],
 'documents':json.loads((OUT/'document_audit.json').read_text()),'notebook':execution,
 'final_model':json.loads((ROOT/'results/final_extra_trees/metrics.json').read_text()),
 'sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in OUT.iterdir() if f.is_file() and f.suffix in {'.pdf','.pptx','.ipynb','.zip'}},
 'member5_id':json.loads((ROOT/'.local_private/submission_identity.json').read_text())['members'][4]['student_id'],
 'human_contribution_review':"Awaiting all members' confirmation before upload",
 'selection_policy_revised_after_prior_test':True,'independent_confirmatory_test':False,
 'prior_hgb_metrics':json.loads((ROOT/'results/final/metrics.json').read_text()),
 'moodle_submitted':False,'github_pushed':False}
(OUT/'submission_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print('Packaged three course files, editable sources, Q&A notes and complete reproducibility ZIP.')
