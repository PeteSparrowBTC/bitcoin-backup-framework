#!/usr/bin/env bash
#
# Builds the published guide from the markdown in this repository.
#
# The point of this script is that no prose is stored twice. README.md and
# START-HERE.md are the only sources; content/ is generated here, is listed in
# .gitignore, and is safe to delete at any time.
#
# Usage:  scripts/build-site.sh            (expects hugo on PATH)
#         HUGO=/path/to/hugo scripts/build-site.sh
#
set -euo pipefail

HUGO="${HUGO:-hugo}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# ---------------------------------------------------------------------------
# 1. Generate content/ from the repository's markdown.
# ---------------------------------------------------------------------------
# Each page is the source file with two changes:
#   - the leading "# Heading" line is dropped, because Hextra renders the title
#     from front matter and would otherwise show it twice;
#   - front matter is prepended.
# Nothing else is rewritten, so what a reader sees on GitHub and what a visitor
# sees on the site are the same words.

rm -rf content
mkdir -p content

emit() {
  # emit <source.md> <destination> <title> <weight>
  local src="$1" dest="$2" title="$3" weight="$4"
  {
    printf -- '---\n'
    printf -- 'title: %s\n' "$title"
    printf -- 'weight: %s\n' "$weight"
    printf -- '---\n\n'
    # Drop the first line when it is the H1, then pass everything else through.
    awk 'NR == 1 && /^# / { next } { print }' "$src"
  } > "$dest"
}

# The framework, as one page. Splitting it into thirteen would invalidate every
# in-document #anchor, which is a deliberate later step and not a build concern.
emit README.md content/framework.md 'The framework' 2

# The quickstart is the front page. Its links point at README.md so they work on
# GitHub; on the site that file is /framework/, so the hrefs are retargeted.
emit START-HERE.md content/_index.md 'Start here' 1
sed -i'' \
  -e 's|](README\.md#|](framework/#|g' \
  -e 's|](README\.md)|](framework/)|g' \
  content/_index.md

# Fail loudly if a README.md link survived the rewrite: a dead link on the front
# page is worse than a failed build.
if grep -n 'README\.md' content/_index.md; then
  echo "build-site: unrewritten README.md link on the front page (above)" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# 2. Build.
# ---------------------------------------------------------------------------
"$HUGO" --minify --gc --cleanDestinationDir

# ---------------------------------------------------------------------------
# 3. The zero-external-requests guard.
# ---------------------------------------------------------------------------
# Checked by a machine, because a theme update is exactly the moment nobody
# remembers to look. The check itself has a test (test-no-external-requests.sh)
# for the same reason: its first version could not fail.

# Invoked through bash rather than executed, so it runs the same way whether or
# not the checkout preserved the executable bit.
bash "$ROOT/scripts/check-no-external-requests.sh" public

echo "build-site: output in public/"
