# Business Analysis Package — Authoring Spec (shared by all module analysts)

Source prototype: `/home/user/manih` (Lovable-built grant-management POC "Manih", Arabic RTL UI, React + TanStack Router + Supabase). Live demo: https://manih.lovable.app (NOT inspected live — analysis is from source code only).

Read `/home/user/manih/AGENTS.md` first — it lists the architecture and business-rule decisions. Then read every file in your module scope (routes, components, lib). Look at `src/integrations/supabase/types.ts` only for the tables you need, and `supabase/migrations/*.sql` for constraints / triggers / RLS relevant to you.

## Roles (from src/lib/persona.tsx + AppShell NAV_BY_ROLE)
`admin`, `grants_manager`, `reviewer`, `committee_secretary`, `project_manager`, `finance`, `ceo`, `applicant` (partner organization user, sees only /portal). The prototype switches personas through a demo "persona switcher" on one shared demo account (no real per-user auth) — permission differences are UI-level only unless you find enforcement in lib code. Say so where relevant.

Role → sidebar: applicant: portal · reviewer: dashboard(analytics), tasks, applications(reviewer), beneficiaries · committee_secretary: tasks, applications · grants_manager: dashboard, plans, tasks, applications, projects, beneficiaries, settings · project_manager: tasks, projects · finance: dashboard, plans, tasks, projects · ceo: dashboard, plans, tasks, applications, projects · admin: all of grants_manager.

## Evidence labels (mandatory on every rule/requirement/behaviour)
- **[Observed]** — implemented in code (cite `file:line` or `file` + function).
- **[Inferred]** — reasonable reading of code intent, not explicit.
- **[Recommended]** — analyst proposal, not in prototype.
- **[To Confirm]** — business decision / value / role that must be confirmed by stakeholders.
Never fabricate screens, fields or rules. Do not invent business value — if not evident, write "[To Confirm]".

## ID scheme (stable; use your module CODE)
- Screen: `SCR-<CODE>-NN` · Interaction: `INT-<CODE>-NNN`
- Epic: `EP-<CODE>-NN` · Feature: `FT-<CODE>-NN`
- Functional requirement: `FR-<CODE>-NNN` · User story: `US-<CODE>-NNN`
- Business rule: `BR-<CODE>-NN` · Issue/inconsistency: `ISS-<CODE>-NN` · Open question: `OQ-<CODE>-NN`
- Data entity: use the real table name.
Cross-module references: use the other module's code and say "(see module X)" — don't duplicate its features.

## Module codes
| Code | Module |
|---|---|
| PLT | Platform: shell, navigation, personas/demo mode, login, tenant registration, invites, global search, AI copilot, saved views, theme, admin workshop deck |
| CFG | Settings & configuration (settings.tsx, admin.tsx config parts, applicant types, taxonomies, departments, memberships, form library) |
| PLN | Annual plans, endowments, plan adjustments, plan tree/summary, initiatives |
| PRG | Grant programs / opportunities, workflow engines (templates), products, RFP, eligibility, opportunity creation |
| PTL | Partner portal (applicant), partner registration, application submission, license update, AI form assist |
| BEN | Partner organizations (beneficiaries) management, team, groups, entity profile, registration review, beneficiary actions |
| REV | Application review & decision: reviewer list/detail, workflow transitions, AI score, compare, merge, committee minutes, staff edits/partner acceptance, attachments & AI doc check, co-funding, application indicators |
| PRJ | Projects & contracts: projects list/detail, contracts, BOQ/payment schedule, project tree/activities, replan/revisions, start execution, indicators achievement, allocations |
| FIN | Finance & payments: finance page, payment approval chain, disbursement order, transfer/receipt, reports, analytics dashboards |
| TSK | Tasks: my tasks, manual vs derived tasks, focus mode, nav counts, kind filters |

## Output 1 — `/home/user/FundManagementDemo/docs/business-analysis/modules/<NN>-<CODE>.md`
Professional English. Structure exactly:

