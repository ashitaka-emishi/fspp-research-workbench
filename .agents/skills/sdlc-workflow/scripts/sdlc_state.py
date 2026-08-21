#!/usr/bin/env python3
"""Deterministic state helpers for the SDLC workflow skill."""

from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any

CONTRACT_VERSION = 1
REVIEW_EVIDENCE_VERSION = 1
GOAL_USAGE_VERSION = 1
CONTRACT_MARKER = re.compile(
    r"<!--\s*fspp-issue-contract:v(?P<version>[0-9]+)\s+"
    r"type=(?P<type>[a-z0-9-]+)\s*-->",
)
CLOSEOUT_MARKER = re.compile(r"<!--\s*fspp-closeout:v(?P<version>[0-9]+)\s*-->")
REVIEW_EVIDENCE_MARKER = re.compile(
    r"<!--\s*fspp-review-evidence:v(?P<version>[0-9]+)\s*-->",
)
GOAL_USAGE_MARKER = re.compile(
    r"<!--\s*fspp-goal-usage:v(?P<version>[0-9]+)\s*-->",
)
CONTRACT_HEADINGS = (
    "Objective",
    "Governing sources",
    "Scope",
    "Suggested branch prefix",
    "Exclusions",
    "Constraints and invariants",
    "Expected evidence",
    "Permissions",
    "Stopping conditions",
)
CLOSEOUT_HEADINGS = (
    "Issue closeout",
    "Post-design mirror",
    "Intent-to-evidence reconciliation",
    "Knowledge reconciliation",
    "Remaining uncertainty",
    "Human acceptance",
)
REVIEW_EVIDENCE_HEADINGS = (
    "Review identity",
    "Design question",
    "Comparison controls",
    "Runs and metrics",
    "Observations",
    "Interpretation",
    "Uncertainty and limitations",
    "Proposed follow-up",
    "Knowledge reconciliation",
)
GOAL_USAGE_HEADINGS = (
    "Goal identity",
    "Final usage",
    "Outcome shape",
    "Sizing assessment",
    "Future sizing recommendation",
)


