"""Build course PDFs and editable slides from verified notebook evidence.

No training or test-set prediction is performed by this document builder.
Student identities and deliverables remain in ignored local storage.
"""
from pathlib import Path
from io import BytesIO
import json, hashlib, html, re
import pymupdf as fitz
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from matplotlib import get_data_path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'submission';OUT.mkdir(exist_ok=True)
E=json.loads((ROOT/'results/submission/evidence.json').read_text())
IDENT=json.loads((ROOT/'.local_private/submission_identity.json').read_text())
T=pd.DataFrame(E['comparison']).set_index('model')
F=E['final']; TEST=F['test']; H=T.loc['hist_gradient_boosting']; ET=T.loc['extra_trees']; S=ET; PRIOR=E['prior_hgb']
NAMES={'linear_reference':'OLS','random_forest':'Random Forest','extra_trees':'Extra Trees','hist_gradient_boosting':'HGB'}
ORDER=list(NAMES)
figdir=ROOT/'figures/submission'
REPO='https://github.com/651yyds3939/ENG5338_CW2'
for name,file in [('Body','DejaVuSerif.ttf'),('BodyBold','DejaVuSerif-Bold.ttf'),('UI','DejaVuSans.ttf'),('UIBold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path(get_data_path())/'fonts/ttf'/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
pdfmetrics.registerFontFamily('UI',normal='UI',bold='UIBold',italic='UI',boldItalic='UIBold')
INK=colors.HexColor('#172b3b');BLUE=colors.HexColor('#245876');TEAL=colors.HexColor('#168879')
PALE=colors.HexColor('#edf3f6');RED=colors.HexColor('#a94a3c')
W,HGT=595.276,841.89;M=70.866;CW=W-2*M
AUDIT=[];PROSE=[]
C=canvas.Canvas(str(OUT/'ENG5338_CW2_report_GAS4.pdf'),pagesize=(W,HGT))
C.setTitle('ENG5338 Coursework 2 — GAS4: Gas-turbine CO estimation')
C.setAuthor('GAS4')
y=0;page=0

def para(text,size=11,leading=14.4,after=8):
    global y
    p=Paragraph(text,ParagraphStyle('body',fontName='Body',fontSize=size,leading=leading,textColor=INK))
    _,height=p.wrap(CW,900)
    assert y+height<HGT-M+6,(page,y,height,text[:70])
    p.drawOn(C,M,HGT-y-height);AUDIT.append({'page':page,'kind':'paragraph','top':y,'height':height})
    y+=height+after;PROSE.append(re.sub('<[^>]+>','',text))

def heading(text,size=14):
    global y
    para('<b>'+text+'</b>',size,size*1.23,9)

def new_page(title,kind='main'):
    global y,page
    if page:C.showPage()
    page+=1;y=M
    C.setFillColor(BLUE);C.setFont('UI',8)
    C.drawString(M,HGT-38,'ENG5338 CW2  |  GAS4  |  CO virtual sensor')
    C.setFont('UI',8.5);C.drawCentredString(W/2,34,f'{page}  •  {kind}')
    heading(title,15)

def table(data,widths=None,size=8.5):
    global y
    if widths is None:widths=[CW/len(data[0])]*len(data[0])
    style=ParagraphStyle('table',fontName='UI',fontSize=size,leading=size*1.27,textColor=INK)
    headstyle=ParagraphStyle('tablehead',parent=style,textColor=colors.white,fontName='UIBold')
    rows=[[Paragraph(html.escape(str(v)),headstyle if i==0 else style) for v in row] for i,row in enumerate(data)]
    t=Table(rows,colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLUE),('ROWBACKGROUNDS',(0,1),(-1,-1),[PALE,colors.white]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.5,colors.white)]))
    _,height=t.wrap(CW,900);assert y+height<HGT-M+6,(page,y,height,'table')
    t.drawOn(C,M,HGT-y-height);AUDIT.append({'page':page,'kind':'table','top':y,'height':height})
    y+=height+10;PROSE.append('\n'.join(' | '.join(str(v) for v in r) for r in data))

def figure(name,maxh):
    global y
    image=ImageReader(str(figdir/name));iw,ih=image.getSize();scale=min(CW/iw,maxh/ih);w,h=iw*scale,ih*scale
    assert y+h<HGT-M+6,(page,y,h,'figure')
    C.drawImage(image,M+(CW-w)/2,HGT-y-h,w,h);AUDIT.append({'page':page,'kind':'figure','top':y,'height':h,'file':name});y+=h+6

# 1: template header plus engineering question.
new_page('ENG5338 Coursework 2: Group Report')
para('<b>Group:</b> GAS4 &nbsp; | &nbsp; <b>Dataset:</b> Gas Turbine CO and NOx Emissions',10,13)
for mem in IDENT['members']:
    sid=mem['student_id'] or '____________'
    para(f"{mem['number']}. {html.escape(mem['name'])} — {sid}",9.4,12,2)
