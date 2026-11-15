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

# The start page is also written into index.html's <main> in English, so
# search engines (which read the HTML before any script runs) see the text.
# site.js replaces it with the page from the address as soon as it starts.
import html
import re

INDEX = os.path.join(ROOT, "index.html")
with io.open(INDEX, "r", encoding="utf-8", newline="") as f:
    page = f.read()
tpl = re.search(r'<template id="p-index">(.*?)</template>', page, re.S).group(1)


def fill(m):
    key = m.group(3)
    return m.group(1) + html.escape(data.get(key, key), quote=False) + m.group(4)


# <tag data-i18n="key" ...>old text</tag>  ->  the English string
static = re.sub(r'(<(\w+)[^>]*\bdata-i18n="([^"]+)"[^>]*>)[^<]*(</\2>)', fill, tpl)
start, end = "<!-- prerendered start page -->", "<!-- /prerendered -->"
block = '<main id="view">' + start + static.strip("\r\n") + end + "</main>"
page, n = re.subn(r'<main id="view">.*?</main>', lambda m: block, page, count=1, flags=re.S)
assert n == 1, "no <main id=\"view\"> in index.html"
with io.open(INDEX, "w", encoding="utf-8", newline="") as f:
    f.write(page)
print("prerendered the start page into", INDEX)
