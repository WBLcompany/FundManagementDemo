# BRD Use-Case Authoring Spec (business-oriented rewrite)

Goal: turn the technical module analyses in `/home/user/FundManagementDemo/docs/business-analysis/modules/NN-CODE.md` into a **business-oriented Business Requirements Document (BRD)** section, structured like the client's template (use-case tables). Audience: business owners, grant managers, finance, executives at the grantor foundation (مؤسسة نورة الملاحي) and the delivery team (WBL). Product: "Manih" (مانح) grant management system.

## Writing style (very important)
- Business language. Describe WHAT the business needs and WHY, not how the code does it.
- NO file names, function names, table names, line numbers, column names, JSON, "RLS", "client-side", "localStorage", route paths, or library names. Say "the system", "the Grants Manager", "the partner organization".
- Business requirements are "The system must …" / "The system should …" statements, testable, one requirement per line.
- Where the prototype has a gap or defect (from §13 Issues), express the **correct target behaviour** as a business requirement (e.g. "Only the assigned approver may approve a payment step"). Do not describe the bug itself inside the use case.
- Where something is a stakeholder decision not settled by the prototype, append " (To be confirmed)" to that requirement.
- Professional English. Keep Arabic only for UI labels and messages taken from the prototype.
- Concise but complete. Prefer 5–10 scenario steps per use case.

## Granularity
Group user stories into **business use cases** (one end-to-end user goal each). Target per module: 5–10 use cases (PLT may have fewer business UCs since much of it is technical — focus on: access & sign-in, role-based workspace, global search, AI assistant, partner self-registration if not in PTL, invitation acceptance). Don't create use cases for purely technical/shared UI components; fold relevant needs into Non-functional/General requirements instead.

## Roles (use these business names)
System Administrator, Grants Manager, Reviewer, Committee Secretary, Project Manager, Finance Officer, CEO / Executive Approver, Partner Organization (Applicant / Partner Delegate). Plus "AI Assistant" and "External AI Evaluation Agent" as system actors where relevant.

## Output — `/home/user/FundManagementDemo/docs/business-analysis/brd/CODE.json`
Valid JSON (validate with python3 json.load). Schema:
```json
{
  "module": "PRG",
  "title": "Grant Opportunities & Programs",           // business name of the module
  "summary": "2–4 sentence business overview of this capability area and its value.",
  "process": {                                         // one business-level process diagram for the module
    "title": "Grant opportunity lifecycle",
    "mermaid": "flowchart LR\n  A[\"Create opportunity\"] --> B[\"Publish\"] ..."   // ALWAYS wrap every node label in double quotes; no semicolons; ≤ 14 nodes; business words only
  },
  "use_cases": [
    {
      "key": "PRG-1",                                  // local key; final UC numbers are assigned later
      "name": "Create and publish a grant opportunity",
      "title": "As a Grants Manager, I want to … so that …",
      "description": "Business description of the use case (2–4 sentences).",
      "actors": ["Grants Manager", "System"],
      "preconditions": ["…"],
      "trigger": "…",
      "scenario": ["step 1", "step 2", "…"],
      "alternative_flows": ["If …, then …"],           // may be empty
      "business_requirements": ["The system must …"],  // 4–12 per use case
      "errors": [{"name": "Short error name", "description": "When it occurs and what the system does"}],  // may be empty
      "postconditions": "…",
      "fields": [                                       // business data captured/shown in this use case (key fields only, may be empty)
        {"en": "Opportunity name", "ar": "اسم الفرصة", "type": "Text|Number|Amount (SAR)|Date|Date-time|List|Yes/No|File|Percentage|Long text", "editable": "Yes|No", "mandatory": "Yes|No", "notes": "restrictions / validation in business terms"}
      ],
      "trace": ["US-PRG-001", "FR-PRG-003"]            // source story / requirement IDs from the module file
    }
  ],
  "messages": [                                        // user-facing messages/notifications observed in the prototype for this module (Arabic text from the code) + recommended ones
    {"type": "Error|Warning|Confirmation|Notification|Information", "en": "English text", "ar": "النص العربي", "use_case": "PRG-1"}
  ],
  "business_rules": [{"rule": "Business-language rule", "use_case": "PRG-1"}],   // the key policy rules (10–25), business wording
  "kpis": [{"name": "…", "definition": "…"}],         // only if the module has reports/dashboards/metrics; else []
  "gaps": [{"area": "…", "gap": "What the prototype does not yet support or does unsafely, in business terms", "impact": "Business impact", "recommendation": "…", "priority": "High|Medium|Low"}],
  "open_questions": ["Business question for stakeholders"]
}
```

## Sources
1. Read the module's markdown file fully (it's long; read in chunks). It is the primary source.
2. For Arabic message texts and Arabic field labels, grep the prototype source in `/home/user/manih/src` (e.g. `toast.error(`, `toast.success(`, `toast(`, `label=`, `placeholder=`) within the files listed in the module's §1 Scope. Use the exact Arabic text; provide an English translation.
3. Do not invent features absent from the prototype unless they are needed as a target requirement to fix a documented gap — then mark the requirement "(Recommended)".

Do not edit anything under /home/user/manih and do not commit. Finish with a 3-line summary (counts of use cases, requirements, messages).
