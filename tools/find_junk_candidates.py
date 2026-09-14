"""Find frequent leftover words in skeletons that look like junk."""
from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSP = ROOT / "Inspiration"
DATA = ROOT / "tools" / "data"
SCRIPT = Path(__file__).resolve().parent / "strip_worthless_words.py"

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z']*(?:-[A-Za-z]+)*")


def load_worthless() -> set[str]:
    src = SCRIPT.read_text(encoding="utf-8")
    m = re.search(r"WORTHLESS = \{(.+?)\n\}", src, re.S)
    if not m:
        return set()
    return set(ast.literal_eval("{" + m.group(1) + "\n}"))


def load_names() -> set[str]:
    names: set[str] = set()
    for f in ("pokemon_en.json", "moves_en.json", "locations_en.json", "regions_en.json"):
        p = DATA / f
        if not p.exists():
            continue
        for n in json.loads(p.read_text(encoding="utf-8")):
            names.add(n.casefold())
            names.add(n.casefold().replace("é", "e"))
    return names


def main() -> None:
    worthless = load_worthless()
    names = load_names()
    counts: Counter[str] = Counter()

    for sk in INSP.glob("*/Skeletons/*.md"):
        if sk.name.startswith("_"):
            continue
        for line in sk.read_text(encoding="utf-8", errors="ignore").splitlines():
            body = re.sub(r"^#+\s+\d+:\s*Chapter\s+\d+:?\s*", "", line, flags=re.I)
            body = re.sub(r"^#+\s+\d+:\s*", "", body)
            for t in TOKEN_RE.findall(body):
                if t[0].isupper():
                    continue
                k = t.casefold()
                if k in worthless or k in names or len(k) <= 2:
                    continue
                counts[k] += 1

    for w, n in counts.most_common(150):
        print(f"{n:6} {w}")


if __name__ == "__main__":
    main()
