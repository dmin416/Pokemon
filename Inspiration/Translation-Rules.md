# Translation Rules (Rough)

Rules for turning Chinese Pokémon fanfic (especially Rancher / related sources) into English story drafts. Prefer official English Pokémon terminology. When unsure, check project files before inventing.

**Name/data checks:**
- Species: `Reference/Pokemon/csv/`, `tools/data/pokemon_en.json`, `Pokemon/Potential.md`
- Moves: `Moves/`
- Places: `Reference/Places/` (region files, `Locations.md`)
- Plants / berries: `Reference/Places/Growth-and-Season.md`, `Berry-Plant-Replacements.md`

---

## 1. Pokémon species names

- Always use **official English** species names (`Cyclizar`, `Miltank`, `Koraidon`, `Tinkaton`).
- Do **not** literal-translate Chinese nicknames or descriptive titles into English prose as the species name.
  - Bad: `Big Milk Can`, `Motorcycle Lizard`
  - Good: `Miltank`, `Cyclizar`
- Keep regional forms explicit: `Alolan Vulpix`, `Galarian Rapidash`, `Hisuian Zoroark`.
- Paradox / Treasures of Ruin / Ultra Beasts: use official English (`Flutter Mane`, `Iron Thorns`, `Wo-Chien`).
- If the Chinese is ambiguous, look it up. Do not sound it out into a fake English name.

## 2. Pokémon cries and sounds

Pokémon usually “speak” in **name-based cries**, not translated words.

- Keep cries as vocalizations: `Pika!`, `Koraaa!`, `Mii~`, growls, chirps.
- Do **not** turn mouth-noises into English dialogue:
  - Bad: `"I'm hungry!"` / `"Wow!"` / `"Angry!"` when the source is a cry
  - Good: `"Kora!"` / `"rrrah!"` / `"chirp!"`, with body language carrying meaning
- Chinese onomatopoeia that is clearly a cry should be remapped to **English onomatopoeia**, an **animal-like sound**, or that species’ usual **name-cry**. Do not leave raw Chinese sound syllables in the English draft (`gao`, `wu`, `miu` as pinyin dumps).
  - Bad: `"Gao!"` / `"Ao!"` kept as Chinese-flavored filler
  - Good: `"Kora!"` / `"Koraaa!"` (name-cry), or English sounds like `"rrrah!"`, `"huff!"`, `"chirp!"`, `"bark!"` when a name-cry does not fit
- Real words are OK when the text is clearly telepathy, a psychic / aura relay, Rotom Phone / Pokédex speech, or narration that translates for the reader.
- Be consistent per species across chapters.

## 3. Moves, abilities, items

- Moves: official English (`Thunderbolt`, `Grassy Terrain`, `Dragon Tail`). Not literal calques.
- Abilities: official English (`Intimidate`, `Huge Power`).
- Items / berries / held items: official English (`Oran Berry`, `Master Ball`, `Focus Sash`).
- If a dish or farm product is story-original, translate naturally; if it is a known item, keep the official name.

## 4. Places and regions

- Use official English region and landmark names (`Paldea`, `Porto Marinada`, `Area Zero`, `Casseroya Lake`).
- Do not invent alternate romanizations when an official English name exists.
- Story-only places (ranch nicknames, local shops) can be translated for clarity; keep them consistent once chosen.

## 5. Character names

- Prefer the project’s story names over raw source names when rewriting into Story 1 / Story 2.
  - Example: Rancher source `D` / D → Story 1 **D** when that is the draft convention.
- Keep canon NPC names in official English (`Geeta`, `Nemona`, `Professor Sada`).
- Chinese original nicknames for Pokémon: either keep a stable English nickname or drop to species name; do not reshuffle every chapter.

## 6. System / UI / cooking text

Cooking and “golden finger” panels appear often in these fics.

- Keep grade letters and structure readable: `[Salt-Overloaded Clear Soup Noodles (D-)]`.
- Translate effect text into clear English, not machineese.
- Do not leave raw Chinese UI strings in the draft unless quoting on purpose.
- Stats / buffs: plain English (`raises Speed`, `restores HP`, `grants Sweet Dream`).

## 7. Tone and prose

- Fix MTL artifacts: broken tense, doubled subjects, dictionary-word salad.
- Keep the scene’s register: cozy ranch daily life stays warm and concrete; battle scenes stay clear and physical.
- Food, farm work, and weather can stay specific (your Places / plants refs exist for this).
- Do not “Westernize” every dish name if a simple English dish name works; do not leave opaque pinyin when an English food word is normal.

## 8. Numbers, money, measures

- League currency: keep the story’s term consistent (`league coins` / project convention).
- Metric is fine for ranch realism (kg, ha, °C) unless the draft already uses another system.
- Chapter numbering: prefer the story’s true chronological numbers when summarizing source material.

## 9. When stuck

1. Check whether it is a **species, move, place, item, or cry**.
2. Look up official English in project files.
3. If still unclear, keep a short translator note in draft comments rather than guessing a wrong proper name.
4. Prefer one consistent choice over alternating synonyms.

---

## Quick do / don’t

| Do | Don’t |
|---|---|
| `Miltank used Rollout!` | `Big Milk Can used Super Rolling!` |
| `Cyclizar barked a cheerful "Kora!"` / `"rrrah!"` | `"Gao!"` left as pinyin, or `"I'm so happy!"` |
| `Porto Marinada` | random respelling of the town |
| Official berry / move names | literal Chinese compound calques |
| Clear cooking-panel English | raw MTL UI paste |