def run(cmd: list[str], cwd: str | None = None) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            cmd,
            cwd=cwd,
            check=False,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError:
        return {"ok": False, "returncode": 127, "stdout": "", "stderr": f"{cmd[0]} not found"}

    return {
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def load_json(cmd: list[str], cwd: str | None = None) -> tuple[Any | None, dict[str, Any]]:
    result = run(cmd, cwd)
    if not result["ok"]:
        return None, result
    try:
        return json.loads(result["stdout"] or "null"), result
    except json.JSONDecodeError as exc:
        result["ok"] = False
        result["stderr"] = f"failed to parse JSON: {exc}"
        return None, result


def heading_counts(body: str, headings: tuple[str, ...]) -> dict[str, int]:
    return {
        heading: len(re.findall(rf"^## {re.escape(heading)}$", body, re.MULTILINE))
        for heading in headings
    }


def marked_document_report(
    body: str,
    marker: re.Pattern[str],
    marker_token: str,
    headings: tuple[str, ...],
    *,
    missing_state: str,
    expected_type: str | None = None,
    expected_version: int = CONTRACT_VERSION,
) -> dict[str, Any]:
    matches = list(marker.finditer(body or ""))
    marker_attempted = marker_token in (body or "")
    counts = heading_counts(body or "", headings)
    errors: list[str] = []

    if not matches:
        errors.append("malformed marker" if marker_attempted else "missing marker")
    elif len(matches) > 1:
        errors.append(f"expected one marker, found {len(matches)}")

    marker_data: dict[str, Any] | None = None
    if matches:
        marker_data = {
            "version": int(matches[0].group("version")),
        }
        marker_type = matches[0].groupdict().get("type")
        if marker_type:
            marker_data["type"] = marker_type
        if marker_data["version"] != expected_version:
            errors.append(
                f"unsupported marker version {marker_data['version']}; expected {expected_version}",
            )
        if expected_type is not None and marker_type != expected_type:
            errors.append(f"marker type {marker_type!r} does not match {expected_type!r}")

    for heading, count in counts.items():
        if count != 1:
            errors.append(f"heading {heading!r} occurs {count} times")

    if not matches:
        state = "invalid" if marker_attempted else missing_state
    elif errors:
        state = "invalid"
    else:
        state = "valid"

    return {
        "state": state,
        "marker": marker_data,
        "headings": counts,
        "errors": errors,
    }


def contract_report(body: str, expected_type: str | None = None) -> dict[str, Any]:
    return marked_document_report(
        body,
        CONTRACT_MARKER,
        "fspp-issue-contract:",
        CONTRACT_HEADINGS,
        missing_state="legacy",
        expected_type=expected_type,
    )


def review_evidence_report(body: str) -> dict[str, Any]:
    return marked_document_report(
        body,
        REVIEW_EVIDENCE_MARKER,
        "fspp-review-evidence:",
        REVIEW_EVIDENCE_HEADINGS,
        missing_state="missing",
        expected_version=REVIEW_EVIDENCE_VERSION,
    )


def goal_usage_document_report(
    body: str,
    *,
    require_completion: bool = False,
) -> dict[str, Any]:
    report = marked_document_report(
        body,
        GOAL_USAGE_MARKER,
        "fspp-goal-usage:",
        GOAL_USAGE_HEADINGS,
        missing_state="missing",
        expected_version=GOAL_USAGE_VERSION,
    )
    if not require_completion or not GOAL_USAGE_MARKER.search(body or ""):
        return report

    fields = {
        "goal_scope": closeout_field(body, "Goal scope").lower(),
        "owner": closeout_field(body, "Owner"),
        "goal_objective": closeout_field(body, "Goal objective"),
        "final_status": closeout_field(body, "Final status").lower(),
        "completed_at": closeout_field(body, "Completed at"),
        "tokens_used": closeout_field(body, "Tokens used"),
        "token_budget": closeout_field(body, "Token budget").lower(),
        "elapsed_seconds": closeout_field(body, "Elapsed seconds"),
        "child_issues_completed": closeout_field(body, "Child issues completed"),
        "pull_requests_merged": closeout_field(body, "Pull requests merged"),
        "human_closeouts": closeout_field(body, "Human closeouts"),
        "risk_and_uncertainty": closeout_field(body, "Risk and uncertainty").lower(),
        "assessment": closeout_field(body, "Assessment").lower(),
        "assessment_rationale": section_content(body, "Sizing assessment"),
        "future_recommendation": section_content(body, "Future sizing recommendation"),
    }
    errors: list[str] = []
    for key in ("owner", "goal_objective", "completed_at"):
        if not fields[key]:
            errors.append(f"missing completed {key.replace('_', ' ')}")
    if fields["completed_at"] and not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})",
        fields["completed_at"],
    ):
        errors.append("completed at must be an ISO 8601 timestamp")
    enums = {
        "goal_scope": {"issue", "milestone"},
        "final_status": {"complete", "blocked"},
        "risk_and_uncertainty": {"low", "medium", "high"},
        "assessment": {"undersized", "right-sized", "oversized", "inconclusive"},
    }
    for key, choices in enums.items():
        if fields[key] not in choices:
            errors.append(f"{key.replace('_', ' ')} must be one of {', '.join(sorted(choices))}")

    numeric_fields = (
        "tokens_used",
        "elapsed_seconds",
        "child_issues_completed",
        "pull_requests_merged",
        "human_closeouts",
    )
    for key in numeric_fields:
        value = fields[key]
        if not value.isdigit():
            errors.append(f"{key.replace('_', ' ')} must be a non-negative integer")
        else:
            fields[key] = int(value)
    if fields["token_budget"] != "not set":
        if not fields["token_budget"].isdigit():
            errors.append("token budget must be a non-negative integer or 'not set'")
        else:
            fields["token_budget"] = int(fields["token_budget"])

    assessment_narrative = re.sub(
        r"<!--.*?-->",
        "",
        fields["assessment_rationale"],
        flags=re.DOTALL,
    )
    assessment_narrative = re.sub(
        r"^- Assessment:.*$",
        "",
        assessment_narrative,
        flags=re.MULTILINE,
    ).strip()
    recommendation_narrative = re.sub(
        r"<!--.*?-->",
        "",
        fields["future_recommendation"],
        flags=re.DOTALL,
    ).strip()
    if not assessment_narrative:
        errors.append("missing sizing assessment rationale")
    if not recommendation_narrative:
        errors.append("missing future sizing recommendation")

    report["usage"] = fields
    report["errors"].extend(errors)
    if report["state"] == "valid" and errors:
        report["state"] = "invalid"
    return report


