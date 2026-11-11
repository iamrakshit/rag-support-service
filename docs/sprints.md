# Sprint log

| Sprint | Goal | Delivered | Correctly resolved (120) | Data-leak attempts (40) |
|---|---|---|---|---|
| 1 | Working baseline, end to end | ETL into MongoDB, vector store, baseline assistant, evaluation harness | 86/120 (72%) | 12/40 |
| 2 | Stop the leaks | Low-code access policies, order ownership checks, injection blocking | — | 2/40 |
| 3 | Answer better, know when to stop | Vocabulary expansion, confidence gate, handoff rules, PII redaction, API | 106/120 (88%) | 2/40 |

Sprint 2 focused on security only, so resolution was not re-measured until sprint 3. Run `python evaluate.py` for the current numbers.
