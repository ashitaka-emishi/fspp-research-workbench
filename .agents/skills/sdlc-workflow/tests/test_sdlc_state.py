from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sdlc_state.py"
SPEC = importlib.util.spec_from_file_location("sdlc_state", MODULE_PATH)
assert SPEC and SPEC.loader
sdlc_state = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sdlc_state)


def sections(headings: tuple[str, ...]) -> str:
    return "\n\n".join(f"## {heading}\n\nvalue" for heading in headings)


def contract_body(contract_type: str = "implementation-task", version: int = 1) -> str:
    return (
        f"<!-- fspp-issue-contract:v{version} type={contract_type} -->\n\n"
        f"{sections(sdlc_state.CONTRACT_HEADINGS)}\n"
    )


def closeout_body(version: int = 1, *, complete: bool = True) -> str:
    fields = ""
    if complete:
        fields = (
            "- Human approver: @maintainer\n"
            "- Accepted at: 2026-07-15T00:00:00Z\n"
            "- Result: accepted for merge\n\n"
        )
    remaining = sections(sdlc_state.CLOSEOUT_HEADINGS[1:])
    return (
        f"<!-- fspp-closeout:v{version} -->\n\n"
        f"## Issue closeout\n\n{fields}value\n\n{remaining}\n"
    )


def review_evidence_body(version: int = 1) -> str:
    return (
        contract_body("review-evidence-report")
        + f"\n<!-- fspp-review-evidence:v{version} -->\n\n"
        + sections(sdlc_state.REVIEW_EVIDENCE_HEADINGS)
        + "\n"
    )


def goal_usage_body(
    version: int = 1,
    *,
    scope: str = "milestone",
    status: str = "complete",
    risk: str = "high",
    assessment: str = "right-sized",
    tokens: int = 1000,
    elapsed: int = 60,
) -> str:
    return (
        contract_body("goal-usage-report")
        + f"\n<!-- fspp-goal-usage:v{version} -->\n\n"
        + "## Goal identity\n\n"
        + f"- Goal scope: {scope}\n"
        + "- Owner: #7\n"
        + "- Goal objective: produce a coherent outcome\n"
        + f"- Final status: {status}\n"
        + "- Completed at: 2026-07-15T00:00:00Z\n\n"
        + "## Final usage\n\n"
        + f"- Tokens used: {tokens}\n"
        + "- Token budget: not set\n"
        + f"- Elapsed seconds: {elapsed}\n\n"
        + "## Outcome shape\n\n"
        + "- Child issues completed: 3\n"
        + "- Pull requests merged: 3\n"
        + "- Human closeouts: 4\n"
        + f"- Risk and uncertainty: {risk}\n\n"
        + "## Sizing assessment\n\n"
        + f"- Assessment: {assessment}\n\n"
        + "The outcome remained coherent and the control points were useful.\n\n"
        + "## Future sizing recommendation\n\n"
        + "Retain one coherent outcome and review again with comparable evidence.\n"
    )


def issue(
    number: int,
    *,
    state: str = "OPEN",
    tracking: bool = False,
    contract: str | None = None,
    closeout: str | None = None,
) -> dict:
    return {
        "number": number,
        "title": f"Issue {number}",
        "state": state,
        "url": f"https://example.test/issues/{number}",
        "labels": [{"name": "tracking"}] if tracking else [],
        "body": contract if contract is not None else contract_body(),
        "comments": (
            [
                {
                    "body": closeout,
                    "author": {"login": "maintainer"},
                    "createdAt": "2026-07-15T00:00:00Z",
                    "url": f"https://example.test/issues/{number}#comment",
                }
            ]
            if closeout is not None
            else []
        ),
    }


