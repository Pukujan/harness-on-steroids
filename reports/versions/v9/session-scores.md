# Session scores vs Work-gold R1/R2/R5/R6

No bodies. Work: never send first; apply_patch after exec-run 0; write-rate 0.01.

## kilo.db

- sessions_with_tools: **17**
- R1 look-first: **17**
- R2 no-write: **2**
- R5 no-write-after-look-run: **2** (Work apply_patch after exec-run 0)
- R6 decompose-not-first: **16**
- decompose-first: **1**
- write-rate: **0.88** (Work gold 1/85 ≈ 0.01)
- write-first: **0**
- median start look-burst: **20** (Work exec-run median 3)
- median tools before write: **39**
- median tools before task/todo: **25** (Work send median 15)
- skipped_study_os: **0**
- wrote: **15**
- sandwich look-after-write: **15**
- multi_piece (task/todo/wait-ish): **10**

| first | n |
| --- | --- |
| read | 9 |
| skill | 3 |
| kilo_local_recall | 3 |
| agent_manager | 1 |
| bash | 1 |

## opencode.db

- sessions_with_tools: **24**
- R1 look-first: **23**
- R2 no-write: **11**
- R5 no-write-after-look-run: **12** (Work apply_patch after exec-run 0)
- R6 decompose-not-first: **16**
- decompose-first: **8**
- write-rate: **0.54** (Work gold 1/85 ≈ 0.01)
- write-first: **1**
- median start look-burst: **4** (Work exec-run median 3)
- median tools before write: **18**
- median tools before task/todo: **0** (Work send median 15)
- skipped_study_os: **53**
- wrote: **13**
- sandwich look-after-write: **12**
- multi_piece (task/todo/wait-ish): **16**

| first | n |
| --- | --- |
| bash | 10 |
| todowrite | 6 |
| glob | 2 |
| task | 2 |
| read | 2 |
| webfetch | 1 |
| write | 1 |
