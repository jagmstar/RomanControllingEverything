#!/usr/bin/env python3
"""
Non-LLM gate for closing tickets in RomanControllingEverything.
Only this script may transition tickets to CLOSED.
Usage: python close_ticket.py <issue_number>
"""
import subprocess
import sys
import re

REPO = "jagmstar/RomanControllingEverything"

def get_comments(issue):
    result = subprocess.run(
        ["gh", "issue", "view", issue, "--repo", REPO, "--json", "comments"],
        capture_output=True, text=True
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
        if not re.search(r"^\[(Architect|DevOps|Dev|QA-Engineer|AI-Engineer|UI-UX-Designer|BA|CTO|Reviewer|Audit-Agent)\]", body, re.MULTILINE):
            continue
        # Must contain command output markers
        if any(marker in body for marker in ["```", "$ ", "> ", "python ", "pytest ", "git ", "gh "]):
            return True
    return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python close_ticket.py <issue_number>")
        sys.exit(1)
    issue = sys.argv[1]
    comments = get_comments(issue)
    if comments is None:
        sys.exit(1)
    if not has_command_output_evidence(comments):
        print(f"FAIL: issue #{issue} lacks role-prefixed command-output evidence")
        sys.exit(1)
    result = subprocess.run(
        ["gh", "issue", "close", issue, "--repo", REPO,
         "--comment", f"[Gate] Evidence verified. Closing via non-LLM gate."],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"FAIL: cannot close issue {issue}: {result.stderr}")
        sys.exit(1)
    print(f"PASS: issue #{issue} closed by gate")

if __name__ == "__main__":
    main()