para(f'<b>Repository:</b> <link href="{REPO}" color="#245876">{REPO}</link>',8.7,12,13)
heading('1. Engineering Question &amp; Constraints')
para('How accurately can nine ambient and process measurements estimate contemporaneous gas-turbine CO (mg/m³), and what computing resources does each pipeline require? The intended application is an advisory virtual sensor for operational monitoring. Inputs and CO describe the same observation.')
para('<b>Accuracy constraint:</b> at least 90% of predictions within ±1 mg/m³ of measured CO. The absolute band gives a consistent error allowance across low and high concentrations. This target expresses the desired consistency of the advisory estimates and provides a concrete basis for comparing candidates.')
para('<b>Computational comparison:</b> record fitting time, single-row latency, batch prediction time, memory increment and model size. The initial draft used a 10 ms latency gate. After reviewing the HGB assessment, the selection priority changed to predictive MAE. The final comparison reports latency alongside accuracy.')
para('<b>Selected model:</b> Extra Trees achieved the lowest development-validation MAE, 0.7226 mg/m³, and the highest coverage, 81.76%. Its 19.03 ms single-row latency is the cost of the chosen accuracy-first trade-off. The 90% coverage target leaves an 8.24 percentage-point development gap to address.')

# 2: common design and data.
new_page('2. Experimental Design')
para('The course CSV contains 36,733 chronologically ordered rows from a Turkish gas turbine during 2011–2015 [1]. Measurements are hourly aggregates; year identifies the period. The nine predictors are AT, AP, AH, AFDP, GTEP, TIT, TAT, TEY and CDP. CO is the target. Year determines the partition, and NOx is excluded from the predictors.')
para('All 36,733 rows have complete, finite values. Seven duplicate complete rows, repeated observations and extreme values are retained. Each pipeline uses a training-fitted median imputer. OLS also standardises its inputs. RF, Extra Trees and HGB use the imputed values directly.')
table([['Partition','Years','Rows','Use'],['Development','2011–2013','22,191','Tuning, comparison, cost measurement'],['Reused assessment','2014–2015','14,542','Extra Trees secondary assessment; prior HGB exposure']], [90,82,65,CW-237],9)
para('Five expanding TimeSeriesSplit folds fit earlier rows and validate on later contiguous rows, separated by 24 rows [3]. Each validation block contains 3,698 observations; training sizes are 3,677, 7,375, 11,073, 14,771 and 18,469. The combined validation output contains 18,490 distinct rows. Gap length is defined in row units.')
para('MAE is the shared tuning objective, measured in mg/m³. Additional metrics are RMSE, R², coverage within ±1 mg/m³ and the fraction of negative predictions. Tables report mean fold scores, with MAE standard deviation describing variation across the five periods. Equal validation-block sizes give equal weighting to the observations for MAE and coverage.')
para('Every candidate uses the same predictors, development rows, chronological folds, scorers, seed 42 and one-worker searches. The folds support both parameter selection and comparison. The 2014–2015 period was used in CW1, then for the initial HGB assessment. After reviewing HGB, the accuracy-first selection chose Extra Trees from the existing development ranking and assessed it on the same 2014–2015 period. Both CW2 records are retained. Further confirmation uses a new future period.')

# 3: pipeline and tuning.
new_page('2. Experimental Design — models and tuning')
para('OLS is an inexpensive additive reference. RF averages bootstrap trees, Extra Trees adds randomised split thresholds, and HGB builds binned trees sequentially [2]. The nonlinear candidates capture interactions and nonlinear responses. Tree depth, leaf size and boosting regularisation control fitting complexity.')
table([['Pipeline','Latest searched grid','Selected setting'],
 ['RF — 3 settings / 15 CV fits','600 trees; depth 11; leaf 20; features 0.5; bootstrap fraction {0.75, 0.85, 0.90}','Fraction 0.90; other listed values fixed'],
 ['Extra Trees — 27 / 135','400 trees; depth {11,12,14}; leaf {7,10,15}; features {0.5,0.8,1.0}','Depth 14; leaf 10; features 0.8'],
 ['HGB — 8 / 40','Learning rate {0.05,0.10}; max leaves {15,31}; L2 {0,1}; 200 iterations','Rate 0.05; leaves 15; L2 1']], [91,213,CW-304],8.4)
para('GridSearchCV selects and refits the configuration with the lowest mean validation MAE. The latest exported grids contain 3 RF, 27 Extra Trees and 8 HGB configurations. RF and Extra Trees also have earlier owner experiments. RF uses bootstrap=True and n_jobs=1; Extra Trees uses bootstrap=False and n_jobs=1. HGB uses min_samples_leaf=20, max_bins=255 and early_stopping=False. Full settings are saved with the search evidence.')
para('The 38 latest configurations were replayed in the integration environment, giving 190 cross-validation fits plus three full-development refits. They reproduced the selected settings. The report uses the shared-runtime validation scores. RF has a small cross-version numerical difference from its received result. The latest Extra Trees configuration improves the earlier depth-12 validation MAE by about 0.0026 mg/m³.')
heading('Computational measurement design',12)
para('Member 5 measured all four complete pipelines on one Windows laptop with 22,191 development rows and one numerical thread. The procedure uses one fit warm-up and three timed fits; a separately fitted pipeline for prediction; five single-row warm-ups and 100 timings; and three batch warm-ups followed by ten 1,000-row timings. Summary values are medians and single-row p95. A separate fit samples RSS approximately every 5 ms. Serialized pipeline size is measured in KiB.')

