"""Assemble the BA package: ClickUp CSV, traceability matrix, coverage summary, combined markdown.

Run: python3 docs/business-analysis/build.py
Inputs: data/<CODE>.json and modules/NN-<CODE>.md (one per module).
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).parent
ORDER = ["PLT", "CFG", "PLN", "PRG", "PTL", "BEN", "REV", "PRJ", "FIN", "TSK"]
PRIORITY = {"must": "High", "should": "Normal", "could": "Low", "won't": "Low", "wont": "Low"}


def load():
    mods = []
    for code in ORDER:
        path = ROOT / "data" / f"{code}.json"
        if path.exists():
            mods.append(json.loads(path.read_text(encoding="utf-8")))
    return mods


def bullets(items):
    return "\n".join(f"- {i}" for i in items or [] if i)


def clickup_priority(p):
    return PRIORITY.get((p or "").strip().lower(), "Normal")


def write_clickup(mods):
    """One row per Epic / Feature / Story; requirements are folded into their story or feature."""
    rows = []
    for m in mods:
        code, name = m["module"]["code"], m["module"]["name"]
        reqs = {r["id"]: r for r in m.get("requirements", [])}
        for e in m.get("epics", []):
            rows.append([f"[{e['id']}] {e['name']}", "Epic", e["id"], "", code, name, "Normal",
                         f"epic,{code}", e.get("description", ""), ""])
        for f in m.get("features", []):
            desc = f.get("description", "")
            if f.get("requirements"):
                desc += "\n\n**Functional requirements**\n" + bullets(
                    f"{rid}: {reqs[rid]['statement']}" if rid in reqs else rid for rid in f["requirements"])
            if f.get("open_questions"):
                desc += "\n\n**Open questions**\n" + bullets(f["open_questions"])
            rows.append([f"[{f['id']}] {f['name']}", "Feature", f["id"], f.get("epic", ""), code, name,
                         clickup_priority(f.get("priority")), f"feature,{code}," + ",".join(f.get("roles", [])),
                         desc, bullets(f.get("acceptance_criteria"))])
        for s in m.get("stories", []):
            desc = s.get("story", "")
            if s.get("requirements"):
                desc += "\n\n**Requirements**\n" + bullets(
                    f"{rid}: {reqs[rid]['statement']}" if rid in reqs else rid for rid in s["requirements"])
            if s.get("dependencies"):
                desc += "\n\n**Dependencies**\n" + bullets(s["dependencies"])
            if s.get("open_questions"):
                desc += "\n\n**Open questions**\n" + bullets(s["open_questions"])
            rows.append([f"[{s['id']}] {s.get('story', '')[:120]}", "User Story", s["id"], s.get("feature", ""),
                         code, name, clickup_priority(s.get("priority")), f"story,{code},{s.get('role', '')}",
                         desc, bullets(s.get("acceptance_criteria"))])
    with open(ROOT / "clickup-import.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["Task Name", "Task Type", "Custom ID", "Parent ID", "Module Code", "Module",
                    "Priority", "Tags", "Description", "Acceptance Criteria"])
        w.writerows(rows)
    return len(rows)


def write_traceability(mods):
    lines = ["# Traceability Matrix", "",
             "Requirement → Feature → Epic → User Stories → Screens. Generated from `data/*.json` by `build.py`.", ""]
    for m in mods:
        feats = {f["id"]: f for f in m.get("features", [])}
        lines += [f"## {m['module']['code']} — {m['module']['name']}", "",
                  "| Requirement | Evidence | Feature | Epic | User Stories | Screens |", "|---|---|---|---|---|---|"]
        for r in m.get("requirements", []):
            f = feats.get(r.get("feature"), {})
            lines.append(f"| {r['id']} | {r.get('evidence', '')} | {r.get('feature', '')} | {f.get('epic', '')} | "
                         f"{', '.join(r.get('stories', []))} | {', '.join(f.get('screens', []))} |")
        orphans = [s["id"] for s in m.get("stories", []) if not s.get("requirements")]
        if orphans:
            lines += ["", f"Stories without a linked requirement: {', '.join(orphans)}"]
        lines.append("")
    (ROOT / "traceability-matrix.md").write_text("\n".join(lines), encoding="utf-8")


def coverage_table(mods):
    keys = ["screens", "epics", "features", "requirements", "stories", "rules", "issues", "open_questions"]
    head = "| Module | " + " | ".join(k.replace("_", " ").title() for k in keys) + " |"
    lines = [head, "|" + "---|" * (len(keys) + 1)]
    totals = [0] * len(keys)
    for m in mods:
        counts = [len(m.get(k, [])) for k in keys]
        totals = [a + b for a, b in zip(totals, counts)]
        lines.append(f"| {m['module']['code']} — {m['module']['name']} | " + " | ".join(map(str, counts)) + " |")
    lines.append("| **Total** | " + " | ".join(f"**{t}**" for t in totals) + " |")
    return "\n".join(lines)


def write_combined(mods):
    parts = [(ROOT / "README.md").read_text(encoding="utf-8")]
    for extra in ["cross-module.md"]:
        if (ROOT / extra).exists():
            parts.append((ROOT / extra).read_text(encoding="utf-8"))
    parts += [p.read_text(encoding="utf-8") for p in sorted((ROOT / "modules").glob("*.md"))]
    parts.append((ROOT / "traceability-matrix.md").read_text(encoding="utf-8"))
    (ROOT / "Manih-BA-Package.md").write_text("\n\n---\n\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    modules = load()
    n = write_clickup(modules)
    write_traceability(modules)
    (ROOT / "coverage.md").write_text("# Coverage\n\n" + coverage_table(modules) + "\n", encoding="utf-8")
    write_combined(modules)
    print(f"{len(modules)} modules, {n} ClickUp rows")
    print(coverage_table(modules))
