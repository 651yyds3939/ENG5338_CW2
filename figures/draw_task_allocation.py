"""Render the agreed GAS4 allocation as a shareable Chinese infographic."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H = 1800, 2070
im = Image.new('RGB', (W, H), '#F1F5F9')
d = ImageDraw.Draw(im)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size, index=2)

def text(x, y, content, size=32, color='#334155', bold=False):
    d.text((x, y), content, font=font(size, bold), fill=color)

def card(box, color):
    x0,y0,x1,y1=box
    d.rounded_rectangle((x0,y0+7,x1,y1+7),radius=24,fill='#E0E7EF')
    d.rounded_rectangle(box,radius=24,fill='white')
    d.rounded_rectangle((x0,y0,x0+10,y1),radius=5,fill=color)

def bullet(x,y,content,size=32):
    d.ellipse((x,y+18,x+9,y+27),fill='#94A3B8')
    text(x+26,y,content,size)

# Heading.
d.rectangle((0,0,W,234),fill='#10233F')
text(84,36,'ENG5338  /  COURSEWORK 2',28,'#9EC5F2',True)
text(80,90,'GAS4 小组任务分工',64,'white',True)
text(84,177,'5 位成员 · 统一实验协议 · 一个最终 Notebook',30,'#CDDAEC')

# Member 1.
card((80,274,1720,574),'#2563EB')
text(118,298,'成员 1 · Wenyi',33,'#2563EB',True)
text(118,348,'公共框架与 Notebook 整合',43,'#10233F',True)
for x,y,s in [(124,424,'数据检查、共同划分与交叉验证'),(930,424,'整合代码，保证整本可复现'),
              (124,484,'统一评分、线性回归基准'),(930,484,'汇总表图，撰写公共实验方法')]:
    bullet(x,y,s,31)

# Middle model owners.
text(90,620,'三位模型负责人：使用共同数据、时间折和指标',35,'#10233F',True)
models=[(80,'成员 2','随机森林回归','Random Forest','#047857'),
        (636,'成员 3','Extra Trees 回归','Extra Trees','#7C3AED'),
        (1192,'成员 4','直方图梯度提升','Histogram Gradient Boosting','#C2410C')]
for x,member,title,english,color in models:
    card((x,688,x+528,1178),color)
    text(x+34,716,member,33,color,True)
    text(x+34,773,title,35,'#10233F',True)
    esize=23 if member=='成员 4' else 27
    text(x+34,828,english,esize,'#64748B')
    d.line((x+34,887,x+494,887),fill='#E2E8F0',width=2)
    for offset,item in enumerate(['折内预处理与模型训练','参数搜索与最佳配置','对比训练、验证成绩','分析过拟合与模型局限']):
        bullet(x+36,913+offset*54,item,28)

# Common delivery strip.
d.rounded_rectangle((80,1215,1720,1323),radius=18,fill='#E3EBF8')
text(113,1230,'成员 2–4 交回',29,'#1D4ED8',True)
text(438,1230,'个人 Notebook ＋ 实验结果 ＋ 分析',32,'#10233F',True)
text(438,1275,'撰写各自模型的方法与结果；只编辑个人实验文件',26,'#475569')

# Member 5.
card((80,1363,1720,1649),'#0369A1')
text(118,1388,'成员 5',33,'#0369A1',True)
text(118,1437,'计算成本测量与最终测试',43,'#10233F',True)
bullet(124,1510,'同一环境测训练、预测时间和资源',30)
bullet(930,1510,'记录硬件、软件及测量条件',30)
bullet(124,1570,'最终模型及参数确定后，测试一次',30)
bullet(930,1570,'撰写成本、测试结果与局限',30)

# Team responsibilities.
d.rounded_rectangle((80,1691,1720,1921),radius=24,fill='#10233F')
text(117,1715,'全组共同负责',35,'white',True)
text(120,1774,'工程问题与部署约束  ·  按验证证据推荐最终方案',31,'#E1EAF7')
text(120,1825,'报告与演示  ·  全员问答准备  ·  实际贡献与 AI 用途记录',31,'#E1EAF7')
text(120,1875,'实验分工不等于已完成贡献；结果以实际运行记录为准。',25,'#ACC0DC')

text(86,1965,'协作流程',26,'#64748B',True)
text(280,1963,'Wenyi 提供框架  →  三人独立实验  →  统一整合与测成本  →  最终测试',29,'#334155')
im.save(ROOT/'GAS4_小组分工图.png',dpi=(180,180))
print(ROOT/'GAS4_小组分工图.png')
