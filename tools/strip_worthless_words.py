"""
Delete worthless filler words from Inspiration chapter copies.
Keep all other words intact, including unknown names and accented text.
Drop nameless leftover fluff lines.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "Inspiration"
STORIES = [
    "Gym Leader",
    "Jordinio Version",
    "Pokemon Ranger",
    "Psychiatrist",
    "Rancher",
]

WORTHLESS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "than", "that", "this",
    "these", "those", "there", "here", "i", "im", "ive", "id", "ill", "me", "my",
    "mine", "myself", "you", "your", "yours", "yourself", "yourselves", "u", "ur",
    "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
    "itself", "we", "us", "our", "ours", "ourselves", "they", "them", "their",
    "theirs", "themselves", "who", "whom", "whose", "which", "what", "when",
    "where", "why", "how", "is", "am", "are", "was", "were", "be", "been",
    "being", "do", "does", "did", "done", "doing", "have", "has", "had", "having",
    "can", "could", "should", "would", "will", "shall", "may", "might", "must",
    "to", "of", "in", "on", "at", "by", "for", "from", "with", "about", "into",
    "over", "after", "before", "between", "through", "during", "without", "within",
    "along", "across", "against", "among", "around", "up", "down", "out", "off",
    "again", "further", "once", "also", "just", "only", "even", "still", "yet",
    "very", "really", "quite", "rather", "pretty", "so", "too", "as", "like",
    "such", "same", "other", "another", "some", "any", "no", "not", "nor", "none",
    "all", "each", "every", "both", "few", "more", "most", "many", "much", "own",
    "upon", "onto", "per", "via", "vs", "etc", "eg", "ie", "mr", "mrs", "ms", "dr",
    "cant", "wont", "dont", "doesnt", "didnt", "isnt", "arent", "wasnt", "werent",
    "hasnt", "havent", "hadnt", "wouldnt", "couldnt", "shouldnt", "mustnt",
    "thats", "theres", "heres", "whats", "whos", "theyre", "youre", "hes", "shes",
    "lets", "ain", "gonna", "wanna", "gotta", "kinda", "sorta", "dunno", "yeah",
    "yep", "nah", "ok", "okay", "alright", "well", "oh", "ah", "uh", "um", "hmm",
    "hey", "wow", "please", "thanks", "thank", "sorry", "excuse",
    "thing", "things", "something", "anything", "everything", "nothing",
    "someone", "anyone", "everyone", "guy", "guys", "lot", "lots", "bit", "kind",
    "sort", "way", "ways", "stuff", "part", "parts", "side", "sides", "place",
    "places", "area", "areas", "point", "points", "fact", "facts", "idea",
    "ideas", "reason", "reasons", "case", "cases", "sense", "feeling", "feelings",
    "look", "looks", "expression", "expressions", "voice", "voices", "tone",
    "face", "faces", "eyes", "eye", "hand", "hands", "head", "heads", "body",
    "bodies", "hair", "mouth", "smile", "smiles", "gaze", "glance", "glances",
    "time", "times", "moment", "moments", "day", "days", "night", "nights",
    "morning", "evening", "afternoon", "hour", "hours", "minute", "minutes",
    "second", "seconds", "today", "tomorrow", "yesterday", "ago", "now", "soon",
    "later", "earlier", "finally", "eventually", "suddenly", "meanwhile",
    "already", "always", "never", "ever", "often", "sometimes", "usually",
    "almost", "enough", "maybe", "perhaps", "probably", "actually", "basically",
    "literally", "definitely", "certainly", "clearly", "simply", "merely",
    "get", "got", "getting", "gotten", "go", "goes", "went", "gone", "going",
    "come", "comes", "came", "coming", "make", "makes", "made", "making",
    "take", "takes", "took", "taken", "taking", "put", "puts", "putting",
    "see", "sees", "saw", "seen", "seeing", "looked", "looking",
    "know", "knows", "knew", "known", "knowing", "think", "thinks", "thought",
    "thinking", "want", "wants", "wanted", "wanting", "need", "needs", "needed",
    "try", "tries", "tried", "trying", "use", "uses", "used", "using",
    "seem", "seems", "seemed", "seeming", "let", "say", "says", "said", "saying",
    "tell", "tells", "told", "telling", "ask", "asks", "asked", "asking",
    "answer", "answers", "answered", "reply", "replies", "replied",
    "begin", "began", "begun", "beginning", "start", "starts", "started",
    "starting", "continue", "continues", "continued", "become", "becomes",
    "became", "becoming", "feel", "feels", "felt", "find", "finds",
    "found", "finding", "turn", "turns", "turned", "turning", "move", "moves",
    "moved", "moving", "walk", "walks", "walked", "walking", "stand", "stands",
    "stood", "standing", "sit", "sits", "sat", "sitting", "run", "runs", "ran",
    "running", "give", "gives", "gave", "given", "giving", "keep", "keeps",
    "kept", "keeping", "leave", "leaves", "left", "leaving", "bring", "brings",
    "brought", "bringing", "hold", "holds", "held", "holding", "hear", "hears",
    "heard", "hearing", "watch", "watches", "watched", "watching", "notice",
    "notices", "noticed", "realize", "realizes", "realized", "remember",
    "remembers", "remembered", "decide", "decides", "decided", "appear",
    "appears", "appeared", "happen", "happens", "happened", "happenings",
    "mean", "means", "meant", "meaning", "show", "shows", "showed", "shown",
    "showing", "call", "calls", "called", "calling", "help", "helps", "helped",
    "helping", "open", "opens", "opened", "opening", "close", "closes",
    "closed", "closing", "follow", "follows", "followed", "following", "stop",
    "stops", "stopped", "stopping", "wait", "waits", "waited", "waiting",
    "remain", "remains", "remained", "stay", "stays", "stayed", "staying",
    "return", "returns", "returned", "returning", "reach", "reaches", "reached",
    "raise", "raises", "raised", "raising", "nod", "nods", "nodded",
    "smiled", "smiling", "laugh", "laughs", "laughed", "laughing", "sigh",
    "sighed", "sighing", "frown", "frowned", "shake", "shakes", "shook",
    "shaken", "shrug", "shrugged", "glanced", "stare", "stared",
    "staring", "whisper", "whispered", "shout", "shouted", "exclaim",
    "exclaimed", "mutter", "muttered", "murmur", "murmured", "add", "adds",
    "added", "adding", "explain", "explains", "explained", "note", "notes",
    "noted", "remark", "remarked", "declare", "declared", "order", "ordered",
    "able", "unable", "sure", "certain", "true", "false",
    "good", "bad", "great", "big", "small", "little", "long", "short", "high",
    "low", "new", "old", "young", "first", "next", "last", "right", "wrong",
    "best", "better", "worse", "worst", "nice", "fine", "happy", "sad",
    "angry", "calm", "quiet", "loud", "soft", "hard", "easy", "difficult",
    "strong", "weak", "fast", "slow", "hot", "cold", "warm", "cool", "full",
    "empty", "real", "normal", "strange", "weird", "serious", "important",
    "special", "simple", "clear", "possible", "impossible", "different",
    "similar", "whole", "entire", "complete", "ready", "busy", "free", "alone",
    "together", "away", "near", "far", "back", "front", "inside", "outside",
    "handsome", "beautiful", "cute", "lovely", "gentle", "kind",
    "polite", "rude", "proud", "humble", "careful", "careless", "sudden",
    "quick", "deep", "light", "dark", "bright", "heavy", "huge", "tiny",
    "shit", "fuck", "fucking", "fucked", "damn", "goddamn", "hell", "ass",
    "crap", "wtf", "lol", "haha",
    "piss", "pissed", "pissing", "hose", "hoses", "hosed", "hosing",
    "limp", "limps", "limped", "limping", "giggle", "giggles", "giggled",
    "giggling", "gape", "gapes", "gaped", "gaping", "according",
    "chapter", "chapters", "story", "stories", "scene", "scenes", "anyway",
    "however", "therefore", "instead", "besides", "although", "though",
    "because", "since", "unless", "until", "whether", "either", "neither",
    "while", "wherever", "whenever", "whatever", "whoever", "one", "two",
    "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "yes", "indeed", "course",
    "said", "asked", "replied", "answered", "continued", "added", "explained",
    "wondered", "considered", "thought", "felt", "seemed", "appeared",
    "looked", "sounded", "became", "remained",
    # frequent leftover fluff from skeleton scans
    "quickly", "immediately", "slightly", "completely", "instantly", "slowly",
    "gently", "truly", "directly", "softly", "happily", "somewhat", "fully",
    "seriously", "extremely", "nearby", "forward", "toward", "towards", "behind",
    "beside", "under", "above", "straight",
    "chuckled", "blinked", "grinned", "grin", "waved", "patted", "widened",
    "eyebrow", "lips", "breath", "arms", "spoke", "huh",
    "surprised", "stunned", "puzzled", "excitement", "surprise", "worry",
    "wonder", "expected", "understood", "understand", "recalled", "prepared",
    "others", "people", "person", "words", "matter", "chance", "attention",
    "situation", "least", "else", "several", "longer", "current",
    "filled", "stepped", "pulled", "spread", "landed", "gathered", "floated",
    "froze", "fell", "shot", "flew", "burst", "lit", "sent", "set",
    "massive", "large", "wide", "sharp", "glowing", "terrifying",
    "mind", "heart", "sky", "air", "room", "life", "home", "work", "end",
    "top", "past", "years", "name", "sound", "figure", "phone",
    "white", "black", "blue", "green", "red",
    "form", "group", "man", "wings",
}

TOKEN_RE = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ']*(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+)*",
    re.UNICODE,
)
CONTRACTION_RE = re.compile(r"(?:n't|'re|'ve|'ll|'d|'m|'s)$", re.I)
HEADING_RE = re.compile(r"^#{1,3}\s+")
HAS_NAME_RE = re.compile(r"[A-ZÀ-ÖØ-Þ]")


def normalize(tok: str) -> str:
    folded = unicodedata.normalize("NFKD", tok)
    folded = "".join(ch for ch in folded if not unicodedata.combining(ch))
    return CONTRACTION_RE.sub("", folded).lower().replace("'", "")


def strip_line(line: str) -> str:
    kept: list[str] = []
    for tok in TOKEN_RE.findall(line):
        base = normalize(tok)
        if base in WORTHLESS:
            continue
        if len(base) <= 1:
            continue
        kept.append(tok)
    return " ".join(kept)


def flush_chapter(out: list[str], heading: str | None, words: list[str]) -> None:
    if heading is None and not words:
        return
    seen: set[str] = set()
    if heading is not None:
        for w in TOKEN_RE.findall(heading):
            seen.add(w.casefold())
    unique: list[str] = []
    for w in words:
        key = w.casefold()
        if key in seen:
            continue
        seen.add(key)
        unique.append(w)
    body = " ".join(unique).strip()
    if heading is None:
        if body:
            out.append(body)
        return
    out.append(f"{heading} {body}".rstrip() if body else heading)


def main() -> None:
    for story in STORIES:
        src = ROOT / story / "Chapters"
        dst = ROOT / story / "Skeletons"
        dst.mkdir(parents=True, exist_ok=True)
        for path in sorted(src.glob("*.md")):
            out: list[str] = []
            heading: str | None = None
            words: list[str] = []
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                s = line.strip()
                if not s:
                    continue
                if HEADING_RE.match(s):
                    flush_chapter(out, heading, words)
                    heading = s
                    words = []
                    continue
                cleaned = strip_line(s)
                if not cleaned:
                    continue
                if not HAS_NAME_RE.search(cleaned):
                    continue
                if len(cleaned.split()) < 2 and len(cleaned) < 8:
                    continue
                words.extend(cleaned.split())
            flush_chapter(out, heading, words)
            text = "\n".join(out) + "\n"
            out_name = f"{story} {path.name}"
            (dst / out_name).write_text(text, encoding="utf-8")
            # Remove old unprefixed name if present.
            old = dst / path.name
            if old.exists() and old.name != out_name:
                old.unlink()
            pct = 100.0 * len(text.encode()) / max(path.stat().st_size, 1)
            print(f"{story}/{out_name}: {path.stat().st_size} -> {len(text.encode())} ({pct:.1f}%)")


if __name__ == "__main__":
    main()
