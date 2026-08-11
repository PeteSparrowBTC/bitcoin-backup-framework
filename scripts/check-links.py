#!/usr/bin/env python3
"""
Fails if any internal link in the built site points at a page or anchor that
does not exist.

This exists because splitting the framework into one page per section moved
every in-document anchor onto a different page, and those cross-references are
rewritten mechanically by generate-content.py. A rewrite that silently produces
a dead link is the expected failure of that approach, so it is checked rather
than trusted: a reader following "see §8" to a 404 loses the argument the link
was carrying.

External links are not followed. Whether github.com is up is not this build's
business, and a network call would make the check flaky.

Usage:  scripts/check-links.py [dir]        (default: public)
"""

import os
import re
import sys
from urllib.parse import unquote, urlparse

directory = sys.argv[1] if len(sys.argv) > 1 else "public"

if not os.path.isdir(directory):
    sys.exit(f"check-links: no such directory: {directory}")

# The site is published under a path, not at a domain root, so Hugo writes
# root-relative hrefs as "/bitcoin-backup-framework/...". On disk that prefix is
# not there. Taking it from baseURL keeps the two in step if the site ever moves
# to its own domain, where the prefix becomes empty.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = ""
try:
    with open(os.path.join(ROOT, "hugo.yaml"), encoding="utf-8") as handle:
        found = re.search(r"^baseURL:\s*(\S+)", handle.read(), re.M)
    if found:
        BASE_PATH = urlparse(found.group(1)).path.rstrip("/")
except FileNotFoundError:
    pass

pages = {}  # url path -> set of ids on that page

for base, _, files in os.walk(directory):
    for name in files:
        if not name.endswith(".html"):
            continue
        path = os.path.join(base, name)
        with open(path, encoding="utf-8", errors="replace") as handle:
            html = handle.read()
        url = "/" + os.path.relpath(path, directory).replace(os.sep, "/")
        url = re.sub(r"/index\.html$", "/", url)
        # Ids are emitted unquoted by --minify, so accept both spellings.
        pages[url] = {
            value
            for group in re.findall(r'id=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))', html)
            for value in group
            if value
        }

failures = []

for base, _, files in os.walk(directory):
    for name in files:
        if not name.endswith(".html"):
            continue
        path = os.path.join(base, name)
        with open(path, encoding="utf-8", errors="replace") as handle:
            html = handle.read()
        page_url = "/" + os.path.relpath(path, directory).replace(os.sep, "/")
        page_url = re.sub(r"/index\.html$", "/", page_url)

        for raw in re.findall(r'href=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))', html):
            href = next((h for h in raw if h), "")
            if not href or href.startswith(("http://", "https://", "//", "mailto:", "data:", "javascript:")):
                continue

            target, _, fragment = href.partition("#")
            fragment = unquote(fragment)

            if not target:
                target_url = page_url  # same-page anchor
            elif target.startswith("/"):
                target_url = target
                if BASE_PATH and target_url.startswith(BASE_PATH + "/"):
                    target_url = target_url[len(BASE_PATH):]
                elif BASE_PATH and target_url == BASE_PATH:
                    target_url = "/"
            else:
                target_url = os.path.normpath(os.path.join(os.path.dirname(page_url), target))
                target_url = target_url.replace(os.sep, "/")

            # A directory URL without its trailing slash is the same page: every
            # server redirects one to the other. Normalised rather than reported,
            # because Hugo emits menu pageRefs this way.
            if not target_url.endswith("/") and not os.path.splitext(target_url)[1]:
                target_url += "/"

            # Assets (css, js, png…) are not pages; existence on disk is enough.
            if os.path.splitext(target_url)[1]:
                on_disk = os.path.join(directory, target_url.lstrip("/").replace("/", os.sep))
                if not os.path.exists(on_disk):
                    failures.append(f"{page_url}  ->  {href}   (missing file)")
                continue

            if target_url not in pages:
                failures.append(f"{page_url}  ->  {href}   (no such page: {target_url})")
            elif fragment and fragment not in pages[target_url]:
                failures.append(f"{page_url}  ->  {href}   (no such anchor on {target_url})")

if failures:
    print("FAIL: dead internal links:", file=sys.stderr)
    for failure in sorted(set(failures)):
        print("  " + failure, file=sys.stderr)
    sys.exit(1)

total = sum(len(ids) for ids in pages.values())
print(f"OK: internal links resolve ({len(pages)} pages, {total} anchors)")
