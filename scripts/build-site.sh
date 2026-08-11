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
# One page per framework section, so the left-hand navigation has a tree to
# show. README.md itself stays one document, because that is how it is read on
# GitHub. See scripts/generate-content.py for how the cross-references between
# sections are retargeted when they stop being same-page anchors.

PYTHON="${PYTHON:-python3}"
"$PYTHON" scripts/generate-content.py

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

# ---------------------------------------------------------------------------
# 4. Every internal link has to land somewhere.
# ---------------------------------------------------------------------------
# The section cross-references are rewritten mechanically when the framework is
# split, so this checks the result rather than assuming it.
"$PYTHON" scripts/check-links.py public

echo "build-site: output in public/"