class ContractReportTests(unittest.TestCase):
    def test_valid_contract_reports_marker_and_headings(self) -> None:
        report = sdlc_state.contract_report(
            contract_body("design-decision"),
            expected_type="design-decision",
        )
        self.assertEqual(report["state"], "valid")
        self.assertEqual(report["marker"], {"version": 1, "type": "design-decision"})
        self.assertEqual(report["errors"], [])

    def test_missing_marker_is_visible_as_legacy(self) -> None:
        report = sdlc_state.contract_report(sections(sdlc_state.CONTRACT_HEADINGS))
        self.assertEqual(report["state"], "legacy")
        self.assertIn("missing marker", report["errors"])

    def test_wrong_version_type_and_missing_heading_are_invalid(self) -> None:
        body = contract_body("wrong-type", version=2).replace(
            "## Permissions\n\nvalue\n\n",
            "",
        )
        report = sdlc_state.contract_report(body, expected_type="implementation-task")
        self.assertEqual(report["state"], "invalid")
        self.assertTrue(any("unsupported marker version" in error for error in report["errors"]))
        self.assertTrue(any("does not match" in error for error in report["errors"]))
        self.assertTrue(any("Permissions" in error for error in report["errors"]))

    def test_attempted_malformed_marker_is_not_reported_as_legacy(self) -> None:
        body = (
            "<!-- fspp-issue-contract:vX type=implementation-task -->\n\n"
            f"{sections(sdlc_state.CONTRACT_HEADINGS)}"
        )
        report = sdlc_state.contract_report(body)
        self.assertEqual(report["state"], "invalid")
        self.assertIn("malformed marker", report["errors"])


class CloseoutReportTests(unittest.TestCase):
    def test_finds_one_valid_marked_closeout(self) -> None:
        report = sdlc_state.closeout_report(
            [
                {"body": "ordinary comment"},
                {
                    "body": closeout_body(),
                    "author": {"login": "maintainer"},
                    "createdAt": "2026-07-15T00:00:00Z",
                    "url": "https://example.test/comment",
                },
            ]
        )
        self.assertEqual(report["state"], "valid")
        self.assertEqual(report["count"], 1)
        self.assertEqual(report["comments"][0]["author"], "maintainer")

    def test_duplicate_closeouts_are_not_silently_accepted(self) -> None:
        report = sdlc_state.closeout_report(
            [{"body": closeout_body()}, {"body": closeout_body()}]
        )
        self.assertEqual(report["state"], "multiple")

    def test_malformed_marked_closeout_is_invalid(self) -> None:
        report = sdlc_state.closeout_report([{"body": "<!-- fspp-closeout:v1 -->"}])
        self.assertEqual(report["state"], "invalid")

    def test_malformed_closeout_marker_is_counted_as_invalid(self) -> None:
        body = (
            "<!-- fspp-closeout:vX -->\n\n"
            f"{sections(sdlc_state.CLOSEOUT_HEADINGS)}"
        )
        report = sdlc_state.closeout_report([{"body": body}])
        self.assertEqual(report["state"], "invalid")
        self.assertEqual(report["count"], 1)

    def test_uncompleted_closeout_template_is_not_human_acceptance(self) -> None:
        report = sdlc_state.closeout_report([{"body": closeout_body(complete=False)}])
        self.assertEqual(report["state"], "invalid")
        errors = report["comments"][0]["document"]["errors"]
        self.assertTrue(any("human approver" in error for error in errors))

    def test_rejected_result_is_not_mistaken_for_acceptance(self) -> None:
        body = closeout_body().replace("Result: accepted for merge", "Result: not accepted")
        report = sdlc_state.closeout_report([{"body": body}])
        self.assertEqual(report["state"], "invalid")
        errors = report["comments"][0]["document"]["errors"]
        self.assertIn("result does not record acceptance", errors)


