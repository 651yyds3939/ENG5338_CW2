# English editions and repository cleanup

Prepared on **9 November 2026** at Wenyi's request. Chinese originals are retained; the default overview and allocation are now English. This is file organisation and translation, not final coursework submission or GitHub publication.

## Document pairs

| English edition | Chinese original |
|---|---|
| [Main README](../README.md) | [Chinese overview](zh/README.md) |
| [Current task allocation](../TASK_ALLOCATION.md) | [Chinese allocation](zh/TASK_ALLOCATION.md) |
| [Project explanation](en/PROJECT_GUIDE.md) | [Project explanation, Chinese](zh/项目全解读_CW1与CW2对照_zh.md) |
| [Model guide](en/MODEL_GUIDE.md) | [Model guide, Chinese](zh/候选模型说明与选型建议_zh.md) |
| [Requirements and plan](en/REQUIREMENTS_AND_PLAN.md) | [Planning notes, Chinese](zh/需求检查与周一讨论_zh.md) |
| [Notebook guide and Q&A](en/NOTEBOOK_GUIDE.md) | [Notebook guide, Chinese](zh/Notebook解读与问答_zh.md) |
| [Handoff overview](../member_handoff/README.md) | [Handoff overview, Chinese](../member_handoff/交接说明.md) |
| [Member 2 instructions](../member_handoff/member2_README.md) | [Member 2 instructions, Chinese](../member_handoff/member2_交接说明.md) |

English editions cover the original technical explanations and identify the current fixed RF/Extra Trees/HGB allocation. Alternative models and historical A–E proposals in early Chinese study material do not supersede the current allocation. Members 3 and 4 already had English instructions.

The English and Chinese allocation images are retained as separate language editions. The English image remains at the project root for easy sharing. Original course PDFs/TeX remain at the root. A subsequent privacy audit moved the supplied personal screenshot and machine-wide package inventory to an ignored local backup, outside the published file set.

## Removed redundant files

- `member_handoff/packages/GAS4_member2_starter/`: verified byte-for-byte against the corresponding ZIP, then removed. It contained no member edits or executed outputs.
- `member_handoff/__pycache__/`: automatically generated Python bytecode cache.
- `figures/GAS4_Team_Task_Allocation_EN.png`: exact duplicate of the retained root image. The English drawing script now writes to the retained root location.
- `build_notebook.py`: obsolete initial constructor that duplicated and could overwrite the maintained master notebook. The master notebook, execution runner and personal-starter builder are retained.

Added `.gitignore` for local environments, caches and duplicate extracted starter folders. It does not ignore the dataset, ZIP handoffs or actual result evidence.

## Verification

- Local Markdown links resolve after Chinese-document relocation.
- Python sources parse successfully; notebooks are structurally valid.
- All three starter ZIPs pass integrity checks and contain matching code/data.
- Member 2's ZIP now includes both Chinese instructions and English `README.md`; members 3/4 retain English instructions.
- SHA-256 checks confirm the master notebook, dataset, shared experiment module and every existing main result file are unchanged.
- No candidate was fitted, no final-test evaluation ran, and no Git repository or remote was created.

The machine-readable check record is [cleanup_verification.json](cleanup_verification.json). Actual experimental run state remains in `results/`.

This records the initial translation/cleanup operation. For the later publication privacy and standalone-run checks, use [the publication audit](PUBLICATION_AUDIT.md).
