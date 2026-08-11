#!/usr/bin/env python3
"""
Generates the Hugo content tree from the markdown in this repository.

README.md and START-HERE.md stay the single source of every sentence. Nothing
this writes is committed: content/ is gitignored and safe to delete.

The framework is split into one page per numbered section, because a left-hand
navigation tree is the point of splitting it and a single 900-line page has no
tree. The split happens here rather than in the repository so that README.md
keeps working as one document on GitHub, which is where most people will meet
it first.

Splitting moves every in-document anchor onto a different page, so every
"[§8](#8-...)" style link has to be retargeted. That rewriting is done from a
map built out of the headings themselves, and scripts/check-links.py then
verifies against the built HTML that each one landed on a real page and a real
anchor. Hand-maintained cross-references across thirteen pages would rot; these
are derived and checked on every build.

Output tree:

    content/_index.md                     START-HERE.md          ->  /
    content/framework/_index.md           README.md preamble     ->  /framework/
    content/framework/<n>-<slug>.md       README.md section n    ->  /framework/<n>-<slug>/
"""

import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")


def slugify(heading: str) -> str:
    """GitHub's anchor rule, which is also what README.md's own links assume.

    Lowercase, drop everything that is not a letter, digit, space or hyphen,
    then turn spaces into hyphens. Kept identical to the shell one-liner used
    to audit README.md's anchors so both agree on what a link points at.
    """
    s = heading.strip().lower()
    s = re.sub(r"[^a-z0-9 -]", "", s)
    return s.replace(" ", "-")


# Links to files that exist in the repository but have no page on the site.
# On GitHub "[MIT](LICENSE)" resolves; on the site it is a 404, so it is pointed
# at the file where it actually lives. Checked by scripts/check-links.py, which
# is how the LICENSE link was found in the first place.
REPO_BLOB = "https://github.com/PeteSparrowBTC/bitcoin-backup-framework/blob/main/"
REPO_FILE_LINKS = {
    "LICENSE": REPO_BLOB + "LICENSE",
}


def read(path: str) -> str:
    with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
        return handle.read()


def write(relpath: str, front: dict, body: str) -> None:
    path = os.path.join(CONTENT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = ["---"]
    for key, value in front.items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n" + body.strip() + "\n")


def yaml_quote(value: str) -> str:
    """Titles contain colons, which YAML would read as a mapping."""
    return '"' + value.replace('"', '\\"') + '"'


# ---------------------------------------------------------------------------
# Split README.md on its level-2 headings.
# ---------------------------------------------------------------------------

readme = read("README.md")

# Drop the document's H1: Hextra renders the title from front matter and would
# otherwise show it twice.
readme = re.sub(r"\A#[^\n]*\n", "", readme, count=1)

parts = re.split(r"^## ", readme, flags=re.M)
preamble, raw_sections = parts[0], parts[1:]

if not raw_sections:
    sys.exit("generate-content: README.md has no '## ' sections to split on")

sections = []
for index, raw in enumerate(raw_sections, start=1):
    heading, _, body = raw.partition("\n")
    heading = heading.strip()
    slug = slugify(heading)
    sections.append(
        {
            "heading": heading,
            "slug": slug,
            "body": body,
            "weight": index,
            # Titles keep their number so the sidebar reads in document order
            # even where a theme sorts alphabetically.
            "title": heading,
        }
    )

# ---------------------------------------------------------------------------
# Map every anchor in README.md to the page it now lives on.
# ---------------------------------------------------------------------------
# An H2 anchor becomes a page of its own. An H3 anchor (the Phase A..D headings
# inside section 6, for instance) stays a fragment, on its parent's page.

anchor_to_page = {}
for section in sections:
    anchor_to_page[section["slug"]] = (section["slug"], "")
    for sub in re.findall(r"^#{3,6} (.+)$", section["body"], flags=re.M):
        anchor_to_page[slugify(sub)] = (section["slug"], slugify(sub))


def retarget(markdown: str, from_depth: int, current_slug: str = "") -> str:
    """Rewrite "](#anchor)" for a page at the given depth below the site root.

    depth 0 is the front page, 1 is /framework/, 2 is a section page. Links to
    an anchor that now lives on this same page are left alone, because they
    still work and a relative link to oneself is noise.
    """

    def replace(match: re.Match) -> str:
        anchor = match.group(1)
        target = anchor_to_page.get(anchor)
        if target is None:
            # Not a heading in README.md. Left as-is and reported by the link
            # checker if it turns out to point nowhere.
            return match.group(0)
        page, fragment = target
        if page == current_slug:
            return f"](#{fragment or anchor})"
        prefix = {0: "framework/", 1: "", 2: "../"}[from_depth]
        suffix = f"#{fragment}" if fragment else ""
        return f"]({prefix}{page}/{suffix})"

    markdown = re.sub(r"\]\(#([a-z0-9-]+)\)", replace, markdown)

    for repo_path, url in REPO_FILE_LINKS.items():
        markdown = markdown.replace(f"]({repo_path})", f"]({url})")

    return markdown


# ---------------------------------------------------------------------------
# Write it out.
# ---------------------------------------------------------------------------

shutil.rmtree(CONTENT, ignore_errors=True)

# The quickstart is the front page. Its links point at README.md so that they
# work when the file is read on GitHub; here they become site paths.
quickstart = read("START-HERE.md")
quickstart = re.sub(r"\A#[^\n]*\n", "", quickstart, count=1)
quickstart = quickstart.replace("](README.md#", "](#").replace("](README.md)", "](framework/)")
quickstart = retarget(quickstart, from_depth=0)

if "README.md" in quickstart:
    sys.exit("generate-content: an unrewritten README.md link survived on the front page")

write("_index.md", {"title": yaml_quote("Start here"), "weight": 1}, quickstart)

write(
    "framework/_index.md",
    {"title": yaml_quote("The framework"), "weight": 2},
    retarget(preamble, from_depth=1),
)

for section in sections:
    write(
        f"framework/{section['slug']}.md",
        {"title": yaml_quote(section["title"]), "weight": section["weight"]},
        retarget(section["body"], from_depth=2, current_slug=section["slug"]),
    )

print(
    f"generate-content: 1 front page, 1 section index, {len(sections)} framework pages, "
    f"{len(anchor_to_page)} anchors mapped"
)