# 4: primary comparison.
new_page('3. Comparative Analysis — predictive behaviour')
rows=[['Model','Train MAE','Val. MAE ± SD','Val. RMSE','Val. R²','Coverage','Fit s','Single ms']]
for name in ORDER:
 r=T.loc[name];rows.append([NAMES[name],f'{r.train_mae:.4f}',f'{r.validation_mae:.4f} ± {r.validation_mae_sd:.4f}',f'{r.validation_rmse:.4f}',f'{r.validation_r2:.4f}',f'{100*r.validation_coverage:.2f}%',f'{r.fit_median_s:.3f}',f'{r.single_median_ms:.2f}'])
table(rows,[78,48,100,50,42,53,40,CW-411],7.5)
para('Table 1. Errors are in mg/m³. Validation values are means over five chronological folds; SD describes the five MAEs. Coverage measures the fraction within ±1 mg/m³. Fitting and prediction columns give Member 5’s Windows medians.', 9, 12)
figure('temporal_validation.png',182)
para('Figure 1. Validation MAE and coverage across five expanding chronological folds.', 8.8, 11.5)
para(f'Extra Trees improves OLS validation MAE by {(1-ET.validation_mae/T.loc["linear_reference"].validation_mae)*100:.1f}% and achieves the highest coverage ({ET.validation_coverage*100:.2f}%). HGB has slightly lower mean fold RMSE ({H.validation_rmse:.4f}) than Extra Trees ({ET.validation_rmse:.4f}), despite worse MAE. MAE is the selection objective, while RMSE gives additional weight to larger errors.')
para('The nonlinear models have training MAEs near 0.41, compared with 0.6732 for OLS. Their train–validation gaps are 0.3232 for RF, 0.3133 for Extra Trees and 0.3544 for HGB; OLS has a gap of 0.2341. The larger errors on later observations show the generalisation challenge. Depth/leaf controls and L2 regularisation restrict complexity, while chronological folds reveal changes across periods.')
para('High CO is the largest error concentration. For the 2,211 validation observations above their training-fold 95th percentile, Extra Trees has MAE 2.2672, coverage 26.68% and mean prediction-minus-measurement −1.9672 mg/m³. RF and HGB also underpredict this subgroup. Training-fold quantiles define the thresholds, and measured validation CO defines subgroup membership.')

# 5: costs.
new_page('3. Comparative Analysis — computational efficiency')
rows=[['Model','Fit s','Single ms','p95 ms','Batch ms / 1k','Size KiB']]
for name in ORDER:
 r=T.loc[name];rows.append([NAMES[name],f'{r.fit_median_s:.4f}',f'{r.single_median_ms:.2f}',f'{r.single_p95_ms:.2f}',f'{r.batch_1000_median_ms:.2f}',f'{r.serialized_pipeline_kib:,.1f}'])
table(rows,[86,59,65,59,87,CW-356],8.5)
para('Table 2. Full-pipeline costs on Member 5’s Windows laptop. Single-row latency includes preprocessing and Python/pipeline overhead. Batch time covers 1,000 observations in one call.', 9, 12)
figure('accuracy_cost.png',198)
para('Figure 2. Development-validation MAE against Windows single-row latency. The dashed line marks the original 10 ms reference. The highlighted point is Extra Trees.', 8.8, 11.5)
para('Cost measurements use Windows build 22631, Intel64 Family 6 Model 140 CPU, eight logical CPUs, 7.65 GiB RAM, Python 3.10.6, scikit-learn 1.7.2, NumPy 2.2.6 and pandas 2.3.3, with one numerical thread. Validation/search replay uses Linux, AMD Ryzen 7 5800H, Python 3.12.9 and scikit-learn 1.9.1. Each comparison uses a shared runtime for its respective accuracy or cost measurements.')
para('HGB is the fastest nonlinear candidate: median fitting 0.5542 s and single-row latency 2.86 ms. Extra Trees fits in 5.2187 s and predicts one row in 19.03 ms. RF takes 24.4929 s and 27.18 ms, respectively. OLS is fastest at 0.70 ms per row. Extra Trees offers the strongest MAE result, while HGB offers a smaller computational footprint.')
para('Sampled RSS increments are 0.02 MiB for OLS, 25.54 for RF, 45.32 for Extra Trees and 6.13 for HGB. RSS estimates depend on the 5 ms polling interval and allocator reuse. Serialized sizes range from 1.6 KiB for OLS to about 44,718 KiB for Extra Trees; HGB is about 365 KiB. The experiment covers fitting at 22,191 rows and prediction calls of one and 1,000 rows.')

