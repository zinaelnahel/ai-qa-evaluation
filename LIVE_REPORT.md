# AI QA evaluation report

Local Ollama qwen3:4b smoke run. Eight model calls and four pre-generation abstentions across six scenarios.

| Check | Passed | Failed or errored | Skipped | Total |
| --- | ---: | ---: | ---: | ---: |
| Live suite (two attempts per case) | 6 | 0 | 0 | 6 |

## Case results

| Case | Result |
| --- | --- |
| `test_live_model[leave-archived-conflict]` | Passed |
| `test_live_model[expense-paraphrase]` | Passed |
| `test_live_model[it-contact]` | Passed |
| `test_live_model[unknown-parking]` | Passed |
| `test_live_model[restricted-record]` | Passed |
| `test_live_model[unapproved-record]` | Passed |
