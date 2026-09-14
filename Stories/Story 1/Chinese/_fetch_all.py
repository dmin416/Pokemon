# -*- coding: utf-8 -*-
"""Fetch full Chinese Rancher text into Stories/Story 1/Chinese as groups of 10."""
from __future__ import annotations

import json
import pathlib
import re
import time
import urllib.request

BOOK_ID = 49383
CATALOG_URL = f"https://tw.hjwzw.com/Book/Chapter/{BOOK_ID}"
OUT_DIR = pathlib.Path(r"c:\Users\admin\Desktop\Main\Pokemon\Stories\Story 1\Chinese")
CACHE_DIR = OUT_DIR / "_cache"
PROGRESS = OUT_DIR / "_progress.json"
UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    "Referer": CATALOG_URL,
}
HEADER = """# 《这次不当训练家了》中文原文（粗抓）

来源镜像：黄金屋中文（繁体页面）。作者：骑车的风。仅作 Story 1 对照草稿，非正式校对。

章节范围：第{start}–{end}章（目录序号）。

---
"""


def http_get(url: str, retries: int = 5) -> str:
    last: Exception | None = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read().decode("utf-8", errors="replace")
            if "top.location='/Book/" in data and "<h1>" not in data.lower():
                raise RuntimeError("JS redirect / empty shell")
            return data
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.2 * (i + 1))
    raise RuntimeError(f"GET failed {url}: {last}")


def load_catalog() -> list[tuple[int, str]]:
    raw = http_get(CATALOG_URL)
    pairs = re.findall(rf'href="/Book/Read/{BOOK_ID},(\d+)"[^>]*>([^<]+)</a>', raw)
    out: list[tuple[int, str]] = []
    seen: set[int] = set()
    for cid_s, title in pairs:
        cid = int(cid_s)
        if cid in seen:
            continue
        seen.add(cid)
        out.append((cid, re.sub(r"\s+", " ", title).strip()))
    return out


def extract_body(html: str, fallback_title: str) -> tuple[str, str]:
    title_m = re.search(r"<h1>\s*([^<]+?)\s*</h1>", html, re.I)
    title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else fallback_title

    # Main readable div(s) with text-indent body style
    chunks = re.findall(
        r'<div style="font-size: 20px; line-height: 30px;[^"]*"[^>]*>([\s\S]*?)</div>',
        html,
    )
    if not chunks and title_m:
        # fallback: from h1 to nav
        rest = html[title_m.end() :]
        cut = rest.find("快捷鍵")
        if cut == -1:
            cut = rest.find("上一章")
        chunks = [rest[: cut if cut != -1 else len(rest)]]

    texts: list[str] = []
    for chunk in chunks:
        chunk = re.sub(r"(?is)<script[^>]*>.*?</script>", "", chunk)
        chunk = re.sub(r"(?i)<br\s*/?>", "\n", chunk)
        chunk = re.sub(r"(?i)<p\s*/?>", "\n", chunk)
        chunk = re.sub(r"<[^>]+>", "", chunk)
        chunk = (
            chunk.replace("\xa0", " ")
            .replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
        )
        for line in re.split(r"\r\n?|\n", chunk):
            line = line.strip()
            if not line:
                continue
            if line.startswith("請記住本站域名"):
                continue
            if line.startswith("最新網址"):
                continue
            # drop "書名 第N章 標題" lead-in
            if re.match(r"^這次不當訓練家了\s+", line) and ("章" in line or title in line):
                continue
            texts.append(line)

    # Deduplicate adjacent identical lines
    cleaned: list[str] = []
    for line in texts:
        if cleaned and cleaned[-1] == line:
            continue
        cleaned.append(line)

    body = "\n\n".join(cleaned).strip()
    # If first line duplicates title, keep it (matches existing files)
    return title, body


def fetch_chapter(cid: int, fallback_title: str) -> tuple[str, str]:
    cache = CACHE_DIR / f"{cid}.json"
    if cache.exists():
        obj = json.loads(cache.read_text(encoding="utf-8"))
        if obj.get("body") and len(obj["body"]) >= 40:
            return obj["title"], obj["body"]

    url = f"https://tw.hjwzw.com/Book/Read/{BOOK_ID},{cid}"
    html = http_get(url)
    title, body = extract_body(html, fallback_title)
    if len(body) < 40:
        raise RuntimeError(f"short body cid={cid} title={title!r} len={len(body)}")
    cache.write_text(
        json.dumps({"title": title, "body": body}, ensure_ascii=False),
        encoding="utf-8",
    )
    return title, body


def write_group(entries: list[tuple[int, str, str]], start: int, end: int) -> pathlib.Path:
    parts = [HEADER.format(start=start, end=end), ""]
    for index, title, body in entries:
        parts.append(f"# {index}: {title}")
        body_lines = body.split("\n")
        first = re.sub(r"\s+", " ", body_lines[0]).strip() if body_lines else ""
        if first == title:
            text = body
        else:
            text = title + "\n\n" + body
        text = re.sub(r"\n*最新網址[：:].*$", "", text, flags=re.M).rstrip()
        parts.append(text + "\n")
        parts.append("")
    path = OUT_DIR / f"{start}-{end}.md"
    path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    catalog = load_catalog()
    total = len(catalog)
    print(f"catalog entries: {total}", flush=True)

    cat_path = OUT_DIR / "_catalog.tsv"
    with cat_path.open("w", encoding="utf-8") as f:
        for i, (cid, title) in enumerate(catalog, 1):
            f.write(f"{i}\t{cid}\t{title}\n")

    done = 0
    if PROGRESS.exists():
        try:
            done = int(json.loads(PROGRESS.read_text(encoding="utf-8")).get("done", 0))
        except Exception:  # noqa: BLE001
            done = 0

    fetched: list[tuple[int, str, str]] = []
    for i, (cid, cat_title) in enumerate(catalog, 1):
        title, body = fetch_chapter(cid, cat_title)
        fetched.append((i, title, body))
        if i > done:
            PROGRESS.write_text(json.dumps({"done": i, "total": total}), encoding="utf-8")
            print(f"ok {i}/{total} cid={cid} title={title[:36]} len={len(body)}", flush=True)
            time.sleep(0.25)
        elif i % 50 == 0:
            print(f"cache-hit through {i}/{total}", flush=True)

    for start in range(1, total + 1, 10):
        end = min(start + 9, total)
        path = write_group(fetched[start - 1 : end], start, end)
        print(f"wrote {path.name}", flush=True)

    print("DONE", flush=True)


if __name__ == "__main__":
    main()