# 6: decision + final scores.
new_page('4. Recommended Pipeline — selection and final assessment')
para('We recommend Extra Trees for its lowest development-validation MAE, 0.7226 mg/m³, and highest coverage, 81.76%. The choice prioritises prediction error while reporting its 19.03 ms latency and 44,718 KiB artifact size. HGB remains the faster alternative. The accuracy-first selection followed the initial HGB assessment and used the existing development ranking.')
para('The selected pipeline is median imputation → ExtraTreesRegressor: 400 trees, max_depth=14, min_samples_leaf=10, max_features=0.8, bootstrap=False, random_state=42 and n_jobs=1. It uses Member 3’s saved settings, fits all 22,191 development rows and predicts the 14,542 later observations. The decision record precedes the Extra Trees assessment.')
rows=[['Partition','Rows','MAE','RMSE','R²','Coverage']]
rows.append(['Full development fit','22,191',f'{F["training"]["mae"]:.4f}',f'{F["training"]["rmse"]:.4f}',f'{F["training"]["r2"]:.4f}',f'{100*F["training"]["coverage"]:.2f}%'])
rows.append(['2014–2015 final','14,542',f'{TEST["mae"]:.4f}',f'{TEST["rmse"]:.4f}',f'{TEST["r2"]:.4f}',f'{100*TEST["coverage"]:.2f}%'])
for r in F['by_year']:rows.append([str(r['year']),f'{r["rows"]:,}',f'{r["mae"]:.4f}',f'{r["rmse"]:.4f}',f'{r["r2"]:.4f}',f'{100*r["coverage"]:.2f}%'])
table(rows,[110,62,67,72,63,CW-374],8.5)
para('Table 3. Extra Trees assessment on 2014–2015. Yearly rows divide the same prediction vector. The full-development training row describes the fitted model’s in-sample error.', 9, 12)
para(f'The final MAE is {TEST["mae"]:.4f} mg/m³ and coverage is {100*TEST["coverage"]:.2f}%. Relative to development-validation MAE, the change is {TEST["mae"]-S.validation_mae:+.4f} mg/m³.  The overall test mean prediction-minus-measurement is {F["test_mean_prediction_minus_actual"]:+.4f} mg/m³, and {F["negative_predictions"]:,} predictions are negative. The saved vectors contain the pipeline’s direct predictions.')
para('Assessment history: HGB was evaluated first, with MAE 0.8998 mg/m³ and coverage 70.00%. The subsequent accuracy-first decision selected Extra Trees using development results and assessed it on the same 2014–2015 observations. Model settings stayed fixed during both assessments. Their decision records, predictions and metrics are stored in separate directories.')

# 7: final diagnostics, limits and sources.
new_page('4. Recommended Pipeline — error analysis and next steps')
figure('final_diagnostics.png',190)
para('Figure 3. Extra Trees predictions and signed errors for 2014–2015. Dashed residual lines mark the ±1 mg/m³ band.', 8.8, 11.5)
para(f'Using only development CO, the 95th-percentile threshold is {F["training_q95"]:.4f} mg/m³. Among {F["tail_rows"]:,} final rows above it, MAE is {F["tail_test"]["mae"]:.4f}, coverage is {100*F["tail_test"]["coverage"]:.2f}% and mean signed error is {F["tail_mean_prediction_minus_actual"]:+.4f} mg/m³. High-CO observations therefore remain a priority for further development.')
para('<b>Engineering recommendation:</b> use Extra Trees as the preferred model for advisory CO estimation. The assessment coverage of 73.36% leaves a 16.64 percentage-point gap to the project target. The next development priorities are high-CO error reduction, sensor-input robustness, drift monitoring and end-to-end timing on the intended system.')
para('<b>Next experiments:</b> collect representative high-CO observations, test additional sensor/history features and evaluate on a new future period. Exact timestamps would support gap selection and temporal diagnostics. Plant-specific error tolerances and service timing requirements would refine the accuracy–cost decision.')
heading('References and reproducibility',12)
para('[1] Kaya, H., Tüfekci, P. and Uzun, E. (2019). <i>Gas Turbine CO and NOx Emission Data Set.</i> UCI Machine Learning Repository. <link href="https://doi.org/10.24432/C5WC95">doi:10.24432/C5WC95</link>.<br/>[2] scikit-learn documentation, <i>Ensembles: random forests, extremely randomised trees and histogram gradient boosting</i>. <link href="https://scikit-learn.org/stable/modules/ensemble.html">scikit-learn.org/stable/modules/ensemble.html</link>.<br/>[3] scikit-learn documentation, <i>TimeSeriesSplit</i>. <link href="https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html">API documentation</link>.<br/>[4] ENG5338 (2026/27), <i>Coursework 2 Brief (Group)</i> and supplied report template. Course materials.',8.2,11)
para('The notebook runs shared validation, verifies search and timing evidence, and checks both saved assessment records. The repository includes data, code, prediction vectors and fixed-model replay switches.', 8.5, 11.5)

