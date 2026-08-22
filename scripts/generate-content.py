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
import subprocess
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
REPO_COMMIT = "https://github.com/PeteSparrowBTC/bitcoin-backup-framework/commit/"
REPO_FILE_LINKS = {
    "LICENSE": REPO_BLOB + "LICENSE",
}

# Sibling documents that become their own top-level page. On GitHub the sources
# link to each other by filename; on the site those filenames become paths, and
# the depth of the page doing the linking decides how many levels to climb.
SIBLING_PAGES = {
    "NUMBERS.md": "numbers",
    "LANDSCAPE.md": "landscape",
    "ACTIONS.md": "actions",
    "CRYPTOGRAPHY.md": "cryptography",
}


def read(path: str) -> str:
    with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
        return stamp_revision(strip_site_banner(handle.read()))


def build_commit() -> str:
    """The commit this build came from, or "" if it cannot be established.

    GITHUB_SHA is what Actions sets and is the push that triggered the build.
    The git fallback is for a local build, where a dirty tree makes the answer
    approximate; that is acceptable because the stamp exists to date the
    published copy, and the published copy is always built in CI.
    """
    sha = os.environ.get("GITHUB_SHA", "")
    if sha:
        return sha
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return ""


def stamp_revision(markdown: str) -> str:
    """Add the build's commit to the revision note, and drop the markers.

    The sources carry a hand-written date, because a date says when somebody
    last checked the claims and no tool can know that. They cannot carry the
    commit: the hash of a commit is not available to the file inside it. So the
    hash is added here, where it can be read off the build.

    The two answer different questions and both are wanted. The date says how
    stale the *thinking* is; the commit says exactly which text you are reading,
    which matters because this document names files that other repositories
    produce and those names have already changed once.

    Delimited by HTML comments for the same reason the site banner is: editing
    the wording must not be able to stop the substitution silently.
    """
    sha = build_commit()

    def replace(match: re.Match) -> str:
        body = match.group(1).strip()
        if not sha:
            return body + "\n"
        return f"{body} Built from commit [`{sha[:8]}`]({REPO_COMMIT}{sha}).\n"

    return re.sub(
        r"[ \t]*<!--\s*revision:start\s*-->\n(.*?)<!--\s*revision:end\s*-->\n?",
        replace,
        markdown,
        flags=re.S,
    )


def strip_site_banner(markdown: str) -> str:
    """Remove the "read this as a website" block when building the website.

    README.md opens with a banner pointing at the published site, because most
    readers meet the document on GitHub and the split version is easier to use.
    On the site that banner would be telling a reader to go where they already
    are, and linking them to the page they are already on.

    Delimited by HTML comments rather than matched by content, so editing the
    banner's wording cannot silently stop it being stripped.
    """
    return re.sub(
        r"[ \t]*<!--\s*site-banner:start\s*-->.*?<!--\s*site-banner:end\s*-->\n?",
        "",
        markdown,
        flags=re.S,
    )


