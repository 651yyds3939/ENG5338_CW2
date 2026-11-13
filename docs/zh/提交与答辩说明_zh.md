# GAS4 提交与答辩

提交文件在 `submission/`：报告 PDF、幻灯片 PDF、已执行的主 Notebook。文件夹还包含可编辑 PPTX、10 分钟讲稿、答辩准备和完整复现 ZIP。

## 模型与结果

推荐 Extra Trees：400 棵树、深度 14、叶节点最少 10 个样本、max_features=0.8。开发验证 MAE 为 0.7226 mg/m³，coverage 为 81.76%；单条预测 19.03 ms。2014–2015 评估 MAE 为 0.8011 mg/m³，coverage 为 73.36%。项目目标是 90% 的预测落在 ±1 mg/m³ 内，当前评估还差 16.64 个百分点。

## 实验记录

先完成 HGB 评估：MAE 0.8998，coverage 70.00%。你随后决定优先预测精度，按已有开发验证排名选择 Extra Trees，再对相同 2014–2015 数据评估。CW1 也使用过这些年份。两份结果分别保存在 results/final 和 results/final_extra_trees。下一阶段使用新的未来时期数据继续验证。

## 运行与提交

安装 requirements.lock.txt 后，运行 `python run_notebook.py`。完整项目包含 src、数据、搜索记录、计时样本和预测结果。报告正文 7 页、附录 1 页、贡献声明另 1 页；幻灯片 11 页，计划讲 10 分钟，随后回答 10 分钟问题。

五位成员学号均已补齐，统一使用 7 位数字；贡献声明等待全员确认。上传前核对姓名、数字和分工，准备整个 Notebook 的问答。发布状态：待推送 GitHub、待上传 Moodle。Moodle 页面提供截止时间和上传回执。
