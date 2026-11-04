"""Add 'Appendix A – Lookup Lists' to a BRD-style document and link the UC29/UC30 fields to it.

usage: python3 add_lookups.py IN.docx OUT.docx
"""
import copy, re, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "brd"))
import docx, build_brd as B, lookups as L
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"; q = lambda t: f"{{{W}}}{t}"
tx = lambda e: "".join(t.text or "" for t in e.iter(q("t")))
doc = docx.Document(sys.argv[1]); body = doc.element.body

# drop an earlier appendix so the script can be re-run
kids = list(body)
start = next((i for i, e in enumerate(kids) if e.tag == q("p") and tx(e).strip().startswith("Appendix A")), None)
if start is not None:
    for e in kids[start:]:
        if e.tag != q("sectPr"): body.remove(e)

def set_text(cell, text):
    ps = cell.findall(q("p")); ts = list(ps[0].iter(q("t"))); ts[0].text = text
    for t in ts[1:]: t.text = ""
    for p in ps[1:]: cell.remove(p)

def fields_table(uc):
    kids = list(body)
    i = next((i for i, e in enumerate(kids) if e.tag == q("p") and re.match(rf"(4\.\d+\.\d+|\d+\.)\s+{uc}\b", tx(e).strip())), None)
    if i is None: return None
    return kids[i + 3] if kids[i + 3].tag == q("tbl") else None

acc = "، ".join(L.ACCOUNT_TYPES)
NOTES = {
 ("UC29", "Target account types"): f"Multi-select. Values (Appendix A.1): {acc}",
 ("UC30", "Charitable association groups"): "Multi-select; shows member count. No preset values: each organization defines its own groups (Appendix A.2).",
 ("UC30", "Classification groups"): "Multi-select. Values: classification level 1 (Appendix A.4).",
 ("UC30", "Sub-classification"): "Multi-select; filtered by the selected classification. Values: level 2 (Appendix A.4).",
 ("UC30", "Region"): "Multi-select; 13 regions (Appendix A.5).",
 ("UC30", "Governorate / city"): "Multi-select; filtered by the selected regions (Appendix A.5).",
 ("UC30", "Target account types"): "Multi-select drop-down list displayed inside the «الجمعيات المستهدفة» box. Values: Appendix A.1.",
}
for uc in ("UC29", "UC30"):
    t = fields_table(uc)
    if t is None: continue
    rows = t.findall(q("tr"))
    for tr in rows:
        tcs = tr.findall(q("tc"))
        key = (uc, tx(tcs[0]).strip())
        if key in NOTES: set_text(tcs[5], NOTES[key])
    if uc == "UC30" and not any(tx(tr.findall(q("tc"))[0]).strip() == "Second sub-classification" for tr in rows):
        sub = next(tr for tr in rows if tx(tr.findall(q("tc"))[0]).strip() == "Sub-classification")
        new = copy.deepcopy(sub); c = new.findall(q("tc"))
        set_text(c[0], "Second sub-classification"); set_text(c[1], "التصنيف الفرعي الثاني")
        set_text(c[5], "Multi-select; filtered by the selected sub-classification. Values: level 3 (Appendix A.4).")
        sub.addnext(new)

# ---------------------------------------------------------------- appendix
B.heading(doc, "Appendix A – Lookup Lists", 1)
B.body(doc, "Values used by the selection lists in the opportunity and charitable association use cases (UC29, UC30 and the "
             "partner registration and profile use cases). The lists are maintained as reference data (UC15) and can be extended by the administrator.")
doc.add_paragraph("A.1  Account types (أنواع الحسابات)", style="Heading 2")
t = B.new_table(doc, [700, 9555], header=["#", "Value"])
for k, v in enumerate(L.ACCOUNT_TYPES, 1): B.add_row(t, [str(k), v])
B.spacer(doc)
doc.add_paragraph("A.2  Charitable association groups (مجموعات الجهات الشريكة)", style="Heading 2")
B.body(doc, "No preset values. The list starts empty and each organization adds its own groups.")
doc.add_paragraph("A.3  Supervising authority (جهة الإشراف)", style="Heading 2")
t = B.new_table(doc, [700, 9555], header=["#", "Value"])
for k, v in enumerate(L.SUPERVISING_AUTHORITIES, 1): B.add_row(t, [str(k), v])
B.spacer(doc)
doc.add_paragraph("A.4  Classification (التصنيف النوعي ← التصنيف الفرعي ← التصنيف الفرعي الثاني)", style="Heading 2")
B.body(doc, "Three-level list: classification, sub-classification and second sub-classification. The levels were arranged from the list "
             "provided by the client (To be confirmed against the National Center for Non-Profit Sector classification).")
t = B.new_table(doc, [2900, 3400, 3955], header=["Classification", "Sub-classification", "Second sub-classification"])
for l1, subs in L.CLASSIFICATION.items():
    first1 = True
    for l2, l3s in subs.items():
        first2 = True
        for l3 in l3s:
            r = B.add_row(t, [l1 if first1 else "", l2 if first2 else "", l3])
            if first1: B.set_cell_fill(r.cells[0], "F2F2F2")
            first1 = first2 = False
B.spacer(doc)
doc.add_paragraph("A.5  Region and governorate / city (المنطقة ← المحافظة / المدينة)", style="Heading 2")
t = B.new_table(doc, [2900, 7355], header=["Region", "Governorates / cities"])
for reg, cities in L.REGIONS.items(): B.add_row(t, [reg, "، ".join(cities)])
doc.save(sys.argv[2]); B.normalize(sys.argv[2]); print("appendix added")
