# Moves Template

How move type files under `Pokemon/Moves` are written.

## File layout

```md
# TypeName

## Physical
### Move Name
Flavor text.
Category | Power N | Accuracy N | PP N | Chance N%
Short battle effect.

## Special
### Move Name
Flavor text.
Category | Power N | Accuracy N | PP N | Chance N%
Short battle effect.

## Status
### Move Name
Flavor text.
Category | Accuracy N | PP N | Chance N%
Short battle effect.

## Other
### Move Name
Flavor text.
PP N
Short battle effect.
```

## Rules

- One file per type. Title is the type name (`# Normal`, `# Fire`, and so on).
- Sections in this order: Physical, Special, Status, Other.
- Other is for Z-Moves, Max Moves, G-Max Moves, and anything without a clear Physical/Special/Status category.
- Within each section, moves are alphabetical by name.
- Each move is a blurb, not a table row.
- Order inside a blurb:
  1. Move name as `###` heading
  2. Flavor text (in-game description)
  3. Stats line
  4. Short battle effect
- Stats line fields, only include what exists: Category, Power, Accuracy, PP, Chance.
- Separate stats with ` | `.
- Write Chance as `Chance 30%`, not a bare number.
- Skip stub flavor text such as "This move can't be used." Prefer a real description from an earlier game when needed.
- No em dashes.
- No tables.

## Example

```md
### Body Slam
The user attacks by dropping onto the target with its full body weight. This may also leave the target with paralysis.
Physical | Power 85 | Accuracy 100 | PP 15 | Chance 30%
May paralyze opponent.
```