# Appendix — one page.
new_page('Appendix — numerical protocol and evidence map','appendix')
folds=pd.read_csv(ROOT/'results/development/folds.csv')
rows=[['Fold','Train rows','Gap rows','Validation row IDs','Val. rows']]
for r in folds.itertuples():rows.append([r.fold,r.train_rows,24,f'{r.first_validation_row}–{r.last_validation_row}',r.validation_rows])
table(rows,[43,83,74,166,CW-366],8.5)
para('Source row IDs are zero-based. Development precedes row 22,191; final rows are 22,191–36,732. The gap is applied independently at each split. Schema and year counts are checked before computation; quantile thresholds used in high-CO validation diagnostics are training-fold quantities.',9.5,13)
rows=[['Evidence','Repository location'],['Original owner searches','results/submitted/member2/latest, member3/latest, member4/latest'],['Executed common-runtime search replay','results/search_reproduction/'],['Common validation and prediction vectors','results/development/'],['Member 5 independent Windows costs','results/member5_local_py310/'],['Original HGB assessment','results/final/'],['Revised Extra Trees assessment','results/final_extra_trees/'],['Report tables and figures','results/submission/; figures/submission/'],['Notebook implementation','src/cw2_common.py; cw2_project.py; cw2_submission.py']]
table(rows,[170,CW-170],8.5)
para('<b>Dataset SHA-256:</b><br/>'+E['protocol']['data_sha256'],8,11)
para('<b>Protocol:</b> '+E['protocol']['protocol_id']+'; <b>Member 5 cost runtime:</b> '+E['member5_runtime']['runtime_id']+'; <b>fixed-assessment runtime:</b> '+F['runtime_id']+'. The receipt protocol identifies the shared folds and metrics; the revised selection is recorded separately.',9.5,13)
para('<b>Search interpretation:</b> the grids cover the latest recorded owner searches. Their sizes are 3, 27 and 8 configurations. Extra Trees depth 14 is the upper edge of its latest depth grid. The saved tables show scores for every tested setting.',9.5,13)

# Contributions — excluded from page limit, factual not invented approval.
new_page('Statement of Contribution','contributions — excluded from page limit')
roles=[
 ('Shared protocol, baseline and integration coordinated using Codex.','Common workflow and experimental-design material assembled with Codex assistance.','§1–3, §7–9'),
 ('RF searches, selected settings, validation scatter analysis.','Received RF method/results/limitations text.','§2–5; RF experiment'),
 ('Successive Extra Trees tuning; latest result export and plot.','Received Extra Trees experiment/limitations text.','§2–5; Extra Trees experiment'),
 ('HGB grid search, fold metrics, figures and interpretation.','Received HGB method/results/limitations text.','§2–5; HGB experiment'),
 ('Independent Windows measurement of all four shared pipelines.','Benchmark methodology, provenance and cost–accuracy interpretation.','§6–7; Member 5 notebook')]
rows=[['Member (name + ID)','Main implementation','Writing evidenced','Notebook location']]
for mem,role in zip(IDENT['members'],roles):rows.append([mem['name']+' / '+(mem['student_id'] or '____________'),*role])
table(rows,[111,132,126,CW-369],8)
para('<b>Integration and writing:</b> Wenyi coordinated the shared workflow and requested the accuracy-first Extra Trees selection after reviewing HGB. Codex assisted with search replay, integration, both assessment runs, report/slides drafting and checks.', 9.5, 13)
para('<b>AI tools and uses:</b> Codex/ChatGPT assisted shared design, programming, debugging, analysis, final assessment, report/slides drafting and document checks. Jiaqi disclosed ChatGPT coding and wording assistance; Sirawich disclosed Claude explanations, plotting and language assistance; Hansini disclosed ChatGPT learning/troubleshooting; Sauhandikaa disclosed ChatGPT environment setup, verification code and drafting guidance. Original member evidence is retained locally; public numerical exports are separated from student IDs.',9.5,13)
if IDENT.get('all_members_reviewed_contribution_statement'):
    para('All members have read and agreed to this contribution statement.',10,13)
else:
    para('<b>Review status:</b> awaiting all members’ confirmation before submission.', 9.5, 13)
C.save()
(OUT/'report_content.md').write_text('# ENG5338 CW2 — GAS4 report source\n\n'+'\n\n'.join(PROSE)+'\n')
assert page==9

# Slides — concise PDF with an editable PPTX equivalent and speaker notes.
slides=[]
def slide(title,subtitle='',bullets=None,table_data=None,image=None,notes='',seconds=50):
    slides.append(dict(title=title,subtitle=subtitle,bullets=bullets or [],table=table_data,image=image,notes=notes,seconds=seconds))
