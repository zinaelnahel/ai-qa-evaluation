# AI QA evaluation for a policy assistant

A standalone Python and pytest project for evaluating a small retrieval-augmented generation system. The fixtures describe a fictional workplace. The assistant uses keyword overlap to rank policy records, limits retrieval to current approved records visible to the caller, and either returns one exact cited quote or abstains.

## Evidence

- [Labeled dataset](data/cases.json) with 20 scenarios covering paraphrases, stale policy, missing or conflicting evidence, unapproved content, and restricted records.
- [Offline results](OFFLINE_REPORT.md) with per-case results from the deterministic baseline.
- [Local model results](LIVE_REPORT.md) from a small Ollama evaluation.

| Quality question | Test oracle |
| --- | --- |
| Did retrieval find the relevant record? | Expected record ID appears in the first three results. |
| Does the answer match its citation? | Returned ID and exact quote match the labeled evidence. |
| Does the assistant abstain? | Expected abstention text and an empty citation for unknown, ambiguous, or restricted cases. |
| Can inappropriate content cross the evidence boundary? | A synthetic indirect prompt-injection fixture and restricted records are excluded from the generation context. Unexpected model fields and unsupported claims are rejected. |
| Can an authorized call affect a subsequent call? | A finance request returns its record. The following employee request abstains. |

## Reproduce the offline run

Use Python 3.12. Run the commands from this directory.

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -m "not live" --junitxml=results/offline.xml
python report.py results/offline.xml results/offline.md --label "Offline regression run"
```

The GitHub Actions workflow runs the offline suite on pushes and pull requests, adds a Markdown job summary, and uploads both the JUnit XML and readable report.

## Reproduce the local model run

With Ollama running locally and `qwen3:4b` installed, use PowerShell:

```powershell
$env:AI_QA_OLLAMA_MODEL = 'qwen3:4b'
python -m pytest -m live --junitxml=results/live.xml
python report.py results/live.xml results/live.md --label "Local Ollama qwen3:4b run"
```

The live suite covers six scenarios, with two attempts per scenario. Two scenarios should abstain before generation and verify that the model receives zero calls. For answerable scenarios, the model selects an exact quote and the same deterministic validator checks it. That restriction makes the result directly reproducible and limits what it says about free-form LLM output.

## Failure examples

| Input or condition | Expected result | What a regression would indicate |
| --- | --- | --- |
| A generated response cites the archived 20-day vacation policy. | The validator abstains. | An ineligible citation or unsupported policy quote reached the answer. |
| An unapproved record contains an instruction and a synthetic marker. | The generator receives only the current approved leave policy. | Unapproved content crossed the retrieval boundary. |

This suite evaluates a synthetic corpus and a single-quote policy assistant. The caller audience is supplied directly by the test harness. A production service would need to derive it from authenticated identity. The corpus has no real employee data and the scores apply only to the included cases.
