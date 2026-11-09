# ENG5338 CW2 — GAS4

当前阶段：公共框架及线性回归已完成；成员 2/3/4 分别执行随机森林、Extra Trees、直方图梯度提升。最终推荐待实际模型比较后选择，不含最终报告或演示。

- [项目全解读：任务、原理、方法、最终效果及 CW1/CW2 对照](项目全解读_CW1与CW2对照_zh.md)
- [需求检查、评分清单及周一讨论方案](需求检查与周一讨论_zh.md)
- [Notebook 用途、结果解读与问答](Notebook解读与问答_zh.md)
- [候选模型原理、优缺点与选型建议](候选模型说明与选型建议_zh.md)
- [提交用英文 Notebook](../../ENG5338_CW2_notebook_GAS4.ipynb)
- [贡献与 AI 协助记录](../../notes/contributions_and_ai.md)
- [精简协作交接：独立模型脚本与三个成员资料包](../../member_handoff/交接说明.md)

模型负责人无需共同编辑主 Notebook：分别发送 `member_handoff/packages/` 中对应 ZIP，
成员只改自己的模型脚本，交回代码、结果和分析，由 Wenyi 整合。主 Notebook 仍是最终提交的统一复现入口。

Notebook 已从新内核完整运行。实际完成的是数据检查、共同时间划分、五折 OLS 评估及其成本测量。
三种候选的开关默认为 False，均显示 NOT RUN；扩展验证、可扩展性、模型锁定与最终测试均未运行。

## 运行

在本目录执行（本次使用已有 CW1 Python 环境，不改动 CW1 文件）：

```bash
../ENG5338_CW1/.venv/bin/python run_notebook.py
```

或使用自己安装依赖的 Python：

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python run_notebook.py
```

`run_notebook.py` 用启动它的 Python 运行本地内核，不需全局注册 kernelspec。
首次实测的完整环境快照为 `environment.initial.freeze.txt`；直接依赖固定版本在
`requirements.lock.txt`，每次 Notebook 实际运行的解释器、依赖版本和硬件在 `results/runtime.json`。
依赖文件只记录本机实际环境，不假定任意平台都可安装同样构建。

Notebook 也可在 Jupyter 中选中具有上述依赖的内核后 Run All。建议每次重新开始内核运行。
模型负责人将 `RUN_MODELS` 中对应值改为 True，并在自己小节补充分析。
Notebook 是实际协作文件；`build_notebook.py` 是初始框架生成源，重新运行会覆盖已有 Notebook
及其输出，故在组员编辑开始后应直接编辑 Notebook，或先同步修改生成源。

## 输出与测试封存

`results/` 保存开发集折划分、评分、成本原始重复样本、环境、图与状态；
`data/gas-turbine-emissions.csv` 是原课程文件的同哈希副本。
协议、目标和阈值都还是草案。更改它们需要重新运行所有模型。

当前不含测试预测调用，也未导出测试指标。测试行只在全表结构检查时读取，随后仅保留开发数据及分区行号。
CW1 早已评估同一 2014–2015 测试期，这一历史暴露限制已在说明中披露。
最终测试需等全组确定最终模型及参数后另行加入带模型锁和重复执行保护的单次流程。

原始 brief、模板 PDF/TeX、截图均保留原样。项目文件全部位于本目录；未写最终报告或演示。
