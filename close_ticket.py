#!/usr/bin/env python3
"""
Non-LLM gate for closing tickets across all twin project repos.
Usage: python close_ticket.py --repo OWNER/REPO --issue NUMBER [--reason TEXT]
"""
import subprocess
import sys
import re
import argparse

ALLOWED_ROLES = r"(Architect|DevOps|Dev|QA-Engineer|AI-Engineer|UI-UX-Designer|BA|CTO|Reviewer|Audit-Agent|PMO|SEDO-Lead|QA-Lead|DevOps-Lead|Memory-Architect|Memory-Warden|CEO|CMO|ResearchO-Lead|CFO|CISO|CFO-Twin|CEO-Twin|CTO-Twin|CMO-Twin|PMO-Twin)"

def get_comments(repo, issue):
    result = subprocess.run(
        ["gh", "issue", "view", issue, "--repo", repo, "--json", "comments"],
        capture_output=True, text=True, encoding='utf-8'
    )
    if result.returncode != 0:
        print(f"FAIL: cannot fetch issue {issue}: {result.stderr}")
        return None
    import json
    data = json.loads(result.stdout)
    return data.get("comments", [])

def has_command_output_evidence(comments):
    """Check for role-prefixed comment with command output evidence."""
    for c in comments:
        body = c.get("body", "")
        # Must have role prefix
        if not re.search(r"^\[" + ALLOWED_ROLES + r"\]", body, re.MULTILINE):
            continue
        # Must contain command output markers
        if any(marker in body for marker in ["```", "$ ", "> ", "python ", "pytest ", "git ", "gh "]):
            return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--issue", required=True)
    parser.add_argument("--reason", default="Evidence verified. Closing via non-LLM gate.")
    args = parser.parse_args()

    comments = get_comments(args.repo, args.issue)
    if comments is None:
        sys.exit(1)
    if not has_command_output_evidence(comments):
        print(f"FAIL: issue #{args.issue} in {args.repo} lacks role-prefixed command-output evidence")
        sys.exit(1)
    result = subprocess.run(
        ["gh", "issue", "close", args.issue, "--repo", args.repo,
         "--comment", f"[Gate] {args.reason}"],
        capture_output=True, text=True, encoding='utf-8'
    )
    if result.returncode != 0:
        print(f"FAIL: cannot close issue {args.issue}: {result.stderr}")
        sys.exit(1)
    print(f"PASS: issue #{args.issue} in {args.repo} closed by gate")

if __name__ == "__main__":
    main()