slide('Gas-turbine CO estimation','ENG5338 Coursework 2  •  GAS4',[
 'Nine process/ambient inputs → contemporaneous CO',
 'Three nonlinear models plus a linear reference',
 'Recommendation: Extra Trees'],notes='Introduce the CO virtual-sensor task and the four-model comparison. Explain that Extra Trees gives the lowest development MAE and highest coverage. The presentation covers the shared protocol, model behaviour, computational measurements, selected pipeline and next experiments.',seconds=35)
slide('Engineering target and priorities','Advisory CO monitoring',[
 'Target: ≥90% of estimates within ±1 mg/m³',
 'Primary selection metric: development-validation MAE',
 'Compare fitting time, latency, memory and model size',
 'Selection priority changed from the initial 10 ms gate to accuracy'],notes='The absolute tolerance gives a consistent error allowance across concentrations. The coverage target expresses the desired screening consistency. The first draft prioritised a ten-millisecond gate; after reviewing HGB, the decision prioritised predictive MAE. Report computational measurements alongside accuracy.',seconds=55)
slide('Chronological experiment design','22,191 development rows  |  14,542 later assessment rows',[
 'Development 2011–2013; assessment 2014–2015',
 'Five expanding folds; 3,698 validation rows each; gap 24 rows',
 'Training-fold median imputation; OLS scaling; seed 42',
 'Nine predictors; CO target; year defines the partition',
 'CW1, HGB and Extra Trees assessments share the later years'],notes='The dataset contains chronologically ordered hourly aggregates. Each fold fits earlier rows and validates on a later contiguous block. Explain the twenty-four-row gap and training-fold preprocessing. The nine inputs include TEY; year determines the split and NOx is excluded. State the assessment history: CW1 used the later years, then HGB was assessed, then the accuracy-first Extra Trees choice was assessed on the same observations.',seconds=65)
slide('Four pipelines','38 latest configurations / 190 CV fits',table_data=[['Model','Reason for inclusion','Selected controls'],['OLS','Inexpensive additive reference','Imputation + scaling'],['RF','Bootstrap tree averaging','600 trees; depth 11; leaf 20'],['Extra Trees','Randomised split thresholds','400 trees; depth 14; leaf 10'],['HGB','Sequential binned boosting','200 rounds; rate .05; leaves 15; L2 1']],notes='Describe each model and its complexity controls. GridSearchCV selects the lowest mean validation MAE. The latest received grids contain three RF, twenty-seven Extra Trees and eight HGB configurations. Replaying these grids reproduced the selected settings. All comparisons share the same folds and metrics.',seconds=60)
slide('Extra Trees leads validation MAE and coverage','Common five-fold comparison',table_data=[['Model','Train MAE','Val. MAE','Coverage'],*[[NAMES[n],f'{T.loc[n,"train_mae"]:.4f}',f'{T.loc[n,"validation_mae"]:.4f}',f'{100*T.loc[n,"validation_coverage"]:.2f}%'] for n in ORDER]],bullets=['Extra Trees validation coverage: 81.76%; project target: 90%.','HGB has the lowest mean fold RMSE.'],notes='MAE is the selection objective and is expressed in milligrams per cubic metre. Extra Trees has the lowest validation MAE and highest coverage. HGB has a slightly lower mean fold RMSE. Explain the training–validation gap and how the MAE standard deviation describes variation across the five periods.',seconds=65)
slide('Temporal and high-CO errors','Training and later validation behaviour',image='temporal_validation.png',bullets=['Extra Trees train–validation MAE gap: 0.3133 mg/m³.','High-CO validation subgroup coverage: 26.68%.'],notes='Walk through the temporal variation. Extra Trees training MAE is about 0.4093 and validation MAE about 0.7226. Above each training-fold ninety-fifth percentile, error increases and predictions tend to be low. The diagnostic subgroup is defined using measured validation CO. Depth and leaf controls restrict complexity; the chronological folds show period-to-period generalisation.',seconds=55)
slide('Computational cost','Member 5: one Windows laptop, one numerical thread',table_data=[['Model','Fit s','Single ms','Batch ms / 1k'],*[[NAMES[n],f'{T.loc[n,"fit_median_s"]:.3f}',f'{T.loc[n,"single_median_ms"]:.2f}',f'{T.loc[n,"batch_1000_median_ms"]:.2f}'] for n in ORDER]],bullets=['Three timed fits; 100 single-row timings; ten batch timings.','Validation: Linux sklearn 1.9.1. Cost: Windows sklearn 1.7.2.'],notes='Sauhandikaa measured all four complete pipelines on one Windows runtime. Explain warm-up, repeated fitting, the single-row median and batch timing. Extra Trees takes about nineteen milliseconds for one prediction and has the largest artifact. HGB offers faster inference and a smaller model. RSS is sampled approximately every five milliseconds, with allocator reuse affecting the measured increment.',seconds=65)
slide('Recommendation: Extra Trees','Prioritise predictive MAE and report computational cost',image='accuracy_cost.png',bullets=['Development MAE: 0.7226 mg/m³; coverage: 81.76%.','Median single-row prediction: 19.03 ms.','Chosen from the development ranking after the HGB assessment.'],notes='Explain the accuracy-first choice. Extra Trees has the lowest existing development MAE and highest coverage. Its slower latency and larger size are the computational trade-off. The initial HGB assessment preceded this change of priorities. The decision uses the development ranking, and the original HGB record remains part of the experiment history.',seconds=55)
slide('Extra Trees: 2014–2015 assessment','400 trees  •  depth 14  •  leaf 10  •  max_features 0.8',table_data=[['Period','MAE','RMSE','R²','Coverage'],['2014–2015',f'{TEST["mae"]:.4f}',f'{TEST["rmse"]:.4f}',f'{TEST["r2"]:.4f}',f'{100*TEST["coverage"]:.2f}%'],*[[str(r['year']),f'{r["mae"]:.4f}',f'{r["rmse"]:.4f}',f'{r["r2"]:.4f}',f'{100*r["coverage"]:.2f}%'] for r in F['by_year']]],bullets=['Earlier HGB assessment: MAE 0.8998; coverage 70.00%.','Both models were assessed on the same 2014–2015 observations.'],notes=f'Extra Trees assessment MAE is {TEST["mae"]:.4f} and coverage is {100*TEST["coverage"]:.2f} percent. The yearly rows divide its saved prediction vector. HGB was assessed first, followed by the accuracy-first selection and Extra Trees assessment. The settings remain those selected on development data. Further confirmation uses a new future period.',seconds=65)
slide('Next experiments','Close the coverage gap and evaluate future operation',[
 'Collect additional high-CO observations',
 'Test sensor and recent-history features',
 'Evaluate on a new future period',
 'Measure input robustness, drift and end-to-end timing'],notes='Focus further work on the largest error groups. Collect representative high-concentration data, assess additional features and evaluate performance on a new future period. Establish plant-specific tolerances and service requirements. These steps extend the accuracy and computational comparison toward operational use.',seconds=45)
