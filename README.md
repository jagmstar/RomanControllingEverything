# RomanControllingEverything

Company control board for Roman's AI-SDLC virtual company.

## Purpose
This repo tracks team accountability, fuckups, action plans, and audit results. It is not a code repo — it is the operational control plane.

## AI-SDLC Flow

1. PMO creates/assigns ticket
2. Role does work and posts `[Role]` evidence comment
3. QA verifies with live command output
4. Reviewer reviews
5. Non-LLM gate checks evidence and closes ticket

## Evidence Standard

Every closure must include one of:
- Commit hash + command output
- Test command + output
- Link to PR with reproducible proof

## Role Prefixes (Mandatory)

[PMO], [QAO], [SEDO], [DevOps], [AI-Engineer], [Architect], [Dev], [QA-Engineer], [Reviewer], [CTO], [CEO], [CFO], [CMO]

## Forbidden

- No agent closes a ticket without gate approval
- No fake ticket references (#0)
- No prose-only closure comments

## Active Epics

- #205 AI-SDLC flow fix + close remaining 37 tickets

## Links

- [Discussions](https://github.com/jagmstar/RomanControllingEverything/discussions)
- [Actions](https://github.com/jagmstar/RomanControllingEverything/actions)
- [Issues](https://github.com/jagmstar/RomanControllingEverything/issues)
