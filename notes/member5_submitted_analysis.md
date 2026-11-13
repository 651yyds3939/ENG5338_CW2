# Member 5 submitted analysis

## Member 5 contribution and interpretation

### Measurement context

On 12 November 2026, I, Sauhandikaa Senthil Arumugam checked that all four selected pipelines could fit and predict with my local Python environment, then ran the project's existing benchmark_all() function to measure computational costs for the 22,191-row 2011–2013 development dataset. The same laptop and one numerical thread were used throughout: Windows 11 / Windows build 22631, eight logical CPU cores, 7.65 GiB RAM, Python 3.10.6, scikit-learn 1.7.2. The original benchmark samples and environment metadata are saved under results/member5_local_py310/ in my local repository.

### Computational findings

| Pipeline | Median training time (s) | Median single-row prediction (ms) | 1,000-row batch (ms) | Serialized size (KiB) |
|---|---:|---:|---:|---:|
| Linear Regression | 0.0205 | 0.6952 | 0.8243 | 1.5957 |
| Random Forest | 24.4929 | 27.1806 | 69.8337 | 24,068.3047 |
| Extra Trees | 5.2187 | 19.0255 | 56.0800 | 44,718.1787 |
| Histogram Gradient Boosting (HGBR) | 0.5542 | 2.8636 | 19.1155 | 364.9746 |

Linear Regression is quickest and smallest but has the worst recorded development-validation MAE (0.9073 mg/m³). Extra Trees achieves the best development-validation MAE (0.7226 mg/m³), but its median single-row latency is 19.03 ms. Random Forest is slower than Extra Trees in both fitting and single-row inference while having slightly worse validation MAE (0.7372 mg/m³). Among the nonlinear candidates, HGBR has the lowest measured fitting and inference costs (0.5542 s and 2.86 ms), at the cost of higher validation MAE (0.7655 mg/m³) than the other nonlinear candidates.

### Accuracy versus proposed constraints
Validation coverage within ±1 mg/m³ is 81.76% for Extra Trees, 81.18% for Random Forest, 79.15% for HGBR, and 71.80% for Linear Regression. On my laptop, only HGBR and Linear Regression meet the team's provisional 10 ms median single-row latency target. None achieves the provisional 90% development-validation coverage target. Consequently, no pipeline satisfies both proposed targets in the current evidence. The team should select a final candidate by explicitly weighing development-validation accuracy, operational cost and engineering priorities, not by declaring a single unconditional winner.

### Limitations and provenance
The development-validation accuracy figures in this notebook were loaded from the team's existing results/development/comparison.csv, generated with a different runtime (Python 3.12.9, scikit-learn 1.9.1). The computational figures were measured separately on my Python 3.10.6 / scikit-learn 1.7.2 Windows environment. The protocol and chosen configurations match, but cross-version differences mean these figures should be identified as combined evidence, not measurements from a single software environment. Wall-clock times vary with processor, system load, operating system and library implementations; they are not universal benchmarks. Memory increments based on sparse RSS samples are approximate and may understate actual peak memory. A zero recorded increment does not imply no memory use. No held-out 2014–2015 scores have been calculated.

### Actual contribution and AI disclosure
As Member 5, I configured and verified my own Python environment, checked the four models for basic compatibility, independently executed the four-model computational benchmark on my laptop, verified its saved runtime/protocol information and compared my timings with the team's recorded development accuracy. I interpreted the accuracy–latency trade-off and checked the provisional constraints. ChatGPT assisted with setup instructions, notebook verification/comparison code and drafting guidance. The common benchmark_all() implementation and older Linux reference run were generated during earlier Codex integration; I do not claim to have independently written that implementation or produced those earlier measurements. Final model selection and held-out testing require group agreement.