slide('Team contributions and conclusion','GAS4  •  Questions',[
 'Wenyi: shared framework, baseline and integration',
 'Jiaqi: RF  |  Sirawich: Extra Trees  |  Hansini: HGB',
 'Sauhandikaa: Windows computational comparison',
 'Codex/ChatGPT: code, assessment and drafting assistance',
 'Extra Trees: lowest development MAE; coverage gap guides next work'],notes='Name the distinctive contributions of the five members. State the recorded AI assistance. Conclude with the selected Extra Trees pipeline, its accuracy–cost trade-off and the coverage gap. The notebook, saved predictions and repository provide the numerical detail. Invite questions.',seconds=35)
assert sum(s['seconds'] for s in slides)==600
SW,SH=960,540
SC=canvas.Canvas(str(OUT/'ENG5338_CW2_presentation_GAS4.pdf'),pagesize=(SW,SH))
SC.setTitle('ENG5338 CW2 — GAS4 presentation');SC.setAuthor('GAS4')
prs=Presentation();prs.slide_width=Inches(13.3333);prs.slide_height=Inches(7.5)
slide_audit=[]

def slide_para(text,x,top,width,size=21,color=INK,bold=False):
    st=ParagraphStyle('slide',fontName='UIBold' if bold else 'UI',fontSize=size,leading=size*1.3,textColor=color)
    p=Paragraph(text,st);_,h=p.wrap(width,SH)
    assert top+h<SH-32,('slide overflow',len(prs.slides),top,h,text)
    p.drawOn(SC,x,SH-top-h)
    slide_audit.append({'slide':len(prs.slides),'top':top,'height':h,'text':re.sub('<[^>]+>','',text)})
    return h

def ppt_text(sl,text,x,y,w,h,size=22,bold=False,color='172B3B'):
    shape=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=shape.text_frame;tf.word_wrap=True
    tf.margin_left=Pt(0);tf.margin_right=Pt(0);tf.margin_top=Pt(0);tf.margin_bottom=Pt(0)
    for i,line in enumerate(text.split('\n')):
        par=tf.paragraphs[0] if i==0 else tf.add_paragraph();par.text=line
        par.font.name='DejaVu Sans';par.font.size=Pt(size);par.font.bold=bold;par.font.color.rgb=RGBColor.from_string(color)
        par.space_after=Pt(10)
    return shape

