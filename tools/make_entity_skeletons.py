"""
Build 5 compiled entity-only skeleton files:
Pokemon names, place names, people. No duplicates per chapter.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from flashtext import KeywordProcessor

ROOT = Path(__file__).resolve().parents[1]
INSP = ROOT / "Inspiration"
DATA = ROOT / "tools" / "data"
OUT = INSP / "Skeletons"

STORIES = [
    "Gym Leader",
    "Jordinio Version",
    "Pokemon Ranger",
    "Psychiatrist",
    "Rancher",
]

HEADING_RE = re.compile(r"^#{1,3}\s+(\d+)")
HEADING_LINE_RE = re.compile(r"^#{1,3}\s+")
TOKEN_RE = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ']*(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+)*",
    re.UNICODE,
)

CAP_JUNK = {
    "The", "A", "An", "And", "But", "Or", "If", "When", "Where", "What", "Why",
    "How", "This", "That", "These", "Those", "There", "Here", "Then", "Than",
    "After", "Before", "Once", "Again", "Still", "Even", "Just", "Only", "Also",
    "Maybe", "Perhaps", "Suddenly", "Finally", "Eventually", "Meanwhile",
    "However", "Therefore", "Instead", "Besides", "Although", "Though",
    "Because", "Since", "Until", "Unless", "While", "During", "Without",
    "With", "From", "Into", "Over", "Under", "About", "Against", "Among",
    "He", "She", "It", "They", "We", "You", "I", "My", "His", "Her", "Their",
    "Our", "Your", "Its", "No", "Yes", "Oh", "Ah", "Well", "So", "As", "At",
    "In", "On", "To", "For", "Of", "By", "Not", "All", "Some", "Any", "Every",
    "One", "Two", "Three", "Four", "Five", "First", "Second", "Next", "Last",
    "Now", "Today", "Tomorrow", "Yesterday", "Later", "Earlier", "Soon",
    "Something", "Someone", "Everyone", "Everything", "Nothing", "Anyone",
    "Chapter", "Pokemon", "Pokémon", "Trainer", "Trainers", "Gym", "Leader",
    "League", "Badge", "Center", "Centre", "Route", "Town", "City", "Island",
    "Professor", "Nurse", "Officer", "Champion", "Elite", "Team", "Type",
    "Using", "According", "Like", "Did", "Does", "Do", "Is", "Are", "Was",
    "Were", "Am", "Be", "Been", "Being", "Has", "Have", "Had", "Can", "Could",
    "Should", "Would", "Will", "Shall", "May", "Might", "Must", "Let",
    "Whatever", "Whenever", "Wherever", "Whoever", "Same", "Most", "Many",
    "Much", "More", "Less", "Such", "Other", "Another", "Each", "Both",
    "Either", "Neither", "Few", "Several", "Own", "Very", "Really", "Quite",
    "Actually", "Basically", "Literally", "Definitely", "Probably", "Certainly",
    "Already", "Always", "Never", "Ever", "Often", "Sometimes", "Usually",
    "Almost", "Enough", "Able", "Unable", "Sure", "True", "False", "Good",
    "Bad", "Great", "Big", "Small", "Little", "Long", "Short", "High", "Low",
    "New", "Old", "Young", "Right", "Wrong", "Best", "Better", "Worse",
    "Nice", "Fine", "Happy", "Sad", "Angry", "Calm", "Quiet", "Loud",
    "Anyway", "It's", "I'm", "I've", "I'd", "I'll", "You're", "They're",
    "There's", "Here's", "What's", "Who's", "That's", "Don't", "Can't",
    "Won't", "Pokémon", "Pokemon",
}

SEED_PEOPLE = {
    "Ash", "Misty", "Brock", "Gary", "Oak", "Giovanni", "Jessie", "James",
    "Lance", "Steven", "Wallace", "Cynthia", "Red", "Blue", "Green", "Yellow",
    "May", "Max", "Dawn", "Iris", "Cilan", "Serena", "Clemont", "Bonnie",
    "Lillie", "Gladion", "Goh", "Chloe", "Dylan", "Johan", "Ilene", "Eileen",
    "Jeanette", "Selene", "Zinnia", "Archer", "Proton", "Petrel", "Ariana",
    "Officer Jenny", "Nurse Joy", "Team Rocket", "Lt. Surge", "Surge",
    "Erika", "Koga", "Sabrina", "Blaine", "Janine", "Falkner", "Bugsy",
    "Whitney", "Morty", "Chuck", "Jasmine", "Pryce", "Clair", "Roxanne",
    "Brawly", "Wattson", "Flannery", "Norman", "Winona", "Tate", "Liza",
    "Juan", "Roark", "Gardenia", "Maylene", "Crasher Wake", "Fantina",
    "Byron", "Candice", "Volkner", "Cheren", "Roxie", "Burgh", "Elesa",
    "Clay", "Skyla", "Brycen", "Drayden", "Marlon", "Viola", "Grant",
    "Korrina", "Ramos", "Clemont", "Valerie", "Olympia", "Wulfric",
    "Hala", "Olivia", "Nanu", "Hapu", "Kiawe", "Mallow", "Lana", "Sophocles",
    "Guzma", "Lusamine", "Faba", "Hop", "Bede", "Marnie", "Leon", "Sonia",
    "Rose", "Oleana", "Nemona", "Arven", "Penny", "Geeta", "Clavell",
    "Sada", "Turo", "Brandon", "Scott", "Anabel", "Lucy", "Spencer",
    "Palmer", "Thorton", "Argenta", "Dahlia", "Darach", "Noland", "Greta",
    "Tucker", "Spenser", "Will", "Karen", "Bruno", "Agatha", "Lorelei",
    "Sidney", "Phoebe", "Glacia", "Drake", "Aaron", "Bertha", "Flint",
    "Lucian", "Shauntal", "Marshal", "Grimsley", "Caitlin", "Malva",
    "Siebold", "Wikstrom", "Drasna", "Alder", "Diantha", "Looker", "Bill",
    "Delia", "Daisy", "Tracey", "Paul", "Trip", "Alain", "Tobias",
    "Maxie", "Archie", "Cyrus", "Ghetsis", "Lysandre", "N", "Hilbert",
    "Hilda", "Nate", "Rosa", "Calem", "Shauna", "Tierno", "Trevor",
    "Elio", "Hau", "Kukui", "Burnet", "Wicke", "Plumeria", "Gladion",
}

EXTRA_PLACES = [
    "Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola", "Galar",
    "Hisui", "Paldea", "Orre", "Fiore", "Almia", "Oblivia", "Indigo Plateau",
    "Victory Road", "Mt. Moon", "Mount Moon", "Mt. Coronet", "Mount Coronet",
    "Cerulean Cave", "Safari Zone", "Power Plant", "Silph Co", "Silph Co.",
    "Pallet Town", "Viridian City", "Pewter City", "Cerulean City",
    "Vermilion City", "Lavender Town", "Celadon City", "Fuchsia City",
    "Saffron City", "Cinnabar Island", "New Bark Town", "Violet City",
    "Azalea Town", "Goldenrod City", "Ecruteak City", "Olivine City",
    "Cianwood City", "Mahogany Town", "Blackthorn City", "Littleroot Town",
    "Petalburg City", "Rustboro City", "Dewford Town", "Slateport City",
    "Mauville City", "Fallarbor Town", "Fortree City", "Lilycove City",
    "Mossdeep City", "Sootopolis City", "Ever Grande City", "Twinleaf Town",
    "Sandgem Town", "Jubilife City", "Oreburgh City", "Eterna City",
    "Hearthome City", "Solaceon Town", "Veilstone City", "Pastoria City",
    "Celestic Town", "Canalave City", "Snowpoint City", "Sunyshore City",
    "Nuvema Town", "Castelia City", "Nimbasa City", "Opelucid City",
    "Lumiose City", "Santalune City", "Shalour City", "Coumarine City",
    "Laverre City", "Anistar City", "Snowbelle City", "Iki Town",
    "Hau'oli City", "Heahea City", "Konikoni City", "Malie City",
    "Postwick", "Motostoke", "Hammerlocke", "Wyndon", "Mesagoza",
    "Area Zero", "Porto Marinada", "Rota", "Rota Gym", "Cerulean Gym",
    "Pewter Gym", "Golden Coast", "Tree of Beginning", "Pokemon Center",
    "Pokémon Center", "Pokemon League", "Pokémon League", "Pokemon School",
    "Pokémon School",
]


def load_list(name: str) -> list[str]:
    path = DATA / name
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def add_variants(kp: KeywordProcessor, term: str) -> None:
    variants = {term}
    if "é" in term or "É" in term:
        variants.add(term.replace("é", "e").replace("É", "E"))
    if "'" in term:
        variants.add(term.replace("'", "’"))
        variants.add(term.replace("'", ""))
    if "’" in term:
        variants.add(term.replace("’", "'"))
        variants.add(term.replace("’", ""))
    if "." in term:
        variants.add(term.replace(".", ""))
        variants.add(term.replace(". ", " "))
    if "-" in term:
        variants.add(term.replace("-", " "))
    for v in variants:
        if len(v) >= 2:
            kp.add_keyword(v, term)


def build_matchers() -> tuple[KeywordProcessor, KeywordProcessor, KeywordProcessor, set[str]]:
    pokemon_kp = KeywordProcessor(case_sensitive=False)
    place_kp = KeywordProcessor(case_sensitive=False)
    people_kp = KeywordProcessor(case_sensitive=False)
    move_names: set[str] = set()

    for name in load_list("pokemon_en.json"):
        add_variants(pokemon_kp, name)
        for prefix in ("Alolan ", "Galarian ", "Hisuian ", "Paldean ", "Mega "):
            add_variants(pokemon_kp, prefix + name)

    for name in load_list("locations_en.json") + load_list("regions_en.json") + EXTRA_PLACES:
        add_variants(place_kp, name)

    for name in SEED_PEOPLE:
        add_variants(people_kp, name)

    for name in load_list("moves_en.json"):
        move_names.add(name.casefold())
        move_names.add(name.casefold().replace("é", "e"))

    return pokemon_kp, place_kp, people_kp, move_names


DIALOGUE_VERBS = (
    "said", "asked", "replied", "muttered", "whispered", "shouted", "exclaimed",
    "answered", "called", "yelled", "snorted", "sighed", "continued", "added",
    "explained", "declared", "ordered", "commanded", "remarked", "noted",
    "thought", "wondered", "smiled", "frowned", "nodded", "laughed",
)
NAME_BEFORE_VERB_RE = re.compile(
    r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\s+(?:"
    + "|".join(DIALOGUE_VERBS)
    + r")\b"
)
POSSESSIVE_RE = re.compile(r"\b([A-Z][a-z]{2,})'s\b")


FALSE_PEOPLE = {
    "Who", "Man", "Woman", "Boy", "Girl", "Ball", "Balls", "Dex", "World",
    "Having", "House", "Ranch", "Tail", "Year", "Years", "Milk", "Tree",
    "Brother", "Sister", "Punch", "Leaf", "Moon", "Sun", "Day", "Night",
    "Time", "Way", "Thing", "Someone", "Everyone", "Anyone", "Something",
    "Nothing", "Everything", "Maybe", "Perhaps", "Suddenly", "Actually",
    "Really", "Probably", "Definitely", "Basically", "Literally", "Anyway",
    "Wait", "Look", "See", "Come", "Go", "Take", "Give", "Let", "Get",
    "Make", "Know", "Think", "Want", "Need", "Feel", "Tell", "Ask", "Try",
    "Use", "Keep", "Leave", "Call", "Put", "Mean", "Seem", "Become",
    "Begin", "Start", "Stop", "Turn", "Move", "Run", "Walk", "Stand",
    "Sit", "Hold", "Bring", "Find", "Hear", "Watch", "Follow", "Help",
    "Show", "Open", "Close", "End", "Side", "Part", "Place", "Area",
    "Point", "Fact", "Idea", "Reason", "Case", "Sense", "Room", "Door",
    "Window", "Hand", "Hands", "Head", "Face", "Eyes", "Eye", "Voice",
    "Body", "Heart", "Mind", "Life", "Death", "Power", "Energy", "Force",
    "Level", "Type", "Move", "Attack", "Battle", "Fight", "Challenge",
    "Gym", "League", "Badge", "Center", "Route", "Town", "City", "Region",
    "School", "Professor", "Nurse", "Officer", "Champion", "Elite", "Team",
    "Trainer", "Trainers", "Leader", "Leaders", "Will", "May", "March",
    "August", "Grant",  # May/Grant/Will are also real characters; prefer seed list only
}


def discover_people(text: str, min_count: int = 4) -> set[str]:
    counts: Counter[str] = Counter()
    for match in NAME_BEFORE_VERB_RE.finditer(text):
        name = match.group(1).strip()
        first = name.split()[0]
        if first in CAP_JUNK or name in CAP_JUNK:
            continue
        if first in FALSE_PEOPLE or name in FALSE_PEOPLE:
            continue
        counts[name] += 1
    return {name for name, n in counts.items() if n >= min_count}


def extract_entities(
    text: str,
    pokemon_kp: KeywordProcessor,
    place_kp: KeywordProcessor,
    people_kp: KeywordProcessor,
) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()

    def keep(label: str) -> None:
        key = label.casefold()
        if key in seen:
            return
        if key in {"pokemon", "pokémon", "pokémon trainer", "pokemon trainer"}:
            return
        seen.add(key)
        found.append(label)

    for name in pokemon_kp.extract_keywords(text):
        keep(name)
    for name in place_kp.extract_keywords(text):
        keep(name)
    for name in people_kp.extract_keywords(text):
        keep(name)
    return found


def chapter_sort_key(path: Path) -> int:
    m = re.search(r"(\d+)-\d+\.md$", path.name)
    return int(m.group(1)) if m else 0


def process_story(
    story: str,
    pokemon_kp: KeywordProcessor,
    place_kp: KeywordProcessor,
    people_kp: KeywordProcessor,
) -> Path:
    src_dir = INSP / story / "Chapters"
    files = sorted(src_dir.glob("*.md"), key=chapter_sort_key)
    combined = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files)

    # Story-specific recurring people, excluding known pokemon/places/moves.
    local_people = KeywordProcessor(case_sensitive=False)
    move_names = {n.casefold() for n in load_list("moves_en.json")}
    for name in discover_people(combined, min_count=6 if story == "Psychiatrist" else 4):
        key = name.casefold()
        if key in move_names:
            continue
        if pokemon_kp.extract_keywords(name) or place_kp.extract_keywords(name):
            continue
        add_variants(local_people, name)
        add_variants(people_kp, name)

    lines_out: list[str] = []

    for path in files:
        heading: str | None = None
        buf: list[str] = []

        def flush() -> None:
            nonlocal heading, buf
            if heading is None:
                buf = []
                return
            chunk = heading + "\n" + "\n".join(buf)
            ents = extract_entities(chunk, pokemon_kp, place_kp, people_kp)
            body = " ".join(ents)
            lines_out.append(f"{heading} {body}".rstrip() if body else heading)
            heading = None
            buf = []

        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip()
            if not s:
                continue
            if HEADING_LINE_RE.match(s):
                flush()
                heading = s
                buf = []
                continue
            if heading is not None:
                buf.append(s)
        flush()

    OUT.mkdir(parents=True, exist_ok=True)
    out_path = OUT / f"{story} Names.md"
    out_path.write_text("\n".join(lines_out) + "\n", encoding="utf-8")
    return out_path


def main() -> None:
    pokemon_kp, place_kp, people_kp, _ = build_matchers()
    for story in STORIES:
        # Fresh people matcher per story so discoveries don't leak forever.
        pokemon_kp, place_kp, people_kp, _ = build_matchers()
        out = process_story(story, pokemon_kp, place_kp, people_kp)
        text = out.read_text(encoding="utf-8")
        print(f"{out.name}: {out.stat().st_size:,} bytes, {text.count(chr(10))} lines")


if __name__ == "__main__":
    main()
