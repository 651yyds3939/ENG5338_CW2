# GAS4 模型比较与选型

目标是用九项环境和过程测量值预测同一时刻的 CO，单位为 mg/m³。四个模型使用同样的时间划分、五折验证和误差指标。每折在训练数据上拟合中位数填补；OLS 另外进行标准化。

| 模型 | 训练 MAE | 验证 MAE | 验证 RMSE | ±1 mg/m³ 覆盖率 | Windows 单条预测 |
|---|---:|---:|---:|---:|---:|
| OLS | 0.6732 | 0.9073 | 1.6892 | 71.80% | 0.70 ms |
| Random Forest | 0.4140 | 0.7372 | 1.5079 | 81.18% | 27.18 ms |
| Extra Trees | 0.4093 | 0.7226 | 1.4735 | 81.76% | 19.03 ms |
| HGB | 0.4111 | 0.7655 | 1.4657 | 79.15% | 2.86 ms |

准确性来自统一 Linux 环境下的五折验证，耗时来自成员 5 的 Windows 笔记本实测。数字来源：[验证表](../../results/development/comparison.csv)、[计时表](../../results/member5_local_py310/comparison.csv)。

## 四个模型

- OLS：拟合线性关系，作为线性基准。
- Random Forest：对多个使用 bootstrap 样本的回归树取平均。当前使用 600 棵树、深度 11、叶节点最少 20 个样本、max_features=0.5、max_samples=0.9。
- Extra Trees：在分裂阈值中增加随机性，再对多棵树取平均。当前使用 400 棵树、深度 14、叶节点最少 10 个样本、max_features=0.8、bootstrap=False。
- HGB：逐轮增加基于直方图的树，减少剩余损失。当前使用 200 轮、学习率 0.05、15 个叶节点、叶节点最少 20 个样本、L2=1、early_stopping=False。

成员最新搜索包含 RF 3 组、Extra Trees 27 组、HGB 8 组参数；统一环境已复跑这 38 组、共 190 次交叉验证拟合。原始数值记录在 results/submitted，复跑记录在 results/search_reproduction。

## 当前推荐

按预测 MAE 优先选择 Extra Trees：验证 MAE 最低、覆盖率最高。HGB 的验证 RMSE 最低，非线性模型中预测速度最快。报告同时列出精度和计算成本。

Extra Trees 在 2014–2015 年的评估结果是 MAE 0.8011、RMSE 1.3654、R² 0.6111、覆盖率 73.36%。此前先评估过 HGB，MAE 为 0.8998、覆盖率 70.00%；随后按已有开发验证排名改选 Extra Trees，再评估相同年份。CW1 也使用过这些年份。两份记录均保留，下一阶段使用新的未来时期继续验证。

在超过各折训练 CO 第 95 百分位数的验证样本中，Extra Trees 覆盖率为 26.68%，平均有符号误差为 −1.9672 mg/m³。后续重点是高 CO 数据和跨时间表现。90% 是本项目设定的覆盖率目标；当前选择以 MAE 为优先，原先的 10 ms 数字保留为耗时参考线。

[Notebook 说明](Notebook解读与问答_zh.md) · [提交说明](提交与答辩说明_zh.md)
