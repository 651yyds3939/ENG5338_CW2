# 成员 2：随机森林回归（模型 1）

**负责模型：随机森林回归，代码为 `RandomForestRegressor`。**
通过多棵决策树的预测取平均来估计 CO。主要调整树的数量 `n_estimators`、树深 `max_depth` 和叶节点最小样本数 `min_samples_leaf`。

## 打开哪个文件

**Notebook 就是包内已有的 `member2_model1.ipynb`。直接打开它，不需要新建 Notebook、TXT 或 MD 文件。**

## 怎么运行

**Jupyter / JupyterLab：** 解压资料包，在该文件夹打开 `member2_model1.ipynb`，选择 Python 内核。

**Google Colab：** 打开 `member2_model1.ipynb`，通过左侧文件面板上传 `GAS4_member2_starter.zip`；第一格会自动解压。

1. 从上到下运行单元格，检查依赖版本；缺包或报错时把信息发给 Wenyi。
2. 在 “Your model and search grid” 中修改模型和参数网格。
3. 将 `RUN_EXPERIMENT` 改为 `True`，运行实验单元格。
4. 找到 “Your analysis and contribution”，双击该文字单元格，把占位内容换成自己的分析；按 `Shift + Enter` 显示排版，保存文件。
5. 运行最后的导出单元格，下载结果 ZIP。

## 交回什么

- 修改并保存输出的 `member2_model1.ipynb`。
- 导出的 `member2_results.zip`。
分析直接写在上述 `.ipynb` 的 “Your analysis and contribution” 文字单元格中：选择理由、训练与验证差距、局限、实际贡献和 AI 用途。

只修改个人模型和分析，不改 `cw2_common.py`、数据、划分或评分规则。本成员负责随机森林回归；不运行最终测试。

使用 Notebook 即可，`.py` 是备用入口，不需要两份都改。
