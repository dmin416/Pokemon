#!/usr/bin/env python3
"""Convert pipe-table movepool dumps into Pokemon/Movepools/*.md files."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "tools" / "movepool_raw"
OUT = ROOT / "Pokemon" / "Movepools"

TYPE_ORDER = [
    "Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire",
    "Flying", "Ghost", "Grass", "Ground", "Ice", "Normal", "Poison",
    "Psychic", "Rock", "Steel", "Water",
]

HEADERS = {
    "Chansey": """# Chansey (#113)

Normal
Happiny → Chansey → Blissey. See also `Pokemon/Movepools/Blissey.md`.

**Found:** Kanto Safari Zone / rare routes; Happiny in Sinnoh. See `Pokemon/Potential.md`.

## Full Movepool

Sorted by type. Scarlet & Violet level-up, egg, and TM. Chansey learns nothing further in Legends: Z-A.
""",
    "Blissey": """# Blissey (#242)

Normal
Evolves from Chansey via friendship. See also `Pokemon/Movepools/Chansey.md`.

## Full Movepool

Sorted by type. Scarlet & Violet level-up, egg, and TM. Nearly identical to Chansey plus TM-only additions on evolution. Learns nothing further in Legends: Z-A.
""",
    "Calyrex": """# Calyrex (#898)

Psychic / Grass (base). Ice Rider: Psychic / Ice. Shadow Rider: Psychic / Ghost.

Legendary. Fusions with Glastrier and Spectrier add that horse's movepool plus one signature move each (Glacial Lance / Astral Barrage). No egg moves.

**Found:** Galar Crown Tundra. See `Pokemon/Potential.md`.

## Full Movepool

Sorted by type. Form column marks base vs Ice Rider vs Shadow Rider learners.
""",
    "Pawmot": """# Pawmi → Pawmo → Pawmot