for i,s in enumerate(slides,1):
    sl=prs.slides.add_slide(prs.slide_layouts[6]);sl.background.fill.solid();sl.background.fill.fore_color.rgb=RGBColor(255,255,255)
    SC.setFillColor(BLUE);SC.rect(0,SH-10,SW,10,fill=1,stroke=0)
    slide_para(s['title'],48,35,864,27,BLUE,True)
    slide_para(s['subtitle'],48,83,864,14)
    ppt_text(sl,s['title'],.67,.48,12,.65,27,True,'245876');ppt_text(sl,s['subtitle'],.67,1.15,12,.4,14)
    top=133
    if s['table']:
        data=s['table'];width=864;colw=width/len(data[0]);fs=14 if i==4 else 17
        sty=ParagraphStyle('sTable',fontName='UI',fontSize=fs,leading=fs*1.3)
        t=Table([[Paragraph(html.escape(str(v)),sty) for v in row] for row in data],colWidths=[colw]*len(data[0]))
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),('VALIGN',(0,0),(-1,-1),'TOP')]))
        _,th=t.wrap(width,400);assert top+th<485
        t.drawOn(SC,48,SH-top-th)
        shape=sl.shapes.add_table(len(data),len(data[0]),Inches(.67),Inches(top/72),Inches(12),Inches(th/72))
        for ri,row in enumerate(data):
            for ci,v in enumerate(row):
                cell=shape.table.cell(ri,ci);cell.text=str(v);cell.margin_top=Pt(8);cell.margin_bottom=Pt(8)
                cell.fill.solid();cell.fill.fore_color.rgb=RGBColor.from_string('EDF3F6' if ri%2==0 else 'FFFFFF')
                for pp in cell.text_frame.paragraphs:pp.font.name='DejaVu Sans';pp.font.size=Pt(fs);pp.font.color.rgb=RGBColor.from_string('172B3B')
        top+=th+18
    if s['image']:
        img=ImageReader(str(figdir/s['image']));iw,ih=img.getSize();scale=min(864/iw,252/ih);ww,hh=iw*scale,ih*scale
        SC.drawImage(img,(SW-ww)/2,SH-top-hh,ww,hh)
        sl.shapes.add_picture(str(figdir/s['image']),Inches((SW-ww)/144),Inches(top/72),width=Inches(ww/72),height=Inches(hh/72))
        top+=hh+10
    for b in s['bullets']:
        size=15 if s['image'] or s['table'] else (19 if i==11 else 21)
        h=slide_para('• '+html.escape(b),54,top,852,size)
        ppt_text(sl,'• '+b,.75,top/72,11.83,(h+12)/72,size);top+=h+15
    if i == 11:
        refs='Sources: Kaya et al. (2019), UCI doi:10.24432/C5WC95; scikit-learn documentation; ENG5338 CW2 brief.'
        slide_para(refs,48,487,864,9)
        ppt_text(sl,refs,.67,6.76,12,.3,9)
    SC.setFont('UI',9);SC.setFillColor(BLUE);SC.drawString(48,20,'GAS4  |  ENG5338 CW2');SC.drawRightString(912,20,str(i))
    ppt_text(sl,f'GAS4  |  ENG5338 CW2                                      {i}',.67,7.12,12,.25,9,color='245876')
    sl.notes_slide.notes_text_frame.text=s['notes']
    SC.showPage()
SC.save();prs.save(OUT/'ENG5338_CW2_presentation_GAS4.pptx')
(OUT/'presentation_notes.md').write_text('# GAS4 — presenter notes\n\nTarget: approximately 10 minutes (600-second plan), followed by 10 minutes of Q&A. Speaking can be shared or led by one person. Every member must understand the whole notebook.\n\n'+'\n\n'.join(f'## {i}. {s["title"]} — {s["seconds"]} seconds\n\n{s["notes"]}' for i,s in enumerate(slides,1))+'\n')
# Final structural/numerical document checks.
report=fitz.open(OUT/'ENG5338_CW2_report_GAS4.pdf');deck=fitz.open(OUT/'ENG5338_CW2_presentation_GAS4.pdf')
assert len(report)==9 and len(deck)==11
report_text='\n'.join(pg.get_text() for pg in report)
for value in [TEST['mae'],TEST['rmse'],TEST['r2']]:assert f'{value:.4f}' in report_text
assert f'{100*TEST["coverage"]:.2f}%' in report_text
assert 'Statement of Contribution' in report_text and REPO in report_text
assert not any(word in report_text for word in ['TODO','TBD','PLACEHOLDER'])
(OUT/'report_extracted.txt').write_text(report_text)
(OUT/'document_audit.json').write_text(json.dumps({'report_pages':9,'main_pages':7,'appendix_pages':1,'contribution_pages':1,'slide_pages':11,'planned_talk_seconds':600,'template':'docs/coursework/template_cw2_ENG5.tex: same four sections, 2.5cm margins, 11pt body; appendix/contributions separate','recommended_model':'extra_trees','selection_policy_revised_after_prior_test':True,'independent_confirmatory_test':False,'member5_id_present':bool(IDENT['members'][4]['student_id']),'contribution_endorsement_confirmed':IDENT['all_members_reviewed_contribution_statement'],'report_layout':AUDIT,'slide_layout':slide_audit},indent=2)+'\n')
print('Built report (7 main + 1 appendix + 1 contribution), 11-slide PDF, editable PPTX and presenter notes.')
