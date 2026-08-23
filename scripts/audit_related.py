"""Audit the 'Related templates' block at the foot of every page.

Checks: the section exists; every link resolves; no page links to itself;
no duplicate targets; the link label matches the target page's real title;
the parent category is linked; and no page is orphaned (nothing links to it).
"""
import glob, re, sys, collections

LINK = re.compile(r'\[([^\]]+)\]\((/docs/[^)]*)\)')


def load():
    pages, titles = {}, {}
    for p in glob.glob("content/docs/**/*.md", recursive=True):
        s = open(p).read()
        t = re.search(r'^title: "(.*)"$', s, re.M)
        rel = p[len("content"):-len(".md")]
        if rel.endswith("/_index"):
            rel = rel[: -len("_index")]
        else:
            rel += "/"
        pages[p] = s
        titles[rel] = t.group(1) if t else "?"
    return pages, titles


pages, titles = load()
inbound = collections.Counter()
problems = []

for p in sorted(pages):
    if p.endswith("_index.md"):
        continue
    s = pages[p]
    name = p.split("content/docs/")[1]
    self_url = "/docs/" + p.split("content/docs/")[1][:-3] + "/"
    cat_url = "/docs/" + p.split("content/docs/")[1].split("/")[0] + "/"

    m = re.search(r'\n## Related templates\n(.*?)$', s, re.S)
    if not m:
        problems.append((name, "no 'Related templates' section"))
        continue
    links = LINK.findall(m.group(1))
    if not links:
        problems.append((name, "'Related templates' contains no links"))
        continue

    seen = set()
    for label, url in links:
        u = url if url.endswith("/") else url + "/"
        inbound[u] += 1
        if u not in titles:
            problems.append((name, f"broken target {url}"))
            continue
        if u == self_url:
            problems.append((name, f"links to itself: {url}"))
        if u in seen:
            problems.append((name, f"duplicate target {url}"))
        seen.add(u)
        real = titles[u]
        if label.strip().lower() != real.strip().lower():
            problems.append((name, f'label "{label}" != target title "{real}"  ({url})'))
    if cat_url not in seen:
        problems.append((name, f"does not link its own category {cat_url}"))

# orphans: template pages nothing links to
for p in sorted(pages):
    if p.endswith("_index.md"):
        continue
    u = "/docs/" + p.split("content/docs/")[1][:-3] + "/"
    if inbound[u] == 0:
        problems.append((p.split("content/docs/")[1], "ORPHAN — no other page links here"))

n_pages = len([p for p in pages if not p.endswith("_index.md")])
print(f"{n_pages} template pages checked, {sum(inbound.values())} related-links total")
print(f"problems: {len(problems)}\n")
for name, msg in problems:
    print(f"  {name:<52} {msg}")

if not problems:
    print("  none")
    ib = [(v, k) for k, v in inbound.items() if k in titles and not k.count("/") == 3]
    print(f"\n  inbound links per template page: min {min(v for v,k in ib)}, max {max(v for v,k in ib)}")
