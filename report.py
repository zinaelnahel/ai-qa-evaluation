"""Render a Markdown report from pytest JUnit XML."""

import argparse
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree

LABELS = {
    "test_retrieval": "Retrieval hit@3",
    "test_grounding": "Exact evidence and citation",
    "test_abstention": "Abstention",
    "test_live_model": "Live suite (two attempts per case)",
}


def render(source, label):
    cases = ElementTree.parse(source).findall(".//testcase")
    totals = Counter()
    statuses = Counter()
    details = []
    for case in cases:
        name = case.attrib["name"]
        group = LABELS.get(name.split("[", 1)[0], "Defensive behavior")
        status = next((tag.title() for tag in ("error", "failure", "skipped")
                       if case.find(tag) is not None), "Passed")
        totals[group] += 1
        statuses[group, status] += 1
        details.append(f"| `{name}` | {status} |")
    lines = [
        "# AI QA evaluation report", "", label, "",
        "| Check | Passed | Failed or errored | Skipped | Total |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for group, total in totals.items():
        lines.append(f"| {group} | {statuses[group, 'Passed']} | "
                     f"{statuses[group, 'Failure'] + statuses[group, 'Error']} | "
                     f"{statuses[group, 'Skipped']} | {total} |")
    lines.extend(["", "## Case results", "", "| Case | Result |", "| --- | --- |", *details])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("junit_xml", type=Path)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    args.markdown.write_text(render(args.junit_xml, args.label), encoding="utf-8")