class TemplateValidationTests(unittest.TestCase):
    def test_validates_typed_issue_and_closeout_templates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issue_dir = root / ".github" / "ISSUE_TEMPLATE"
            issue_dir.mkdir(parents=True)
            (issue_dir / "implementation-task.md").write_text(
                contract_body("implementation-task"),
                encoding="utf-8",
            )
            (root / ".github" / "ISSUE_CLOSEOUT_TEMPLATE.md").write_text(
                closeout_body(),
                encoding="utf-8",
            )

            report = sdlc_state.validate_template_tree(root)
            self.assertTrue(report["valid"])
            self.assertEqual(report["errors"], [])

    def test_rejects_type_mismatch_and_missing_closeout_template(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issue_dir = root / ".github" / "ISSUE_TEMPLATE"
            issue_dir.mkdir(parents=True)
            (issue_dir / "implementation-task.md").write_text(
                contract_body("design-decision"),
                encoding="utf-8",
            )

            report = sdlc_state.validate_template_tree(root)
            self.assertFalse(report["valid"])
            self.assertTrue(any("does not match" in error for error in report["errors"]))
            self.assertTrue(any("missing closeout template" in error for error in report["errors"]))

    def test_validates_versioned_review_evidence_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issue_dir = root / ".github" / "ISSUE_TEMPLATE"
            issue_dir.mkdir(parents=True)
            (issue_dir / "review-evidence-report.md").write_text(
                review_evidence_body(),
                encoding="utf-8",
            )
            (root / ".github" / "ISSUE_CLOSEOUT_TEMPLATE.md").write_text(
                closeout_body(),
                encoding="utf-8",
            )

            report = sdlc_state.validate_template_tree(root)
            self.assertTrue(report["valid"])
            evidence = report["issue_templates"][0]["evidence_schema"]
            self.assertEqual(evidence["marker"], {"version": 1})

    def test_rejects_review_evidence_schema_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issue_dir = root / ".github" / "ISSUE_TEMPLATE"
            issue_dir.mkdir(parents=True)
            body = review_evidence_body(version=2).replace(
                "## Observations\n\nvalue\n\n",
                "",
            )
            (issue_dir / "review-evidence-report.md").write_text(body, encoding="utf-8")
            (root / ".github" / "ISSUE_CLOSEOUT_TEMPLATE.md").write_text(
                closeout_body(),
                encoding="utf-8",
            )

            report = sdlc_state.validate_template_tree(root)
            self.assertFalse(report["valid"])
            self.assertTrue(
                any("unsupported marker version 2" in error for error in report["errors"])
            )
            self.assertTrue(
                any(
                    "heading 'Observations' occurs 0 times" in error
                    for error in report["errors"]
                )
            )

    def test_validates_versioned_goal_usage_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issue_dir = root / ".github" / "ISSUE_TEMPLATE"
            issue_dir.mkdir(parents=True)
            (issue_dir / "goal-usage-report.md").write_text(
                goal_usage_body(),
                encoding="utf-8",
            )
            (root / ".github" / "ISSUE_CLOSEOUT_TEMPLATE.md").write_text(
                closeout_body(),
                encoding="utf-8",
            )

            report = sdlc_state.validate_template_tree(root)
            self.assertTrue(report["valid"])
            usage = report["issue_templates"][0]["usage_schema"]
            self.assertEqual(usage["marker"], {"version": 1})


class GoalUsageTests(unittest.TestCase):
    def test_completed_goal_usage_is_parsed(self) -> None:
        report = sdlc_state.goal_usage_document_report(
            goal_usage_body(tokens=75049, elapsed=213),
            require_completion=True,
        )
        self.assertEqual(report["state"], "valid")
        self.assertEqual(report["usage"]["tokens_used"], 75049)
        self.assertEqual(report["usage"]["token_budget"], "not set")

    def test_malformed_goal_usage_is_rejected(self) -> None:
        body = goal_usage_body().replace("- Tokens used: 1000", "- Tokens used: many")
        body = body.replace("- Risk and uncertainty: high", "- Risk and uncertainty: extreme")
        report = sdlc_state.goal_usage_document_report(body, require_completion=True)
        self.assertEqual(report["state"], "invalid")
        self.assertTrue(any("tokens used" in error for error in report["errors"]))
        self.assertTrue(any("risk and uncertainty" in error for error in report["errors"]))

    def test_placeholder_narrative_and_bad_timestamp_are_rejected(self) -> None:
        body = goal_usage_body().replace(
            "2026-07-15T00:00:00Z",
            "sometime",
        ).replace(
            "The outcome remained coherent and the control points were useful.",
            "<!-- explain sizing -->",
        )
        report = sdlc_state.goal_usage_document_report(body, require_completion=True)
        self.assertEqual(report["state"], "invalid")
        self.assertTrue(any("ISO 8601" in error for error in report["errors"]))
        self.assertIn("missing sizing assessment rationale", report["errors"])

    def test_fewer_than_three_comparable_records_is_insufficient(self) -> None:
        issues = [{"number": 1, "body": goal_usage_body(), "url": "one"}]
        report = sdlc_state.summarize_goal_usage(issues, scope="milestone", risk="high")
        self.assertEqual(report["evidence_state"], "insufficient")
        self.assertEqual(report["comparable_record_count"], 1)

    def test_three_comparable_records_produce_advisory_medians(self) -> None:
        issues = [
            {
                "number": index,
                "body": goal_usage_body(tokens=tokens, elapsed=elapsed, assessment="oversized"),
                "url": str(index),
            }
            for index, tokens, elapsed in ((1, 1000, 40), (2, 2000, 60), (3, 9000, 80))
        ]
        report = sdlc_state.summarize_goal_usage(issues, scope="milestone", risk="high")
        self.assertEqual(report["evidence_state"], "advisory")
        self.assertEqual(report["statistics"]["tokens_used"]["median"], 2000)
        self.assertIn("smaller coherent scope", report["sizing_signal"])


class MilestoneSummaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.milestone = {
            "number": 1,
            "title": "M1",
            "state": "open",
            "description": "Outcome",
            "open_issues": 1,
            "closed_issues": 1,
            "html_url": "https://example.test/milestone/1",
        }
        self.tracker = issue(
            1,
            tracking=True,
            contract=contract_body("milestone-tracking"),
        )

    def test_open_child_prevents_milestone_closeout(self) -> None:
        report = sdlc_state.summarize_milestone(self.milestone, [self.tracker, issue(2)])
        self.assertEqual(report["recommended_continuation"], "continue open child issues")
        self.assertFalse(report["summary"]["all_children_closed"])

    def test_legacy_closed_child_closeout_gap_is_visible(self) -> None:
        legacy = issue(2, state="CLOSED", contract="legacy issue body")
        report = sdlc_state.summarize_milestone(self.milestone, [self.tracker, legacy])
        self.assertEqual(
            report["recommended_continuation"],
            "review child closeout gaps before milestone closeout",
        )
        self.assertEqual(report["summary"]["closed_children_without_valid_closeout"], [2])

    def test_valid_child_and_tracker_closeouts_still_require_explicit_closure(self) -> None:
        tracker = issue(
            1,
            tracking=True,
            contract=contract_body("milestone-tracking"),
            closeout=closeout_body(),
        )
        child = issue(2, state="CLOSED", closeout=closeout_body())
        report = sdlc_state.summarize_milestone(self.milestone, [tracker, child])
        self.assertEqual(
            report["recommended_continuation"],
            "human closeout recorded; explicit milestone closure authorization required",
        )
        self.assertEqual(report["summary"]["outcome_acceptance"], "recorded")

    def test_missing_tracker_blocks_milestone_workflow(self) -> None:
        report = sdlc_state.summarize_milestone(self.milestone, [issue(2)])
        self.assertEqual(
            report["recommended_continuation"],
            "blocked: milestone tracking issue unavailable",
        )


class CommandFailureTests(unittest.TestCase):
    def test_inspect_milestone_fails_when_issue_state_is_unavailable(self) -> None:
        args = SimpleNamespace(milestone=1, repo="owner/repo", cwd=".", json=False)
        milestone = {
            "number": 1,
            "title": "M1",
            "state": "open",
            "html_url": "https://example.test/milestone/1",
        }
        failed = {"ok": False, "returncode": 1, "stdout": "", "stderr": "unavailable"}
        with (
            patch.object(sdlc_state, "resolve_repo", return_value=("owner/repo", None)),
            patch.object(
                sdlc_state,
                "gh_milestone",
                return_value=(milestone, {**failed, "ok": True}),
            ),
            patch.object(sdlc_state, "gh_milestone_issues", return_value=([], failed)),
            redirect_stdout(io.StringIO()) as output,
        ):
            result = sdlc_state.inspect_milestone(args)

        self.assertEqual(result, 1)
        self.assertIn("blocked: milestone issue state unavailable", output.getvalue())


if __name__ == "__main__":
    unittest.main()
