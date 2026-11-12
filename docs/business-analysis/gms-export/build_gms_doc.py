"""Build a Word document (BRD template) from GMS Delivery Board tasks exported as markdown.

usage: python3 build_gms_doc.py TEMPLATE.docx MD_DIR OUT.docx "Title" MODULE_ID [MODULE_ID ...]
MD_DIR holds <task_id>.md (markdown description) and index.json [{id,name,parent,status,url,assignees}].
"""
import datetime, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "brd"))
import build_brd as B
from docx.shared import RGBColor

tpl, mdd, out, title = sys.argv[1], Path(sys.argv[2]), sys.argv[3], sys.argv[4]
modules = sys.argv[5:]
idx = {t["id"]: t for t in json.load(open(mdd / "index.json", encoding="utf-8"))}
MODNAME = {"z90uw3ye8z": "07 · Project Management", "z90uw3ye92": "10 · Dynamic Form Management"}

def clean(s):
    s = re.sub(r"\\([\[\]_*#<>`|-])", r"\1", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 (\2)", s)
    s = s.replace("<br>", "\n").replace("&nbsp;", " ")
    return s.strip()

def item(l):
    return re.sub(r"^\s*(?:[*\-•]\s+|\d+[.)]\s+)", "", l)

def sections(md):
    head, secs, cur = [], [], None
    for line in md.splitlines():
        m = re.match(r"^#{1,4}\s+(.*)", line)
        if m:
            cur = [clean(m.group(1)), []]; secs.append(cur)
        elif cur is None:
            head.append(line)
        else:
            cur[1].append(line)
    return head, secs

def table(lines):
    rows = [l for l in lines if l.strip().startswith("|")]
    out = []
    for r in rows:
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", r.strip().strip("|"))]
        if all(re.fullmatch(r":?-{2,}:?", c.replace(" ", "")) or not c for c in cells) and any("-" in c for c in cells): continue
        out.append([clean(c) for c in cells])
    return out

def blocks(lines):
    """split body lines into ('p'|'li'|'tbl', payload) blocks"""
    res, buf = [], []
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.strip().startswith("|"):
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"): j += 1
            res.append(("tbl", table(lines[i:j]))); i = j; continue
        if not l.strip() or re.fullmatch(r"\s*(\* \* \*|---+|\*\*\*)\s*", l): i += 1; continue
        if re.match(r"^\s*(?:[*\-•]\s+|\d+[.)]\s+)", l):
            res.append(("li", (len(l) - len(l.lstrip())) // 2, clean(item(l))))
        else:
            res.append(("p", clean(l)))
        i += 1
    return res

def render(doc, lines):
    for b in blocks(lines):
        if b[0] == "tbl":
            rows = b[1]
            if not rows: continue
            n = max(len(r) for r in rows)
            w = [int(10255 / n)] * n
            t = B.new_table(doc, w, header=(rows[0] + [""] * (n - len(rows[0])))[:n])
            for r in rows[1:]: B.add_row(t, (r + [""] * n)[:n])
            B.spacer(doc, 4)
        elif b[0] == "li":
            p = doc.add_paragraph(); B.para_fmt(p, after=60)
            p.paragraph_format.left_indent = B.Pt(18 + 14 * b[1]); p.paragraph_format.first_line_indent = B.Pt(-12)
            B.add_run(p, "•  " + b[2])
        else:
            B.body(doc, b[1])

UC_KEYS = {"title": "Title", "description": "Use Case Description", "actors": "Actors", "preconditions": "Pre-Conditions",
           "trigger": "Trigger", "scenario": "Scenario", "alternative_flows": "Alternative Flow", "postconditions": "Post-Condition"}

def items_of(lines):
    out = []
    for b in blocks(lines):
        if b[0] == "li": out.append(("   " * b[1]) + b[2] if b[1] else b[2])
        elif b[0] == "p": out.append(b[1])
    return out

def story(doc, md):
    head, secs = sections(md)
    render(doc, head)
    d = {k: [] for k in UC_KEYS}
    ids = {"brq": [], "err": []}
    rest = []
    by = {s[0]: s[1] for s in secs}
    known = set()
    for k, lab in UC_KEYS.items():
        for name, lines in secs:
            if name.lower().startswith(lab.lower()):
                d[k] = items_of(lines); known.add(name); break
    for name, lines in secs:
        nl = name.lower()
        if nl.startswith("business requirements") or nl.startswith("errors"):
            key = "brq" if nl.startswith("business") else "err"
            for r in table(lines)[1:]:
                if len(r) >= 2 and r[0]: ids[key].append((r[0], r[1].split("\n")))
            known.add(name)
    if not any(d.values()) and not ids["brq"]:
        for name, lines in secs:
            doc.add_paragraph(name, style="Heading 4" if "Heading 4" in [s.name for s in doc.styles] else "Heading 3"); render(doc, lines)
        return
    for k in ("title", "description", "trigger", "postconditions"):
        d[k] = " ".join(d[k])
    B.uc_table(doc, d, ids)
    B.spacer(doc, 6)
    for name, lines in secs:
        if name in known: continue
        p = doc.add_paragraph(); B.para_fmt(p, after=60); B.add_run(p, name, bold=True, color=B.TEAL_DARK, size=11)
        if name.lower().startswith("fields description"):
            rows = table(lines)
            if rows:
                B.fields_table(doc, [dict(zip(["en", "ar", "type", "editable", "mandatory", "notes"], (r + [""] * 6)[:6])) for r in rows[1:]])
                B.spacer(doc, 6); continue
        render(doc, lines)

doc = B.prepare(tpl)
p = doc.add_paragraph(); B.para_fmt(p, after=60); B.add_run(p, "Manih  |  مانح", bold=True, color=B.TEAL, size=24)
p = doc.add_paragraph(); B.para_fmt(p, after=200); B.bottom_rule(p); B.add_run(p, title, color=B.TEAL_DARK, size=14)
t = B.new_table(doc, [2600, 7655])
kids = lambda pid: sorted([x for x in idx.values() if x["parent"] == pid], key=lambda x: x["name"])
nfeat = sum(len(kids(m)) for m in modules); nst = sum(len(kids(f["id"])) for m in modules for f in kids(m))
for k, v in (("Source", "ClickUp · GMS Delivery Board"), ("Modules", ", ".join(MODNAME.get(m, m) for m in modules)),
             ("Content", f"{nfeat} features and {nst} user stories"), ("Extracted", datetime.date.today().strftime("%d/%m/%Y"))):
    r = B.add_row(t, [k, v], fills={0: B.TEAL}); r.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor.from_string("FFFFFF"); r.cells[0].paragraphs[0].runs[0].bold = True
B.spacer(doc, 6)
p = doc.add_paragraph(); B.para_fmt(p, after=80); B.add_run(p, "Contents", bold=True, color=B.TEAL, size=13)
for m in modules:
    B.add_run(doc.add_paragraph(), MODNAME.get(m, m), bold=True)
    for f in kids(m):
        q = doc.add_paragraph(); q.paragraph_format.left_indent = B.Pt(14); B.para_fmt(q, after=20)
        q.paragraph_format.left_indent = B.Pt(14)
        B.add_run(q, f"{f['name']}  ({len(kids(f['id']))} stories)", size=10)
for mi, m in enumerate(modules, 1):
    doc.add_paragraph(f"{mi}.  Module {MODNAME.get(m, m)}", style="Heading 1").paragraph_format.page_break_before = True
    for fi, f in enumerate(kids(m), 1):
        doc.add_paragraph(f"{mi}.{fi}  {f['name']}", style="Heading 2")
        meta = f"Status: {f['status']}" + (f" · Assignee: {', '.join(f['assignees'])}" if f.get("assignees") else "") + f" · {f['url']}"
        p = doc.add_paragraph(); B.para_fmt(p, after=80); B.add_run(p, meta, size=8.5, color="595959")
        render(doc, (mdd / f"{f['id']}.md").read_text(encoding="utf-8").splitlines())
        for si, s in enumerate(kids(f["id"]), 1):
            doc.add_paragraph(f"{mi}.{fi}.{si}  {s['name']}", style="Heading 3")
            meta = f"Status: {s['status']}" + (f" · Assignee: {', '.join(s['assignees'])}" if s.get("assignees") else "") + f" · {s['url']}"
            p = doc.add_paragraph(); B.para_fmt(p, after=80); B.add_run(p, meta, size=8.5, color="595959")
            story(doc, (mdd / f"{s['id']}.md").read_text(encoding="utf-8"))
doc.save(out)
B.normalize(out)
print("features", nfeat, "stories", nst)