def write(relpath: str, front: dict, body: str) -> None:
    """Write a page, always typed `docs`.

    The type is what decides whether Hextra keeps the left-hand navigation on
    screen. Hugo derives a page's type from its top-level section, so pages
    under content/framework/ were typed `framework`, and Hextra renders anything
    that is not `docs` with a sidebar hidden below 1280px wide
    (`hx:md:hidden hx:xl:block` rather than `hx:md:sticky`). The tree was in the
    HTML the whole time and simply not displayed.

    Setting it explicitly keeps the URLs descriptive: /framework/8-storing.../
    rather than /docs/8-storing.../, which matters because these paths are meant
    to go in video descriptions and stay put.
    """
    # A marker that reaches the site means its block was never substituted, so
    # the page would carry a revision note with no commit and an HTML comment
    # where the sentence should be. Cheap to check, and the failure is silent
    # otherwise because HTML comments do not render.
    if "revision:start" in body or "site-banner:start" in body:
        sys.exit(f"generate-content: an unsubstituted marker survived into {relpath}")

    path = os.path.join(CONTENT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = ["---", "type: docs"]
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

def short_label(heading: str) -> str:
    """A sidebar-sized version of a section heading.

    The sidebar column is about 16rem. Full headings such as "8. Storing the
    shares: the object, and where it goes" wrap to three lines there and the
    numbers stop lining up, which is most of what makes a tree readable.

    Section headings in this document are written as "N. Subject: elaboration"
    or "N. Subject, elaboration", so the subject is what precedes the first
    colon, comma or bracket. The page keeps its full heading; only the link text
    is shortened.
    """
    label = re.split(r"[:,(]", heading, maxsplit=1)[0].strip()
    # Never shorten to just the number, and do not bother when the saving is
    # small enough that the truncation is only a loss of meaning.
    if len(label) < 12 or len(heading) - len(label) < 6:
        return heading
    return label


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
            "link_title": short_label(heading),
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


def promote_headings(markdown: str) -> str:
    """Lift every heading one level, for a section that has become its own page.

    In README.md a section is "## 8. Storing the shares" with "### The object"
    beneath it. On the site that "##" becomes the page title, so its children
    are a level lower than their position warrants: the page's top-level
    subsections are marked H3 with no H2 above them.

    That is also why the right-hand contents had no indentation. It lists
    headings by level, and a page whose headings are all H3 is a flat list
    however it is rendered. Promoting makes the top-level subsections H2 and
    anything beneath them H3, which is the hierarchy the panel indents.

    Anchors are unaffected: they are derived from the heading text, not its
    level, so every existing cross-reference still lands.
    """
    return re.sub(r"^(#{3,6}) ", lambda m: "#" * (len(m.group(1)) - 1) + " ", markdown, flags=re.M)


def retarget(
    markdown: str,
    from_depth: int,
    current_slug: str = "",
    to_framework: str | None = None,
) -> str:
    """Rewrite the links in a source file for the page it is becoming.

    from_depth is how far the page sits below the site root, which decides how
    many levels a link has to climb: 0 for the front page, 1 for /framework/ or
    a standalone page such as /numbers/, 2 for a framework section page.

    to_framework is the way from this page to the framework's section pages, and
    it is not derivable from depth alone: /framework/ and /landscape/ are both
    one level down, and only one of them has the sections as siblings. It
    defaults to the right answer for pages inside the framework tree.

    Three kinds of link are handled, all of which are written in the sources the
    way GitHub needs them:

      ](#anchor)            a same-document anchor in README.md
      ](README.md#anchor)   another document pointing into README.md
      ](NUMBERS.md#anchor)  a standalone sibling, per SIBLING_PAGES

    Links to an anchor that still lives on this same page are left alone.
    """
    up = "../" * from_depth
    if to_framework is None:
        to_framework = {0: "framework/", 1: "", 2: "../"}[from_depth]

    # Normalise cross-document references into README to the same form as its
    # own internal ones, so a single rule below places both.
    markdown = markdown.replace("](README.md#", "](#")
    markdown = markdown.replace("](README.md)", f"]({up}framework/)")

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
        suffix = f"#{fragment}" if fragment else ""
        return f"]({to_framework}{page}/{suffix})"

    markdown = re.sub(r"\]\(#([a-z0-9-]+)\)", replace, markdown)

    # Links to a standalone sibling, with or without a fragment.
    for source, page in SIBLING_PAGES.items():
        markdown = re.sub(
            re.escape(f"]({source}") + r"(#[a-z0-9-]+)?\)",
            lambda m: f"]({up}{page}/{m.group(1) or ''})",
            markdown,
        )

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
quickstart = retarget(quickstart, from_depth=0)

if "README.md" in quickstart:
    sys.exit("generate-content: an unrewritten README.md link survived on the front page")

write("_index.md", {"title": yaml_quote("Start here"), "weight": 1}, quickstart)

write(
    "framework/_index.md",
    {"title": yaml_quote("The framework"), "weight": 3},
    retarget(preamble, from_depth=1),
)

for section in sections:
    # Breadcrumbs are off by default for this page kind. On a split document
    # they carry the context the single page used to give for free: which of
    # thirteen sections you are in, and that there is a whole above it.
    # They render linkTitle, so they pick up the short labels too.
    front = {
        "title": yaml_quote(section["title"]),
        "weight": section["weight"],
        "breadcrumbs": "true",
    }
    if section["link_title"] != section["title"]:
        front["linkTitle"] = yaml_quote(section["link_title"])
    write(
        f"framework/{section['slug']}.md",
        front,
        promote_headings(retarget(section["body"], from_depth=2, current_slug=section["slug"])),
    )

# The standalone pages, each beside the framework rather than inside it, so
# that any of them can be linked from the quickstart or from the framework's
# sections without living inside either one's folder.
STANDALONE = [
    ("ACTIONS.md", "actions", "Generate, back up, or both", 2),
    ("NUMBERS.md", "numbers", "How the numbers work", 4),
    ("CRYPTOGRAPHY.md", "cryptography", "How the cryptography works", 5),
    ("LANDSCAPE.md", "landscape", "What else is out there", 6),
]

for source, page, title, weight in STANDALONE:
    body = re.sub(r"\A#[^\n]*\n", "", read(source), count=1)
    write(
        f"{page}/_index.md",
        {"title": yaml_quote(title), "weight": weight},
        retarget(body, from_depth=1, to_framework="../framework/"),
    )

print(
    f"generate-content: 1 front page, 1 section index, {len(sections)} framework pages, "
    f"{len(SIBLING_PAGES)} sibling pages, {len(anchor_to_page)} anchors mapped"
)
