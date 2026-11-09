"""Render the GAS4 allocation in English for group sharing."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W,H=1800,2070
im=Image.new('RGB',(W,H),'#F1F5F9')
d=ImageDraw.Draw(im)
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def text(x,y,s,size=31,color='#334155',bold=False,max_width=None):
    f=ImageFont.truetype(BOLD if bold else REG,size)
    if max_width:
        while d.textbbox((0,0),s,font=f)[2]>max_width and size>18:
            size-=1
            f=ImageFont.truetype(BOLD if bold else REG,size)
    d.text((x,y),s,font=f,fill=color)

def card(box,color):
    x0,y0,x1,y1=box
    d.rounded_rectangle((x0,y0+7,x1,y1+7),radius=24,fill='#E0E7EF')
    d.rounded_rectangle(box,radius=24,fill='white')
    d.rounded_rectangle((x0,y0,x0+10,y1),radius=5,fill=color)

def bullet(x,y,s,size=29,max_width=700):
    d.ellipse((x,y+12,x+9,y+21),fill='#94A3B8')
    text(x+26,y,s,size,max_width=max_width)

d.rectangle((0,0,W,234),fill='#10233F')
text(84,42,'ENG5338  /  COURSEWORK 2',28,'#9EC5F2',True)
text(80,96,'GAS4 | Team Task Allocation',61,'white',True)
text(84,182,'5 members  /  One shared protocol  /  One final notebook',29,'#CDDAEC')

card((80,274,1720,574),'#2563EB')
text(118,307,'MEMBER 1  /  WENYI',31,'#2563EB',True)
text(118,362,'Shared framework & notebook integration',43,'#10233F',True)
bullet(124,443,'Data checks, splits and cross-validation',28)
bullet(930,443,'Integrate code and verify reproducibility',28)
bullet(124,503,'Shared metrics and linear regression baseline',28)
bullet(930,503,'Comparison charts and common methods',28)

text(90,628,'MODEL OWNERS: SAME DATA, TIME FOLDS AND METRICS',32,'#10233F',True)
models=[(80,'MEMBER 2',['Random Forest','Regression'],'#047857'),
        (636,'MEMBER 3',['Extra Trees','Regression'],'#7C3AED'),
        (1192,'MEMBER 4',['Histogram Gradient','Boosting Regression'],'#C2410C')]
for x,member,title,color in models:
    card((x,688,x+528,1178),color)
    text(x+34,724,member,30,color,True)
    text(x+34,786,title[0],34,'#10233F',True,max_width=460)
    text(x+34,834,title[1],34,'#10233F',True,max_width=460)
    d.line((x+34,901,x+494,901),fill='#E2E8F0',width=2)
    for i,s in enumerate(['Fold-local preprocessing & fitting','Tune hyperparameters','Compare train / validation scores','Analyse overfitting & limitations']):
        bullet(x+35,931+i*53,s,25,438)

d.rounded_rectangle((80,1215,1720,1323),radius=18,fill='#E3EBF8')
text(113,1238,'MEMBERS 2–4',27,'#1D4ED8',True)
text(438,1235,'Return: personal notebook + results + analysis',32,'#10233F',True,max_width=1220)
text(438,1281,'Write your model methods/results; edit your own experiment file only.',25,'#475569',max_width=1230)

card((80,1363,1720,1649),'#0369A1')
text(118,1397,'MEMBER 5',31,'#0369A1',True)
text(118,1450,'Computational cost & final testing',43,'#10233F',True)
bullet(124,1528,'Benchmark fit, prediction and resources',28)
bullet(930,1528,'Record hardware, software and conditions',28)
bullet(124,1586,'Test once after model and parameters are fixed',28)
bullet(930,1586,'Write cost, test findings and limitations',28)

d.rounded_rectangle((80,1691,1720,1921),radius=24,fill='#10233F')
text(117,1727,'SHARED RESPONSIBILITIES',33,'white',True)
text(120,1785,'Engineering question & constraints  /  Evidence-based final recommendation',29,'#E1EAF7',max_width=1560)
text(120,1834,'Report & presentation  /  Q&A preparation  /  Contributions & AI-use record',29,'#E1EAF7',max_width=1560)
text(120,1881,'Task allocation does not imply completion. Report only results that were actually run.',23,'#ACC0DC',max_width=1560)

text(86,1978,'WORKFLOW',25,'#64748B',True)
text(280,1978,'Framework → Individual experiments → Integration & cost → Final test',29,'#334155',max_width=1440)
path=ROOT.parent/'GAS4_Team_Task_Allocation_EN.png'
im.save(path,dpi=(180,180))
print(path)
