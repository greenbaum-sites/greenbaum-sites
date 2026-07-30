#!/usr/bin/env python3
"""Taxonomy integrity validator.

taxonomy_manifest.json is upstream authority. Any FM/FFN id-name pair in public
HTML, JS, JSON, JSON-LD, SVG text, metadata or tool data that disagrees with the
manifest is a defect in the page.

Detects pairs where the id and name sit in SEPARATE nested elements:
  - sibling divs / spans          <div class="fm-id">FM-01</div><div class="fm-name">X</div>
  - strong / em wrappers          <strong>FM-01</strong> — X
  - JavaScript arrays             "FM-01: X"
  - SVG <text> nodes              <text>FM-01</text><text>X</text>
  - table cells                   <td>FM-01</td><td>X</td>
  - cards / custom components     any tag pair within a short window

Exits nonzero on any mismatch.

    python3 validate_taxonomy.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SITES = ["justingreenbaum.com", "greenbaumlabs.com", "dripractice.com"]
# the canonical taxonomy pages define the taxonomy; they are the rendering of the manifest
SOURCE_DIRS = ("dripractice.com/fm/", "dripractice.com/ffn/")

man = json.loads((ROOT / "taxonomy_manifest.json").read_text())
CANON = {e["id"]: e["canonical_name"] for e in man["entries"]}
PENDING = {a.lower() for e in man["entries"] for a in e.get("pending_alias_review", [])}
APPROVED = {a.lower() for e in man["entries"] for a in e.get("aliases", [])}
ALLNAMES = {n.lower(): i for i, n in CANON.items()}

TAG = r'<[^>]{0,400}?>'
STOP = (r'\s+(?:is|are|was|were|and|in|for|to|the|that|which|when|appears|feeds|triggers|'
        r'adds|showed|at|a|an|its|their|has|have|because|while|but|so|as|on|by|from)\b')


CANON_LOWER = None  # set in main(); longest-first for prefix matching


def clean(name: str, expected: str = None) -> str:
    """Trim a captured name to its most plausible form.

    A canonical name may itself contain a stop word ('Responsibility Compression
    at the Edge'), so try full canonical matches BEFORE splitting on stop words.
    The canonical name for THIS id is tried first, otherwise a longer name
    belonging to a different id can shadow the correct shorter one.
    """
    name = re.sub(r'&[a-z]+;|&#\d+;', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    low = name.lower()
    if expected and low.startswith(expected.lower()):
        return name[:len(expected)]
    if CANON_LOWER:
        for c in CANON_LOWER:                 # longest first
            if low.startswith(c):
                return name[:len(c)]
    name = re.split(STOP, name)[0]
    name = re.sub(r'[\s\-–—:·|,.;)(]+$', '', name.strip())
    return re.sub(r'\s+', ' ', name).strip()


def pairs(text: str, CANON=None):
    """Yield (id, name, how) for every id/name pair, including split-element forms."""
    # 1. same-run: FM-01 · Name   /  FM-01: Name  /  FM-01 — Name
    for m in re.finditer(r'((?:FM|FFN)-\d\d)\s*(?:·|:|&middot;|&mdash;|—|–|-|\||\()\s*'
                         r'([A-Z][A-Za-z\'’ \-]{3,50})', text):
        yield m.group(1), clean(m.group(2), (CANON or {}).get(m.group(1))), "inline"
    # 2. split across tags. The ID must be the ENTIRE content of its own element —
    #    >FM-01</div> — otherwise ordinary prose ("FM-01 detection across 16 entities",
    #    "The FM-04 Moment") is misread as a name mapping. Same for the name.
    #    <th> is excluded: adjacent column headers are labels, not id/name mappings.
    for m in re.finditer(r'>\s*((?:FM|FFN)-\d\d)\s*</(?!th)[^>]+>\s*(?:' + TAG + r'\s*){0,4}'
                         r'>?\s*([A-Z][A-Za-z\'’ \-]{3,50}?)\s*</(?!th)', text):
        yield m.group(1), clean(m.group(2), (CANON or {}).get(m.group(1))), "split-element"
    # 3. reverse order: >Name</y> ... >FM-01</x>
    for m in re.finditer(r'>\s*([A-Z][A-Za-z\'’ \-]{3,50}?)\s*</(?!th)[^>]+>\s*(?:' + TAG + r'\s*){0,2}'
                         r'>\s*((?:FM|FFN)-\d\d)\s*</(?!th)', text):
        yield m.group(2), clean(m.group(1), (CANON or {}).get(m.group(2))), "split-element-reverse"


def main():
    global CANON_LOWER
    CANON_LOWER = sorted((n.lower() for n in CANON.values()), key=len, reverse=True)
    mismatches, unapproved, ok = [], [], 0
    files = []
    for s in SITES:
        for ext in ("html", "js", "json"):
            files += sorted((ROOT / s).rglob(f"*.{ext}"))

    for f in files:
        rel = str(f.relative_to(ROOT))
        if any(rel.startswith(d) for d in SOURCE_DIRS):
            continue
        text = f.read_text(errors="replace")
        seen = set()
        for cid, name, how in pairs(text, CANON):
            if len(name) < 4:
                continue
            key = (cid, name.lower())
            if key in seen:
                continue
            seen.add(key)
            canon = CANON.get(cid)
            if canon is None:
                mismatches.append((rel, cid, name, "ID NOT IN MANIFEST", how))
            elif name.lower() == canon.lower() or name.lower() in APPROVED:
                ok += 1
            elif name.lower() in PENDING:
                unapproved.append((rel, cid, name, how))
            elif name.lower() in ALLNAMES:
                mismatches.append((rel, cid, name,
                                   f"name belongs to {ALLNAMES[name.lower()]}; expected '{canon}'", how))
            else:
                mismatches.append((rel, cid, name, f"expected '{canon}'", how))

    # vertex definition consistency
    VERTEX = {
        "Truth": "Whether narrative aligns with evidence.",
        "Authority": "Whether decision rights match accountability.",
        "Continuity": "Whether decisions, rationale, and learning persist over time.",
    }
    LEGACY = ["earned weight", "authenticity proven over time",
              "through-line that connects", "What IS, not what we wish"]
    vertex_hits = []
    for f in files:
        if f.suffix != ".html":
            continue
        rel = str(f.relative_to(ROOT))
        text = f.read_text(errors="replace")
        for phrase in LEGACY:
            for m in re.finditer(re.escape(phrase), text, re.I):
                ctx = " ".join(text[max(0, m.start() - 120):m.end() + 90].split())
                vertex_hits.append((rel, phrase, ctx[:190]))

    print("== taxonomy validation ==")
    print(f"  manifest        : v{man['schema_version']}  status={man['status']}  "
          f"entries={len(man['entries'])}")
    print(f"  files scanned   : {len(files)}")
    print(f"  correct pairs   : {ok}")
    print(f"  MISMATCHES      : {len(mismatches)}")
    for rel, cid, name, why, how in sorted(set(mismatches)):
        print(f"     [{rel}] {cid} «{name}» ({how})\n        {why}")
    print(f"  UNAPPROVED ALIAS: {len(unapproved)}")
    for rel, cid, name, how in sorted(set(unapproved)):
        print(f"     [{rel}] {cid} «{name}» is in pending_alias_review ({how})")
    print(f"  LEGACY VERTEX   : {len(vertex_hits)}")
    for rel, phrase, ctx in vertex_hits:
        print(f"     [{rel}] «{phrase}»\n        ...{ctx}...")

    missing = [e["id"] for e in man["entries"] if not e["canonical_name"]]
    print(f"  MISSING ENTRIES : {len(missing)} {missing if missing else ''}")

    fail = len(mismatches) + len(unapproved) + len(vertex_hits) + len(missing)
    print(f"\n==== {'PASS' if fail == 0 else 'FAIL'} — {fail} defect(s) ====")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
