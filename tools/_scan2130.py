from pathlib import Path
import re

t = Path(r"c:\Users\Admin\Desktop\Main\Pokemon\Stories\Story 1\Chapters\21-30.md").read_text(
    encoding="utf-8"
)
print("curly", "\u201c" in t)
short = []
for i, line in enumerate(t.splitlines(), 1):
    s = line.strip()
    if not s or s.startswith("#"):
        continue
    if s.startswith("[") or s.startswith("Cooking") or s.startswith("Rating:") or s.startswith(
        "Additional"
    ):
        continue
    if s.startswith('"') or s.startswith("D:"):
        continue
    words = re.findall(r"[A-Za-z0-9']+", s)
    if len(words) < 4:
        short.append((i, len(words), s))
print("short", len(short))
for x in short:
    print(x)
print("heads", re.findall(r"^# \d+:", t, re.M))