```
# <CODE> — <Module name>
## 1. Scope & Coverage
Files analyzed (list). Coverage notes and limitations.
## 2. Screen Inventory
Table: Screen ID | Name (EN + Arabic label) | Route / Component | Roles | Purpose | Entry points | Exits / Navigates to
## 3. Screen Details
Per screen: displayed data & fields, tabs/sections, filters, tables & columns, actions/buttons, modals/dialogs, states (loading/empty/error/validation/confirmation) — each tagged with evidence.
## 4. Interaction Inventory
Table: INT ID | Screen | Trigger (control) | System response | Data written | Evidence
## 5. Shared Components & Dependencies
## 6. Business Process Workflows
Status/state machines and process flows (use Mermaid `stateDiagram-v2` or `flowchart` where useful). Include actors and transitions with guards.
## 7. Business Rules
Table: BR ID | Rule | Evidence label + reference
## 8. Data Requirements
Per entity: table, key fields (name, type, required, meaning), relationships, lifecycle/status values.
## 9. Product Structure
Epics → Features list.
## 10. Features
Per feature, all of: Feature ID, Name, Description, Business Objective, Expected Business Value, Primary User Roles, Scope, Out of Scope, Functional Requirements (IDs), Business Rules (IDs), Dependencies, Related Screens, Acceptance Criteria, Open Questions, Assumptions, Priority Recommendation (MoSCoW).
## 11. Functional Requirements
Per FR: ID, Statement ("The system shall …"), Description, Type (Functional / Data / Integration / UI / Security / Reporting / AI), Source/Prototype reference, Related Feature, Related Story, Priority, Dependencies, Acceptance Criteria, Validation Rules, Exceptions & Alternative Flows, Open Questions, Evidence label.
## 12. User Stories
Per story: ID, Parent Epic, Parent Feature, User Role, "As a … I want to … so that …", Preconditions, Main Flow, Alternative Flows, Exception Flows, Business Rules, Acceptance Criteria (Given/When/Then, ≥2), Required Data, Field Validations, Permissions, Error Handling, Dependencies, Definition of Ready checklist (checkbox list; tick only what the evidence supports), Suggested Priority, Open Questions.
## 13. Issues, Inconsistencies & Prototype Gaps
Table: ISS ID | Description | Location | Severity (High/Med/Low) | Recommendation
## 14. Open Questions & Assumptions
```
Be complete but not repetitive: right-size stories (no mega-stories, no one-button stories). Keep FR ↔ story ↔ feature traceability consistent.

## Output 2 — `/home/user/FundManagementDemo/docs/business-analysis/data/<CODE>.json`
Machine-readable records (used to generate the ClickUp import and traceability matrix). Must be valid JSON, matching the markdown exactly:
```json
{
  "module": {"code": "PLN", "name": "Annual Plans & Endowments"},
  "screens": [{"id": "SCR-PLN-01", "name": "", "route": "", "roles": [""]}],
  "epics": [{"id": "EP-PLN-01", "name": "", "description": ""}],
  "features": [{"id": "FT-PLN-01", "epic": "EP-PLN-01", "name": "", "description": "", "roles": [""], "priority": "Must|Should|Could|Won't", "screens": ["SCR-PLN-01"], "requirements": ["FR-PLN-001"], "stories": ["US-PLN-001"], "rules": ["BR-PLN-01"], "dependencies": [""], "acceptance_criteria": [""], "open_questions": [""]}],
  "requirements": [{"id": "FR-PLN-001", "feature": "FT-PLN-01", "stories": ["US-PLN-001"], "statement": "", "type": "", "priority": "", "evidence": "Observed|Inferred|Recommended|To Confirm", "source": "file:line", "acceptance_criteria": [""]}],
  "stories": [{"id": "US-PLN-001", "epic": "EP-PLN-01", "feature": "FT-PLN-01", "role": "", "story": "As a … I want to … so that …", "priority": "", "requirements": ["FR-PLN-001"], "acceptance_criteria": ["Given … When … Then …"], "dependencies": [""], "open_questions": [""]}],
  "rules": [{"id": "BR-PLN-01", "rule": "", "evidence": "", "source": ""}],
  "issues": [{"id": "ISS-PLN-01", "description": "", "severity": "High|Medium|Low", "location": "", "recommendation": ""}],
  "open_questions": [{"id": "OQ-PLN-01", "question": "", "related": [""]}]
}
```
Validate the JSON with `python3 -c "import json;json.load(open(PATH))"` before finishing.

Do not edit anything under /home/user/manih. Do not commit. Finish with a 5-line summary: counts of screens, features, FRs, stories, issues, and any files you could not analyze.
