"""Compare the section headings of each page's Template block with its Worked
example block. Reports headings present in one but not the other."""
import glob, re, sys

TPL = re.compile(r'## Template\n\n\{\{< doctabs >\}\}\n(.*?)\n\{\{< /doctabs >\}\}', re.S)
EX  = re.compile(r'## Worked example\n\n\{\{< doctabs >\}\}\n(.*?)\n\{\{< /doctabs >\}\}', re.S)
FENCE = re.compile(r'^(`{3,})')


def headings(block):
    """Top-level (##) headings outside nested code fences, normalised."""
    out, in_f, mk = [], False, ""
    for ln in block.split("\n"):
        m = FENCE.match(ln)
        if in_f:
            if m and m.group(1) == mk:
                in_f = False
            continue
        if m:
            in_f, mk = True, m.group(1)
            continue
        h = re.match(r'^##\s+(.*?)\s*$', ln)
        if h:
            t = h.group(1)
            t = re.sub(r'^\d+(\.\d+)*\.?\s*', '', t)         # drop section numbers
            t = re.sub(r'[^a-z0-9 ]', '', t.lower()).strip()
            out.append((t, h.group(1)))
    return out


rows = []
for p in sorted(glob.glob("content/docs/*/[!_]*.md")):
    s = open(p).read()
    t, e = TPL.search(s), EX.search(s)
    if not (t and e):
        continue
    th, eh = headings(t.group(1)), headings(e.group(1))
    tset = {k for k, _ in th}
    eset = {k for k, _ in eh}
    missing = [orig for k, orig in th if k not in eset]
    extra = [orig for k, orig in eh if k not in tset]
    marked = "extract" in e.group(1).split("\n")[0].lower()
    rows.append((p.split("content/docs/")[1], len(th), len(eh), missing, extra, marked))

clean = [r for r in rows if not r[3] and not r[4]]
print(f"{len(clean)}/{len(rows)} pages: template and example headings match exactly\n")
for name, nt, ne, missing, extra, marked in rows:
    if missing or extra:
        tag = "  [marked extract]" if marked else ""
        print(f"{name}  (template {nt} / example {ne}){tag}")
        for m in missing:
            print(f"    - in template, NOT in example : {m}")
        for x in extra:
            print(f"    + in example, NOT in template : {x}")
        print()
