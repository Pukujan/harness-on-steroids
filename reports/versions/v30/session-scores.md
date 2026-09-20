# Session scores vs Work-gold R1/R2/R5/R6

No bodies. Work: never send first; apply_patch after exec-run 0; write-rate 0.01.

## kilo.db

- sessions_with_tools: **13**
- **Work-match (R1∧R2∧R3∧R4∧R5∧R6): 1** / 13 (0.08)
- R1 look-first: **13**
- R3 read-first (not bash): **10** (Work first=exec 79, shell 2)
- bash-first: **1**
- R2 no-write: **2**
- R5 no-write-after-look-run: **2** (Work apply_patch after exec-run 0)
- R4 no-todowrite: **7** (Work update_plan 0)
- todowrite sessions: **6**
- wrote-without-task: **11**
- R6 decompose-not-first: **11**
- decompose-first: **2**
- write-rate: **0.85** (Work gold 1/87 ≈ 0.01)
- write-first: **0**
- median start look-burst: **6** (Work exec-run median 3)
- median tools before write: **51**
- median tools before task/todo: **3** (Work send median 15)
- skipped_study_os: **0**
- skipped_plan_agent: **7**
- wrote: **11**
- sandwich look-after-write: **11**
- multi_piece (task/wait-ish, not todowrite): **3**

| first | n |
| --- | --- |
| read | 7 |
| glob | 1 |
| todowrite | 1 |
| skill | 1 |
| agent_manager | 1 |
| kilo_local_recall | 1 |
| bash | 1 |

| fail_mask | n |
| --- | --- |
| R2+R4+R5 | 5 |
| R2+R5 | 4 |
| R2+R3+R4+R5+R6 | 1 |
| R3+R6 | 1 |
| none | 1 |
| R2+R3+R5 | 1 |

## opencode.db

- sessions_with_tools: **21**
- **Work-match (R1∧R2∧R3∧R4∧R5∧R6): 4** / 21 (0.19)
- R1 look-first: **20**
- R3 read-first (not bash): **5** (Work first=exec 79, shell 2)
- bash-first: **10**
- R2 no-write: **8**
- R5 no-write-after-look-run: **9** (Work apply_patch after exec-run 0)
- R4 no-todowrite: **11** (Work update_plan 0)
- todowrite sessions: **10**
- wrote-without-task: **9**
- R6 decompose-not-first: **16**
- decompose-first: **5**
- write-rate: **0.62** (Work gold 1/87 ≈ 0.01)
- write-first: **1**
- median start look-burst: **7** (Work exec-run median 3)
- median tools before write: **18**
- median tools before task/todo: **16** (Work send median 15)
- skipped_study_os: **53**
- skipped_plan_agent: **3**
- wrote: **13**
- sandwich look-after-write: **12**
- multi_piece (task/wait-ish, not todowrite): **5**

| first | n |
| --- | --- |
| bash | 10 |
| todowrite | 3 |
| glob | 2 |
| task | 2 |
| read | 2 |
| webfetch | 1 |
| write | 1 |

| fail_mask | n |
| --- | --- |
| R2+R3+R4+R5 | 6 |
| none | 4 |
| R3 | 3 |
| R2+R3+R4+R5+R6 | 3 |
| R3+R6 | 1 |
| R2+R3+R6 | 1 |
| R1+R2+R3+R5 | 1 |
| R2+R3+R5 | 1 |
| R2+R4+R5 | 1 |