Electric → Electric → Electric / Fighting
Pawmi (#921) → Pawmo (#922) → Pawmot (#923)

## Full Movepool

Sorted by type. Scarlet & Violet level-up, evolution, egg, and TM. Learns nothing further in Legends: Z-A.
""",
    "Ralts": """# Ralts (#280)

Psychic / Fairy
Ralts → Kirlia → Gardevoir (Gallade not covered here). Companion: `Pokemon/Ralts.md`.

## Full Movepool

Sorted by type. Scarlet & Violet plus Legends: Z-A (no extra moves beyond SV).
""",
    "Kirlia": """# Kirlia (#281)

Psychic / Fairy
Evolves from Ralts. Nearly identical to Ralts plus three moves on evolution.

## Full Movepool

Sorted by type. Scarlet & Violet plus Legends: Z-A.
""",
    "Gardevoir": """# Gardevoir (#282)

Psychic / Fairy
Evolves from Kirlia. Same learnset for base, Mega, and Dynamax; Mega/Dynamax do not add learnable moves.

Companion: `Pokemon/Ralts.md`.

## Full Movepool

Sorted by type. Scarlet & Violet (level-up, evolution, egg, TM) plus Legends: Z-A.
""",
    "Rotom": """# Rotom (#479)

Electric / Ghost (base). Appliance forms change typing and stats only.

Forms: base, Heat, Wash, Frost, Fan, Mow. Shared movepool except one exclusive signature move per appliance form (see Form line).

## Full Movepool

Sorted by type. Scarlet & Violet plus Legends: Z-A.
""",
    "Heatran": """# Heatran (#485)

Fire / Steel
Legendary. Does not evolve. No egg moves (Undiscovered).

## Full Movepool

Sorted by type. Scarlet & Violet (level-up and TM) plus Legends: Z-A.
""",
    "Giratina": """# Giratina (#487)

Ghost / Dragon
Legendary. Altered and Origin Formes share this movepool. No egg moves. Learns nothing in Legends: Z-A.

## Full Movepool

Sorted by type. Scarlet & Violet level-up and TM.
""",
    "Celesteela": """# Celesteela (#797)

Steel / Flying
Ultra Beast (UB-04 Blaster). Does not evolve. Absorbs air particles to fuel launches from its arms and head.

**Found:** Alola Ultra Wormholes / Ultra Space. See `Pokemon/Potential.md`.

## Full Movepool

Sorted by type. Combined learnset across games for this species.
""",
    "Koraidon": """# Koraidon (#1007)

Fighting / Dragon
Legendary Paradox Pokémon. Known as the Winged King in old Paldean texts. Generation 9 only: no egg moves, no Z-A additions.

**Found:** Paldea Area Zero / Great Crater (Scarlet). See `Pokemon/Potential.md`.

## Full Movepool

Sorted by type. Entire movepool.
""",
    "Dragonite": """# Dratini → Dragonair → Dragonite

Dragon → Dragon → Dragon / Flying
Dratini (#147) → Dragonair (#148) → Dragonite (#149)

**Found:** Kanto Safari / rare water; Johto Dragon's Den. See `Pokemon/Potential.md`.

## Full Movepool

Sorted by type. Scarlet & Violet (level-up, evolution, egg, TM) plus Legends: Z-A level-up/TM.
""",
    "Deoxys": """# Deoxys (#386) - Full Movepool

Psychic
Mythical. Forms: Normal, Attack, Defense, Speed. Does not breed.

Companion to the main species file: `Pokemon/Deoxys.md`.

## Full Movepool

Sorted by type. Master list across all four Formes. The Forme line notes level-up learners when the move is not universal; TM-only moves are marked.
""",
    "Gogoat": """# Skiddo → Gogoat

Grass
Skiddo (#672) → Gogoat (#673)

## Full Movepool

Sorted by type. Scarlet & Violet (level-up, evolution, egg, TM) plus Legends: Z-A level-up/TM.
""",
    "Misdreavus": """## Misdreavus (#200)

Ghost
Learns nothing further in Legends: Z-A. Scarlet & Violet level-up, egg, and TM.
""",
    "Mismagius": """## Mismagius (#429)

Ghost
Evolves from Misdreavus via Dusk Stone. Learns nothing further in Legends: Z-A. Scarlet & Violet level-up, egg, and TM.
""",
    "Flutter Mane": """# Flutter Mane (#987)

Ghost / Fairy
Paradox Pokémon. Ancient relative of Misdreavus. Scarlet exclusive. Generation 9 only: no egg moves, no Z-A additions.

Main file for this line: Flutter Mane first, then Misdreavus and Mismagius movepools below.

**Found:** Paldea Area Zero (Scarlet). See `Pokemon/Potential.md`.

## Flutter Mane

Sorted by type. Entire movepool.
""",
    "Wo-Chien": """# Wo-Chien (#1001)

Dark / Grass
Treasure of Ruin. No egg moves. Learns nothing in Legends: Z-A.

**Found:** Paldea Grasswither Shrine. See `Pokemon/Potential.md`.

## Full Movepool

Sorted by type. Scarlet & Violet level-up and TM.
""",
    "Chien-Pao": """# Chien-Pao (#1002)

Dark / Ice
Treasure of Ruin. No egg moves. Learns nothing in Legends: Z-A.

**Found:** Paldea Icerend Shrine. See `Pokemon/Potential.md`.

## Full Movepool

Sorted by type. Scarlet & Violet level-up and TM.
""",
}


def clean(text: str) -> str:
    text = text.replace("—", "-").replace("–", "-")
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    # Drop Oxford comma before and/or
    text = re.sub(r",(\s+(?:and|or)\b)", r"\1", text)
    # Drop comma before but
    text = re.sub(r",(\s+but\b)", r"\1", text)
    return text.strip()


def fmt_stat(value: str) -> str | None:
    value = value.strip()
    if value in {"", "-", "—"}:
        return None
    value = value.rstrip("%")
    return value


def parse_table(text: str) -> list[dict]:
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 3:
        raise ValueError("Need header, separator, and at least one row")
    headers = [h.strip() for h in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < len(headers):
            cells += [""] * (len(headers) - len(cells))
        row = dict(zip(headers, cells))
        rows.append(row)
    return rows


def format_move(row: dict, move_level: int = 3) -> str:
    name = clean(row["Move"])
    mtype = clean(row["Type"])
    cat = clean(row["Category"])
    power = fmt_stat(row.get("Power", ""))
    acc = fmt_stat(row.get("Accuracy", ""))
    pp = fmt_stat(row.get("PP", ""))
    effect = clean(row.get("Effect", ""))
    what = clean(row.get("What It Is", ""))
    forme = clean(
        row.get("Forme(s) (level-up only)", "")
        or row.get("Forme(s)", "")
        or row.get("Form", "")
    )
    forme_label = "Form" if row.get("Form") else "Forme(s)"

    parts = [f"{mtype} | {cat}"]
    if power is not None:
        parts.append(f"Power {power}")
    if acc is not None:
        if acc not in {"-", "—"}:
            parts.append(f"Accuracy {acc}")
    elif cat != "Status" and row.get("Accuracy", "").strip() in {"-", "—", ""}:
        if power is not None:
            parts.append("Accuracy never misses")
    if pp is not None:
        parts.append(f"PP {pp}")

    h = "#" * move_level
    lines = [f"{h} {name}", " | ".join(parts)]
    if forme:
        lines.append(f"{forme_label}: {forme}")
    if effect:
        lines.append(effect)
    if what:
        lines.append(what)
    return "\n".join(lines) + "\n"


def build_sections(rows: list[dict], type_level: int = 2, move_level: int = 3) -> str:
    by_type: dict[str, list[dict]] = {}
    for row in rows:
        by_type.setdefault(row["Type"], []).append(row)

    type_h = "#" * type_level
    chunks: list[str] = []
    ordered = [t for t in TYPE_ORDER if t in by_type] + [
        t for t in by_type if t not in TYPE_ORDER
    ]
    for t in ordered:
        chunks.append(f"{type_h} {t}")
        chunks.append("")
        for row in by_type[t]:
            chunks.append(format_move(row, move_level=move_level).rstrip())
            chunks.append("")
    return "\n".join(chunks).rstrip() + "\n"


def build_file(name: str, raw_text: str) -> str:
    rows = parse_table(raw_text)
    return HEADERS[name].rstrip() + "\n\n" + build_sections(rows)


def load_table(name: str) -> str:
    path = RAW / f"{name}.md"
    text = path.read_text(encoding="utf-8")
    if "| Move |" not in text:
        raise SystemExit(f"No table in {path}")
    return text[text.index("| Move |") :]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    nested_under = {"Misdreavus", "Mismagius"}

    for path in sorted(RAW.glob("*.md")):
        name = path.stem
        if name in nested_under:
            continue
        if name not in HEADERS:
            print(f"skip unknown: {name}")
            continue
        if name == "Flutter Mane":
            chunks = [HEADERS["Flutter Mane"].rstrip(), ""]
            chunks.append(build_sections(parse_table(load_table("Flutter Mane"))).rstrip())
            chunks.append("")
            for child in ("Misdreavus", "Mismagius"):
                chunks.append(HEADERS[child].rstrip())
                chunks.append("")
                chunks.append(
                    build_sections(
                        parse_table(load_table(child)),
                        type_level=3,
                        move_level=4,
                    ).rstrip()
                )
                chunks.append("")
            out = "\n".join(chunks).rstrip() + "\n"
            dest = OUT / "Flutter Mane.md"
            dest.write_text(out, encoding="utf-8")
            print(f"wrote {dest.relative_to(ROOT)} (combined)")
            for child in ("Misdreavus", "Mismagius"):
                old = OUT / f"{child}.md"
                if old.exists():
                    old.unlink()
                    print(f"removed {old.relative_to(ROOT)}")
            continue

        out = build_file(name, load_table(name))
        dest = OUT / f"{name}.md"
        dest.write_text(out, encoding="utf-8")
        print(f"wrote {dest.relative_to(ROOT)} ({out.count('### ')} moves)")


if __name__ == "__main__":
    main()
