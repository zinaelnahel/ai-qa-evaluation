# AI QA evaluation report

Local offline baseline using Python 3.12 and pytest 9.2.0.

| Check | Passed | Failed or errored | Skipped | Total |
| --- | ---: | ---: | ---: | ---: |
| Retrieval hit@3 | 15 | 0 | 0 | 15 |
| Exact evidence and citation | 15 | 0 | 0 | 15 |
| Abstention | 5 | 0 | 0 | 5 |
| Defensive behavior | 8 | 0 | 0 | 8 |

## Case results

| Case | Result |
| --- | --- |
| `test_retrieval[leave-days]` | Passed |
| `test_retrieval[leave-paraphrase]` | Passed |
| `test_retrieval[leave-archived-conflict]` | Passed |
| `test_retrieval[expense-deadline]` | Passed |
| `test_retrieval[expense-paraphrase]` | Passed |
| `test_retrieval[laptop-replacement]` | Passed |
| `test_retrieval[laptop-paraphrase]` | Passed |
| `test_retrieval[remote-work]` | Passed |
| `test_retrieval[remote-paraphrase]` | Passed |
| `test_retrieval[training-allowance]` | Passed |
| `test_retrieval[training-paraphrase]` | Passed |
| `test_retrieval[it-contact]` | Passed |
| `test_retrieval[it-paraphrase]` | Passed |
| `test_retrieval[authorized-record]` | Passed |
| `test_retrieval[unapproved-record]` | Passed |
| `test_grounding[leave-days]` | Passed |
| `test_grounding[leave-paraphrase]` | Passed |
| `test_grounding[leave-archived-conflict]` | Passed |
| `test_grounding[expense-deadline]` | Passed |
| `test_grounding[expense-paraphrase]` | Passed |
| `test_grounding[laptop-replacement]` | Passed |
| `test_grounding[laptop-paraphrase]` | Passed |
| `test_grounding[remote-work]` | Passed |
| `test_grounding[remote-paraphrase]` | Passed |
| `test_grounding[training-allowance]` | Passed |
| `test_grounding[training-paraphrase]` | Passed |
| `test_grounding[it-contact]` | Passed |
| `test_grounding[it-paraphrase]` | Passed |
| `test_grounding[authorized-record]` | Passed |
| `test_grounding[unapproved-record]` | Passed |
| `test_abstention[unknown-parking]` | Passed |
| `test_abstention[unknown-relocation]` | Passed |
| `test_abstention[ambiguous-topic]` | Passed |
| `test_abstention[restricted-record]` | Passed |
| `test_abstention[cross-session]` | Passed |
| `test_isolation_after_authorized_request` | Passed |
| `test_ambiguous_query_has_competing_evidence` | Passed |
| `test_only_approved_evidence_reaches_generation` | Passed |
| `test_restricted_evidence_never_reaches_generation` | Passed |
| `test_untrusted_model_output[unsupported-quote]` | Passed |
| `test_untrusted_model_output[archived-citation]` | Passed |
| `test_untrusted_model_output[extra-field]` | Passed |
| `test_untrusted_model_output[malformed-response]` | Passed |
