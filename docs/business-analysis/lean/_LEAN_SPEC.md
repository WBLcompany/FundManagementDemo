# Lean BRD — authoring spec (Epic → Feature → Use case → Stories)

Goal: replace the heavy BRD (96 use cases, ~850 requirements) with a short, releasable, testable specification
the team can build sprint by sprint. Readers: business owners, BA, developers, QA. Professional English, plain business language.

## Inputs
- Feature list, scope, acceptance criteria, dependencies, release: `/home/user/FundManagementDemo/docs/business-analysis/backlog/backlog_data.py`
  (feature keys there: F01…F13, F13B, F14…; the FINAL numbering is F01–F34 in list order — use the final IDs below).
- Detailed source per old use case: `/home/user/FundManagementDemo/docs/business-analysis/brd/<CODE>.json` (use_cases[].key/name/scenario/business_requirements/errors/fields; old UC numbers: PLT UC01–08, CFG UC09–18, PLN UC19–28, PRG UC29–38, PTL UC39–48, BEN UC49–58, REV UC59–68, PRJ UC69–78, FIN UC79–87, TSK UC88–96, in file order).
- The reviewer DELETED these requirements — do not reintroduce them: sign-in lock/throttle after failed attempts; excluding demo features from live service; public site showing only one grantor's opportunities; wording that registration link is for partners not grantors; message when the opportunities list is empty/fails; Arabic letter-variant equivalence in search; splitting long forms into guided steps.
- Terminology from reviewer: say "Charity" (الجمعية الخيرية) for the partner organization and "Grantor" / "the Foundation" for the grant-giving organization. The product is "Manih – Grant Management System".

## Epics and features (final IDs)
| Epic | Features |
|---|---|
| E1 Access & Roles | F01 Staff accounts and secure sign-in · F02 Role-based workspace · F29 Custom roles and permissions · F34 Multi-organization platform |
| E2 Charity Registry | F03 Charity self-registration · F04 Registration review and charity register · F05 Charity portal access and team · F06 Charity profile and verification |
| E3 Annual Plan & Budget | F07 Annual plan and budget structure · F24 Budget monitoring and adjustments · F25 Endowments |
| E4 Grant Opportunities | F08 Publish a grant opportunity · F09 Opportunities on the public page and portal · F10 Eligibility, groups and invitations · F28 Configuration library and governance |
| E5 Applications & Decisions | F11 Submit a grant application · F13 Application review by stages · F14 Evaluation criteria and pass score · F15 Charity follow-up and requested edits · F16 Committee decisions by minute |
| E6 Contracts & Projects | F17 Contract and project from an approved application · F18 Project plan and start of execution · F19 Charity progress reports and milestone approval · F20 Plan revisions and project closure |
| E7 Payments | F21 Payment approval chain · F22 Disbursement order, transfer and receipt · F23 Payments register and commitments |
| E8 Work Management & Insight | F12 My Tasks inbox · F26 Executive dashboard and reports · F27 Productivity tools |
| E9 Advanced Grants & AI | F30 AI assistance · F31 In-kind grants · F32 Tendered projects (RFP) · F33 Multi-project grants, merges and funding conditions |

Keep each feature's scope, release, priority, size and dependencies exactly as in backlog_data.py (do not add forward dependencies).

## Per feature, write
1. **summary** — 1–2 sentences: what and why.
2. **use_case** — ONE compact use case: actors, trigger, preconditions (≤3), main_flow (4–8 short steps), alternative_flows (0–3, "If …, then …"), business_rules (2–6 short rules). Only what is needed to build and test THIS feature.
3. **stories** — 2–6 user stories that together deliver the feature. Each story:
   - small enough for one developer in a few days, independently testable;
   - `As a <role>, I want <action>, so that <value>`;
   - 2–4 acceptance criteria in Given/When/Then, concrete and testable (values, statuses, messages);
   - optional `notes` (one line) for validation rules or fields that matter.
   Avoid stories for purely technical work. Do not repeat the same AC in several stories.
4. **decision** — the open business decision blocking Ready, or "" (keep the ones in backlog_data.py).
5. **old_ucs** — the old UC numbers covered (from backlog_data.py).

## Output — `/home/user/FundManagementDemo/docs/business-analysis/lean/<EPIC>.json`
```json
{"epic": "E3", "name": "Annual Plan & Budget", "goal": "one sentence business goal",
 "features": [{"id": "F07", "name": "...", "release": "R3", "priority": "Must", "size": "M", "depends_on": ["F02"],
   "summary": "...", "old_ucs": ["UC19"], "decision": "",
   "use_case": {"actors": ["Grants Manager"], "trigger": "...", "preconditions": ["..."], "main_flow": ["..."],
                "alternative_flows": ["..."], "business_rules": ["..."]},
   "stories": [{"id": "S-F07-01", "title": "Create the annual plan", "story": "As a ..., I want ..., so that ...",
                "acceptance": ["Given ... When ... Then ..."], "notes": ""}]}]}
```
Validate with `python3 -c "import json;json.load(open(PATH))"`. Do not edit other files; do not commit. Finish with counts (features, stories).