def section_content(body: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}$\n(?P<content>.*?)(?=^## |\Z)",
        body,
        re.MULTILINE | re.DOTALL,
    )
    return match.group("content").strip() if match else ""


def closeout_field(body: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:[ \t]*(.*)$", body, re.MULTILINE)
    return match.group(1).strip() if match else ""


def closeout_document_report(body: str, *, require_completion: bool = False) -> dict[str, Any]:
    report = marked_document_report(
        body,
        CLOSEOUT_MARKER,
        "fspp-closeout:",
        CLOSEOUT_HEADINGS,
        missing_state="missing",
    )
    if not require_completion or not CLOSEOUT_MARKER.search(body or ""):
        return report

    completion = {
        "human_approver": closeout_field(body, "Human approver"),
        "accepted_at": closeout_field(body, "Accepted at"),
        "result": closeout_field(body, "Result"),
        "human_acceptance": section_content(body, "Human acceptance"),
    }
    completion_errors = []
    for key in ("human_approver", "accepted_at", "result", "human_acceptance"):
        if not completion[key]:
            completion_errors.append(f"missing completed {key.replace('_', ' ')}")
    if completion["result"] and not completion["result"].lower().startswith("accepted"):
        completion_errors.append("result does not record acceptance")
    if completion["human_acceptance"].startswith("Record the explicit human decision"):
        completion_errors.append("human acceptance still contains the template prompt")

    report["completion"] = completion
    report["errors"].extend(completion_errors)
    if report["state"] == "valid" and completion_errors:
        report["state"] = "invalid"
    return report


def closeout_report(comments: list[dict[str, Any]] | None) -> dict[str, Any]:
    closeouts = []
    for comment in comments or []:
        body = str(comment.get("body") or "")
        if "fspp-closeout:" not in body:
            continue
        document = closeout_document_report(body, require_completion=True)
        author = comment.get("author") or {}
        closeouts.append(
            {
                "url": comment.get("url"),
                "author": author.get("login") if isinstance(author, dict) else str(author),
                "created_at": comment.get("createdAt"),
                "document": document,
            }
        )

    if not closeouts:
        state = "missing"
    elif len(closeouts) > 1:
        state = "multiple"
    elif closeouts[0]["document"]["state"] == "valid":
        state = "valid"
    else:
        state = "invalid"

    return {
        "state": state,
        "count": len(closeouts),
        "comments": closeouts,
    }


def issue_pattern(issue: int) -> re.Pattern[str]:
    return re.compile(rf"(^|[^0-9]){re.escape(str(issue))}([^0-9]|$)")


def git_snapshot(issue: int, cwd: str | None) -> dict[str, Any]:
    status = run(["git", "status", "--short", "--branch"], cwd)
    if not status["ok"]:
        return {"available": False, "error": status["stderr"] or status["stdout"]}

    branch_result = run(["git", "branch", "--all", "--format=%(refname:short)"], cwd)
    branches: list[dict[str, str]] = []
    if branch_result["ok"]:
        pattern = issue_pattern(issue)
        for raw_name in branch_result["stdout"].splitlines():
            name = raw_name.strip()
            if not name or not pattern.search(name):
                continue
            kind = (
                "remote"
                if name.startswith("remotes/") or name.startswith("origin/")
                else "local"
            )
            branches.append({"name": name, "kind": kind})

    return {
        "available": True,
        "status": status["stdout"].splitlines(),
        "branches_for_issue": branches,
    }


def gh_issue(
    issue: int,
    repo: str | None,
    cwd: str | None,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    cmd = [
        "gh",
        "issue",
        "view",
        str(issue),
        "--json",
        "number,title,state,url,milestone,labels,assignees,projectItems,body,comments",
    ]
    if repo:
        cmd.extend(["--repo", repo])
    return load_json(cmd, cwd)


def resolve_repo(repo: str | None, cwd: str | None) -> tuple[str | None, dict[str, Any] | None]:
    if repo:
        return repo, None
    data, result = load_json(["gh", "repo", "view", "--json", "nameWithOwner"], cwd)
    return (data or {}).get("nameWithOwner"), result


def gh_milestone(
    milestone: int,
    repo: str,
    cwd: str | None,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    return load_json(
        ["gh", "api", f"repos/{repo}/milestones/{milestone}"],
        cwd,
    )


def gh_milestone_issues(
    title: str,
    repo: str,
    cwd: str | None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cmd = [
        "gh",
        "issue",
        "list",
        "--repo",
        repo,
        "--milestone",
        title,
        "--state",
        "all",
        "--limit",
        "200",
        "--json",
        "number,title,state,url,labels,body,comments",
    ]
    data, result = load_json(cmd, cwd)
    return data or [], result


def gh_goal_usage_issues(
    repo: str,
    cwd: str | None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    return load_json(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            repo,
            "--label",
            "goal-usage",
            "--state",
            "all",
            "--limit",
            "200",
            "--json",
            "number,title,state,url,body",
        ],
        cwd,
    )


def gh_prs(
    issue: int,
    repo: str | None,
    cwd: str | None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cmd = [
        "gh",
        "pr",
        "list",
        "--state",
        "open",
        "--search",
        str(issue),
        "--json",
        "number,title,body,headRefName,baseRefName,state,url,isDraft,reviewDecision,statusCheckRollup",
        "--limit",
        "50",
    ]
    if repo:
        cmd.extend(["--repo", repo])
    data, result = load_json(cmd, cwd)
    pattern = issue_pattern(issue)
    filtered = []
    for pr in data or []:
        haystack = "\n".join(str(pr.get(field) or "") for field in ("title", "body", "headRefName"))
        if f"#{issue}" in haystack or pattern.search(haystack):
            pr.pop("body", None)
            filtered.append(pr)
    return filtered, result


def gh_tracking_issues(
    milestone: dict[str, Any] | None,
    repo: str | None,
    cwd: str | None,
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    if not milestone or not milestone.get("title"):
        return [], None

    cmd = [
        "gh",
        "issue",
        "list",
        "--state",
        "open",
        "--label",
        "tracking",
        "--milestone",
        milestone["title"],
        "--json",
        "number,title,url,state,milestone",
        "--limit",
        "20",
    ]
    if repo:
        cmd.extend(["--repo", repo])
    data, result = load_json(cmd, cwd)
    return data or [], result


def continuation(
    issue_data: dict[str, Any] | None,
    git_data: dict[str, Any],
    prs: list[dict[str, Any]],
) -> str:
    if not issue_data:
        return "blocked: issue state unavailable"
    if issue_data.get("state") == "CLOSED":
        return "stop: issue is closed"
    if prs:
        return "inspect open PR before changing code"
    if not git_data.get("available"):
        return "blocked: local git state unavailable for branch decision"
    branches = git_data.get("branches_for_issue") or []
    if branches:
        return "inspect existing issue branch before creating new branch"
    return "start issue work from intended base branch"


def compact_checks(checks: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    compacted = []
    for check in checks or []:
        compacted.append(
            {
                "name": check.get("name") or check.get("context"),
                "status": check.get("status"),
                "conclusion": check.get("conclusion"),
            }
        )
    return compacted


def label_names(issue: dict[str, Any]) -> list[str]:
    return [label.get("name", "") for label in issue.get("labels", []) if label.get("name")]


def issue_workflow_report(issue: dict[str, Any]) -> dict[str, Any]:
    return {
        "number": issue.get("number"),
        "title": issue.get("title"),
        "state": issue.get("state"),
        "url": issue.get("url"),
        "labels": label_names(issue),
        "contract": contract_report(str(issue.get("body") or "")),
        "closeout": closeout_report(issue.get("comments")),
    }


def summarize_milestone(milestone: dict[str, Any], issues: list[dict[str, Any]]) -> dict[str, Any]:
    reports = [issue_workflow_report(issue) for issue in issues]
    trackers = [report for report in reports if "tracking" in report["labels"]]
    children = [report for report in reports if "tracking" not in report["labels"]]
    open_children = [report for report in children if report["state"] == "OPEN"]
    closed_children = [report for report in children if report["state"] == "CLOSED"]
    closeout_gaps = [
        report
        for report in closed_children
        if report["closeout"]["state"] != "valid"
    ]
    milestone_closeout_recorded = (
        len(trackers) == 1 and trackers[0]["closeout"]["state"] == "valid"
    )

    if not trackers:
        continuation = "blocked: milestone tracking issue unavailable"
    elif len(trackers) > 1:
        continuation = "blocked: multiple milestone tracking issues require human resolution"
    elif trackers[0]["contract"]["state"] != "valid":
        continuation = "repair milestone contract before closeout"
    elif open_children:
        continuation = "continue open child issues"
    elif closeout_gaps:
        continuation = "review child closeout gaps before milestone closeout"
    elif trackers[0]["closeout"]["state"] != "valid":
        continuation = "prepare human milestone closeout"
    elif milestone.get("state") == "open":
        continuation = "human closeout recorded; explicit milestone closure authorization required"
    else:
        continuation = "milestone is closed"

    return {
        "milestone": {
            "number": milestone.get("number"),
            "title": milestone.get("title"),
            "state": milestone.get("state"),
            "description": milestone.get("description"),
            "open_issues": milestone.get("open_issues"),
            "closed_issues": milestone.get("closed_issues"),
            "url": milestone.get("html_url"),
        },
        "tracking_issues": trackers,
        "children": children,
        "summary": {
            "open_children": len(open_children),
            "closed_children": len(closed_children),
            "closed_children_without_valid_closeout": [
                report["number"] for report in closeout_gaps
            ],
            "all_children_closed": not open_children,
            "outcome_acceptance": (
                "recorded" if milestone_closeout_recorded else "requires human milestone closeout"
            ),
        },
        "recommended_continuation": continuation,
    }


def summarize_goal_usage(
    issues: list[dict[str, Any]],
    *,
    scope: str | None = None,
    risk: str | None = None,
    status: str = "complete",
) -> dict[str, Any]:
    records = []
    invalid = []
    for issue in issues:
        document = goal_usage_document_report(str(issue.get("body") or ""), require_completion=True)
        item = {
            "number": issue.get("number"),
            "title": issue.get("title"),
            "url": issue.get("url"),
            "document": document,
        }
        if document["state"] != "valid":
            invalid.append(item)
            continue
        usage = document["usage"]
        if scope and usage["goal_scope"] != scope:
            continue
        if risk and usage["risk_and_uncertainty"] != risk:
            continue
        if status != "all" and usage["final_status"] != status:
            continue
        records.append(item)

    measures = (
        "tokens_used",
        "elapsed_seconds",
        "child_issues_completed",
        "pull_requests_merged",
        "human_closeouts",
    )
    statistics_report: dict[str, Any] = {}
    for measure in measures:
        values = [item["document"]["usage"][measure] for item in records]
        if values:
            median = statistics.median(values)
            statistics_report[measure] = {
                "minimum": min(values),
                "median": int(median) if float(median).is_integer() else median,
                "maximum": max(values),
            }

    assessments = {
        choice: 0
        for choice in ("undersized", "right-sized", "oversized", "inconclusive")
    }
    for item in records:
        assessments[item["document"]["usage"]["assessment"]] += 1

    if len(records) < 3:
        evidence_state = "insufficient"
        sizing_signal = "collect comparable records before deriving a sizing signal"
    else:
        conclusive = {key: value for key, value in assessments.items() if key != "inconclusive"}
        leader = max(conclusive, key=conclusive.get)
        leader_count = conclusive[leader]
        tied = list(conclusive.values()).count(leader_count) > 1
        if leader_count <= len(records) / 2 or tied:
            sizing_signal = "mixed evidence; retain human judgment"
        elif leader == "oversized":
            sizing_signal = "consider a smaller coherent scope for comparable goals"
        elif leader == "undersized":
            sizing_signal = "consider combining adjacent work only when coherence is preserved"
        else:
            sizing_signal = "retain the current scope shape for comparable goals"
        evidence_state = "advisory"

    return {
        "filters": {"scope": scope, "risk": risk, "status": status},
        "valid_records": records,
        "invalid_records": invalid,
        "comparable_record_count": len(records),
        "minimum_comparable_records": 3,
        "evidence_state": evidence_state,
        "statistics": statistics_report,
        "assessments": assessments,
        "sizing_signal": sizing_signal,
    }


def inspect_issue(args: argparse.Namespace) -> int:
    cwd = str(Path(args.cwd).resolve()) if args.cwd else None
    issue_data, issue_result = gh_issue(args.issue, args.repo, cwd)
    git_data = git_snapshot(args.issue, cwd)
    prs, pr_result = gh_prs(args.issue, args.repo, cwd)
    tracking, tracking_result = gh_tracking_issues(
        (issue_data or {}).get("milestone"),
        args.repo,
        cwd,
    )

    for pr in prs:
        pr["statusCheckRollup"] = compact_checks(pr.get("statusCheckRollup"))

    comments = issue_data.pop("comments", []) if issue_data else []
    contract = (
        contract_report(str((issue_data or {}).get("body") or ""))
        if issue_data
        else {"state": "unavailable"}
    )
    report = {
        "issue": issue_data,
        "contract": contract,
        "closeout": closeout_report(comments) if issue_data else {"state": "unavailable"},
        "git": git_data,
        "open_prs": prs,
        "tracking_issues": tracking,
        "recommended_continuation": continuation(issue_data, git_data, prs),
        "command_status": {
            "issue": command_summary(issue_result),
            "prs": command_summary(pr_result),
            "tracking": command_summary(tracking_result),
        },
    }

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text_report(report)

    return 0 if issue_data else 1


def inspect_milestone(args: argparse.Namespace) -> int:
    cwd = str(Path(args.cwd).resolve()) if args.cwd else None
    repo, repo_result = resolve_repo(args.repo, cwd)
    if not repo:
        report = {
            "milestone": None,
            "recommended_continuation": "blocked: repository state unavailable",
            "command_status": {"repo": command_summary(repo_result)},
        }
        if args.json:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            print("Milestone: unavailable")
            print("Recommended continuation: blocked: repository state unavailable")
        return 1

    milestone, milestone_result = gh_milestone(args.milestone, repo, cwd)
    issues: list[dict[str, Any]] = []
    issues_result: dict[str, Any] | None = None
    if milestone and milestone.get("title"):
        issues, issues_result = gh_milestone_issues(milestone["title"], repo, cwd)

    if milestone and issues_result and issues_result.get("ok"):
        report = summarize_milestone(milestone, issues)
    elif milestone:
        report = {
            "milestone": {
                "number": milestone.get("number"),
                "title": milestone.get("title"),
                "state": milestone.get("state"),
                "url": milestone.get("html_url"),
            },
            "tracking_issues": [],
            "children": [],
            "summary": {},
            "recommended_continuation": "blocked: milestone issue state unavailable",
        }
    else:
        report = {
            "milestone": None,
            "tracking_issues": [],
            "children": [],
            "summary": {},
            "recommended_continuation": "blocked: milestone state unavailable",
        }
    report["command_status"] = {
        "repo": command_summary(repo_result),
        "milestone": command_summary(milestone_result),
        "issues": command_summary(issues_result),
    }

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_milestone_report(report)
    return 0 if milestone and issues_result and issues_result.get("ok") else 1


def summarize_goal_usage_command(args: argparse.Namespace) -> int:
    cwd = str(Path(args.cwd).resolve()) if args.cwd else None
    repo, repo_result = resolve_repo(args.repo, cwd)
    if not repo:
        print("blocked: repository state unavailable", file=sys.stderr)
        return 1
    issues, issues_result = gh_goal_usage_issues(repo, cwd)
    if not issues_result.get("ok"):
        print("blocked: goal usage issue state unavailable", file=sys.stderr)
        return 1
    report = summarize_goal_usage(
        issues,
        scope=args.scope,
        risk=args.risk,
        status=args.status,
    )
    report["command_status"] = {
        "repo": command_summary(repo_result),
        "issues": command_summary(issues_result),
    }
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Comparable records: {report['comparable_record_count']}")
        print(f"Evidence state: {report['evidence_state']}")
        print(f"Sizing signal: {report['sizing_signal']}")
        print(f"Invalid records: {len(report['invalid_records'])}")
        for measure, values in report["statistics"].items():
            print(
                f"{measure.replace('_', ' ')}: "
                f"{values['minimum']} / {values['median']} / {values['maximum']} "
                "(min / median / max)"
            )
    return 0


def command_summary(result: dict[str, Any] | None) -> dict[str, Any] | None:
    if result is None:
        return None
    return {
        "ok": result["ok"],
        "returncode": result["returncode"],
        "stderr": result["stderr"],
    }


def print_text_report(report: dict[str, Any]) -> None:
    issue = report["issue"] or {}
    milestone = issue.get("milestone") or {}
    labels = ", ".join(label.get("name", "") for label in issue.get("labels", [])) or "none"

    print(f"Issue: #{issue.get('number', '?')} {issue.get('title', '(unavailable)')}")
    print(f"State: {issue.get('state', 'unknown')}")
    print(f"URL: {issue.get('url', 'unknown')}")
    print(f"Milestone: {milestone.get('title') or 'none'}")
    print(f"Labels: {labels}")
    contract = report["contract"]
    marker = contract.get("marker") or {}
    marker_label = ""
    if marker:
        marker_label = f" type={marker.get('type', 'n/a')} v{marker.get('version', '?')}"
    print(f"Contract: {contract.get('state', 'unknown')}{marker_label}")
    print(f"Closeout: {report['closeout'].get('state', 'unknown')}")
    print(f"Recommended continuation: {report['recommended_continuation']}")

    git_data = report["git"]
    print("\nGit:")
    if git_data.get("available"):
        print("  Status:")
        for line in git_data.get("status", []):
            print(f"    {line}")
        print("  Branches for issue:")
        branches = git_data.get("branches_for_issue") or []
        if branches:
            for branch in branches:
                print(f"    {branch['kind']}: {branch['name']}")
        else:
            print("    none")
    else:
        print(f"  unavailable: {git_data.get('error')}")

    print("\nOpen PRs matching issue:")
    if report["open_prs"]:
        for pr in report["open_prs"]:
            print(
                f"  #{pr['number']} {pr['title']} "
                f"({pr['headRefName']} -> {pr['baseRefName']}, draft={pr['isDraft']})"
            )
            print(f"    reviewDecision={pr.get('reviewDecision')} url={pr['url']}")
            for check in pr.get("statusCheckRollup", []):
                print(f"    check {check['name']}: {check['status']} / {check['conclusion']}")
    else:
        print("  none")

    print("\nOpen same-milestone tracking issues:")
    if report["tracking_issues"]:
        for item in report["tracking_issues"]:
            print(f"  #{item['number']} {item['title']} {item['url']}")
    else:
        print("  none")


def print_milestone_report(report: dict[str, Any]) -> None:
    milestone = report.get("milestone") or {}
    print(f"Milestone: #{milestone.get('number', '?')} {milestone.get('title', '(unavailable)')}")
    print(f"State: {milestone.get('state', 'unknown')}")
    print(f"URL: {milestone.get('url', 'unknown')}")
    print(f"Recommended continuation: {report['recommended_continuation']}")

    print("\nTracking issues:")
    trackers = report.get("tracking_issues") or []
    if trackers:
        for tracker in trackers:
            print(
                f"  #{tracker['number']} {tracker['title']} "
                f"state={tracker['state']} contract={tracker['contract']['state']} "
                f"closeout={tracker['closeout']['state']}",
            )
    else:
        print("  none")

    print("\nChild issues:")
    children = report.get("children") or []
    if children:
        for child in sorted(children, key=lambda item: item["number"] or 0):
            print(
                f"  #{child['number']} {child['title']} "
                f"state={child['state']} contract={child['contract']['state']} "
                f"closeout={child['closeout']['state']}",
            )
    else:
        print("  none")

    summary = report.get("summary") or {}
    print("\nAcceptance facts:")
    print(f"  all children closed: {summary.get('all_children_closed', False)}")
    gaps = summary.get("closed_children_without_valid_closeout") or []
    print(f"  closed children without valid closeout: {gaps or 'none'}")
    print(f"  outcome acceptance: {summary.get('outcome_acceptance', 'unknown')}")


def validate_template_tree(root: Path) -> dict[str, Any]:
    issue_dir = root / ".github" / "ISSUE_TEMPLATE"
    closeout_path = root / ".github" / "ISSUE_CLOSEOUT_TEMPLATE.md"
    issue_reports = []
    errors: list[str] = []

    issue_paths = sorted(issue_dir.glob("*.md")) if issue_dir.is_dir() else []
    if not issue_paths:
        errors.append(f"no Markdown issue templates found under {issue_dir}")

    for path in issue_paths:
        body = path.read_text(encoding="utf-8")
        report = contract_report(body, expected_type=path.stem)
        item = {"path": str(path.relative_to(root)), **report}
        if report["state"] != "valid":
            errors.extend(f"{path.relative_to(root)}: {error}" for error in report["errors"])
        if path.stem == "review-evidence-report":
            evidence = review_evidence_report(body)
            item["evidence_schema"] = evidence
            if evidence["state"] != "valid":
                errors.extend(
                    f"{path.relative_to(root)}: {error}" for error in evidence["errors"]
                )
        if path.stem == "goal-usage-report":
            usage = goal_usage_document_report(body)
            item["usage_schema"] = usage
            if usage["state"] != "valid":
                errors.extend(
                    f"{path.relative_to(root)}: {error}" for error in usage["errors"]
                )
        issue_reports.append(item)

    if closeout_path.is_file():
        closeout = closeout_document_report(closeout_path.read_text(encoding="utf-8"))
        closeout_report_data = {"path": str(closeout_path.relative_to(root)), **closeout}
        if closeout["state"] != "valid":
            errors.extend(
                f"{closeout_path.relative_to(root)}: {error}" for error in closeout["errors"]
            )
    else:
        closeout_report_data = {"path": str(closeout_path.relative_to(root)), "state": "missing"}
        errors.append(f"missing closeout template {closeout_path}")

    return {
        "valid": not errors,
        "issue_templates": issue_reports,
        "closeout_template": closeout_report_data,
        "errors": errors,
    }


def validate_templates(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    report = validate_template_tree(root)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for item in report["issue_templates"]:
            print(f"{item['path']}: {item['state']}")
        closeout = report["closeout_template"]
        print(f"{closeout['path']}: {closeout['state']}")
        if report["errors"]:
            print("\nErrors:")
            for error in report["errors"]:
                print(f"  {error}")
        else:
            print("\nTemplate schema valid.")
    return 0 if report["valid"] else 1


def tracker_entry(args: argparse.Namespace) -> int:
    checked = "x" if args.state.lower() == "closed" else " "
    title = args.title.strip()
    prefix = f"#{args.issue}"
    entry = f"- [{checked}] {prefix}"
    if title:
        entry += f" {title}"
    if args.url:
        entry += f" ({args.url})"
    if args.note:
        entry += f" - {args.note.strip()}"
    print(entry)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect deterministic SDLC workflow state from git and GitHub.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect = subparsers.add_parser(
        "inspect-issue",
        help="Report issue, branch, PR, and same-milestone tracking state.",
    )
    inspect.add_argument("issue", type=int, help="GitHub issue number")
    inspect.add_argument("--repo", help="GitHub repository in OWNER/REPO form")
    inspect.add_argument("--cwd", help="Git checkout to inspect; defaults to current directory")
    inspect.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    inspect.set_defaults(func=inspect_issue)

    milestone = subparsers.add_parser(
        "inspect-milestone",
        help="Report milestone contract, child issue, closeout, and acceptance state.",
    )
    milestone.add_argument("milestone", type=int, help="GitHub milestone number")
    milestone.add_argument("--repo", help="GitHub repository in OWNER/REPO form")
    milestone.add_argument("--cwd", help="Git checkout to inspect; defaults to current directory")
    milestone.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    milestone.set_defaults(func=inspect_milestone)

    usage = subparsers.add_parser(
        "summarize-goal-usage",
        help="Summarize comparable versioned goal-usage issue records.",
    )
    usage.add_argument("--repo", help="GitHub repository in OWNER/REPO form")
    usage.add_argument("--cwd", help="Git checkout to inspect; defaults to current directory")
    usage.add_argument("--scope", choices=("issue", "milestone"))
    usage.add_argument("--risk", choices=("low", "medium", "high"))
    usage.add_argument("--status", choices=("complete", "blocked", "all"), default="complete")
    usage.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    usage.set_defaults(func=summarize_goal_usage_command)

    templates = subparsers.add_parser(
        "validate-templates",
        help="Validate versioned issue-contract and closeout template schemas.",
    )
    templates.add_argument(
        "--root",
        default=".",
        help="Repository root; defaults to current directory",
    )
    templates.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    templates.set_defaults(func=validate_templates)

    tracker = subparsers.add_parser(
        "tracker-entry",
        help="Format a deterministic tracking checklist entry for an issue.",
    )
    tracker.add_argument("issue", type=int, help="GitHub issue number")
    tracker.add_argument("--title", default="", help="Issue title")
    tracker.add_argument("--state", choices=("open", "closed"), default="open", help="Issue state")
    tracker.add_argument("--url", help="Issue URL")
    tracker.add_argument("--note", help="Short tracker note to append")
    tracker.set_defaults(func=tracker_entry)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
