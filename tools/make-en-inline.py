"""Regenerates lang/en-inline.js from lang/en.json.

The site used to fetch lang/en.json after the page had loaded, so the whole
page stayed blank until that request finished (that was the layout shift and
the slow Largest Contentful Paint). en-inline.js carries the same English
strings as a plain script, so the first paint already has the real page.
Run this after editing lang/en.json:  python tools/make-en-inline.py
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "lang", "en.json")
OUT = os.path.join(ROOT, "lang", "en-inline.js")

with io.open(SRC, "r", encoding="utf-8") as f:
    data = json.load(f)

body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
text = (
    "/* Generated from lang/en.json by tools/make-en-inline.py. Do not edit. */\n"
    "window.SHROOMBREW_EN=" + body + ";\n"
)
with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print("wrote", OUT, len(body), "bytes of strings")
