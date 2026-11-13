# GAS4 Notebook 运行与阅读

打开[主 Notebook](../../ENG5338_CW2_notebook_GAS4.ipynb)。它有 8 个已执行的代码单元，分为 9 部分：环境和数据、调参证据、统一五折验证、训练差距和高 CO 诊断、成员分析、计算成本、模型选择、Extra Trees 评估及实验经过、结论与贡献。

## 如何运行

安装 requirements.lock.txt 中的依赖，在项目根目录执行：

```sh
python -m pip install -r requirements.lock.txt
python run_notebook.py
```

默认会重新运行四个已选参数配置的五折验证，核对搜索记录与成员 5 计时样本，再读取和验证已保存的评估结果。RUN_FULL_SEARCHES=True 会重跑成员最新搜索网格；固定模型重放开关会复现 Extra Trees 的已保存预测。两个开关默认均为 False。

使用 VS Code 或 Jupyter 时，选择对应 Python 环境、重启内核并运行全部单元。使用 Colab 时，解压完整项目，将工作目录设到项目根目录，保留 src、data、results 与 Notebook 的相对位置。

## 核心数据

- 全部数据 36,733 行，开发期 2011–2013 共 22,191 行，后期评估 2014–2015 共 14,542 行。
- 五折扩展时间验证，每折验证 3,698 行，训练和验证之间留出 24 行，seed=42，单数值线程。
- 所有预处理在当前训练折内拟合。MAE 选择参数，同时报告 RMSE、R²、±1 mg/m³ 覆盖率、训练与验证差距。
- Extra Trees 验证 MAE 0.7226，覆盖率 81.76%；后期评估 MAE 0.8011，覆盖率 73.36%。
- 先前 HGB 与当前 Extra Trees 都评估过相同 2014–2015 数据，CW1 也使用过这些年份。两份评估均保留原参数、哈希和预测向量。

## 文件位置

- results/submitted：成员搜索记录；results/search_reproduction：统一环境搜索复跑。
- results/development：统一验证分数、逐行预测和高 CO 诊断。
- results/member5_local_py310：成员 5 的 Windows 实测；results/costs：较早的 Linux 参考计时。
- results/final：先前 HGB 评估；results/final_extra_trees：当前 Extra Trees 评估。
- results/submission：文档用合并表和执行核验。

校验现有结果运行 `python scripts/verify_integration.py`。该检查从保存的预测向量重算指标，核对参数、计时样本、原件哈希与成员入口路径。成员个人重跑输出进入被忽略的 results/member_runs。

[模型比较](候选模型说明与选型建议_zh.md) · [提交说明](提交与答辩说明_zh.md) · [根目录说明](../../README.md)
