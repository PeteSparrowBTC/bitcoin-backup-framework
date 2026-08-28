#!/usr/bin/env bash
# Mechanical half of the framework review. Reports, never edits.
#
# These are the checks that a reader would eventually notice and that a human
# reviewer reliably misses: box-drawing that stopped lining up after a rename,
# a section reference that is not a link, a filename this repo asserts that the
# tool no longer emits, and work sitting on a branch that main will never see.
#
# The judgement half of the review is in SKILL.md and is not automatable.
#
# Exit code is the number of findings, so CI could gate on it later. Today it
# is run by hand at the start of a review.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

SOURCES="README.md START-HERE.md NUMBERS.md LANDSCAPE.md"
FINDINGS=0

say() { printf '\n== %s\n' "$1"; }
hit() { printf '  %s\n' "$1"; FINDINGS=$((FINDINGS + 1)); }

# --------------------------------------------------------------------------
# 1. ASCII diagrams whose rows stopped matching their borders.
# --------------------------------------------------------------------------
# The §5 architecture diagram broke silently when payload.age was renamed to
# payload.age.gpg.asc: three content rows grew past the box and nothing failed.
# Widths are measured in characters, not bytes, because every border is
# multi-byte box-drawing.
say "diagram alignment"
python - "$SOURCES" <<'PY'
import io, re, sys

bad = 0
for path in sys.argv[1].split():
    try:
        lines = io.open(path, encoding="utf-8").read().split("\n")
    except IOError:
        continue
    fenced, block = False, []
    for n, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            if fenced:
                widths = {len(l) for _, l in block
                          if re.match(r"^\s*[┌└├]", l)}
                if len(widths) == 1:
                    want = widths.pop()
                    for ln, l in block:
                        if re.match(r"^\s*│", l) and len(l) != want:
                            print("%s:%d row %d wide, box %d" % (path, ln, len(l), want))
                            bad += 1
                block = []
            fenced = not fenced
            continue
        if fenced:
            block.append((n, line))
sys.exit(0 if bad == 0 else 1)
PY
[ $? -eq 0 ] || hit "(above) diagram rows do not match their box"

# --------------------------------------------------------------------------
# 2. Section references that are not links.
# --------------------------------------------------------------------------
# CLAUDE.md requires cross-references to be clickable. A bare "(§6.5)" also
# tends to name a section that does not exist, because nothing checks it.
say "unlinked section references"
grep -nE '§[0-9]' $SOURCES | grep -vE '\[§' | while read -r line; do
    printf '  %s\n' "$line"
done
grep -qnE '§[0-9]' $SOURCES 2>/dev/null && \
    grep -nE '§[0-9]' $SOURCES | grep -qvE '\[§' && hit "(above) bare section references"

# --------------------------------------------------------------------------
# 3. Style constructions this repository has ruled out.
# --------------------------------------------------------------------------
say "banned constructions"
for pattern in '—' '–' '“' '”' '’' '\bhonest' '\bpretend' '\bquietly\b'; do
    found=$(grep -nP "$pattern" $SOURCES 2>/dev/null | head -5)
    if [ -n "$found" ]; then
        printf '  pattern %s\n%s\n' "$pattern" "$found"
        hit "banned construction: $pattern"
    fi
done

# --------------------------------------------------------------------------
# 4. Filenames this repo asserts, against what the tool actually emits.
# --------------------------------------------------------------------------
# The framework names the payload file forty times. The tool decides that name
# in one constant. Reading the constant off the sibling's origin/main is the
# only way to know they still agree.
say "payload filename, against the tool"
TOOL_DIR=""
for candidate in ../Seed-Phrase-Storage-SLIP39 ../slip39-backup; do
    [ -d "$candidate/.git" ] && TOOL_DIR="$candidate" && break
done
if [ -z "$TOOL_DIR" ]; then
    hit "no local checkout of the backup tool found beside this repo"
else
    ACTUAL=$(git -C "$TOOL_DIR" show origin/main:Slip39Demo.Core/Bundle/OutputBundleBuilder.cs 2>/dev/null \
             | grep -oE 'PayloadFileName = "[^"]+"' | grep -oE '"[^"]+"' | tr -d '"')
    if [ -z "$ACTUAL" ]; then
        hit "could not read PayloadFileName from $TOOL_DIR (fetch origin first)"
    else
        printf '  tool emits: %s\n' "$ACTUAL"
        # Anchored so the old name is not matched as a prefix of the new one.
        STALE=$(grep -nE "payload\.age[a-z.]*" $SOURCES | grep -v "$ACTUAL" | head -10)
        if [ -n "$STALE" ]; then
            printf '%s\n' "$STALE"
            hit "documents name a payload file the tool does not emit"
        fi
    fi
fi

# --------------------------------------------------------------------------
# 5. Sibling repositories checked out somewhere other than main.
# --------------------------------------------------------------------------
# Reviewing a sibling on a feature branch is how a corrected tool gets reported
# as broken, and how a broken one gets reported as fine.
say "sibling checkouts"
for sib in ../dice-to-seed ../Seed-Phrase-Storage-SLIP39 ../slip39-backup ../seed-generation; do
    [ -d "$sib/.git" ] || continue
    branch=$(git -C "$sib" rev-parse --abbrev-ref HEAD 2>/dev/null)
    behind=$(git -C "$sib" rev-list --count "HEAD..origin/main" 2>/dev/null || echo "?")
    if [ "$branch" != "main" ] || [ "$behind" != "0" ]; then
        hit "$(basename "$sib"): on '$branch', $behind commits behind origin/main"
    else
        printf '  %s: main, current\n' "$(basename "$sib")"
    fi
done

# --------------------------------------------------------------------------
# 6. Commits that exist only on a branch main will never take.
# --------------------------------------------------------------------------
# Five separate fixes have been lost this way, and the sharpest case is the one
# that looks finished: a pull request merges, a further commit lands on the same
# branch minutes later, and nothing ever takes it. Being "ahead of main" cannot
# detect that on its own, because a squash merge leaves every merged branch
# permanently ahead. What separates the two is the commit GitHub actually took:
# a merged branch whose tip is no longer that commit is carrying lost work.
#
# A commit that was later recovered onto a different branch still shows up here,
# because this compares commit identity and recovery rewrites it. Read the
# subjects it prints: if the change is on main under another hash, the branch is
# just old and can be deleted, which is the fix for this whole class anyway.
say "stranded commits"
git fetch origin --quiet 2>/dev/null
if ! command -v gh >/dev/null 2>&1; then
    printf '  skipped: gh not on PATH\n'
else
for ref in $(git for-each-ref --format='%(refname:short)' refs/remotes/origin | grep -v 'origin/main\|origin/HEAD'); do
    ahead=$(git rev-list --count "origin/main..$ref" 2>/dev/null || echo 0)
    [ "$ahead" = "0" ] && continue
    head_name="${ref#origin/}"
    tip=$(git rev-parse "$ref")
    pr=$(gh pr list --state all --head "$head_name" --limit 1 \
         --json number,state,headRefOid --jq '.[] | "\(.number) \(.state) \(.headRefOid)"' 2>/dev/null)
    if [ -z "$pr" ]; then
        hit "$head_name: $ahead commits ahead of main and never had a pull request"
        continue
    fi
    set -- $pr
    num=$1; state=$2; merged_oid=$3
    case "$state" in
        OPEN)   printf '  %s: open in #%s\n' "$head_name" "$num" ;;
        MERGED)
            if [ "$tip" != "$merged_oid" ]; then
                extra=$(git rev-list --count "$merged_oid..$ref")
                hit "$head_name: #$num merged at ${merged_oid:0:8}, branch has $extra commit(s) after it"
                git --no-pager log --oneline "$merged_oid..$ref" | sed 's/^/      /'
            else
                printf '  %s: merged in #%s (squash artifact)\n' "$head_name" "$num"
            fi ;;
        *)      hit "$head_name: #$num is $state and the branch is $ahead ahead" ;;
    esac
done
fi

# --------------------------------------------------------------------------
# 7. The site is the last merged commit, not the working tree.
# --------------------------------------------------------------------------
say "published site"
if command -v gh >/dev/null 2>&1; then
    # --branch main --event push, because the deploy job is gated on
    # github.ref == refs/heads/main. A pull-request run builds and skips
    # deploying, so taking the newest run of any kind names a commit that was
    # never published, and raises a false alarm for as long as a PR is open.
    gh run list --workflow=pages.yml --branch main --event push --limit 1 \
        --json headSha,conclusion,createdAt \
        --jq '.[] | "  last deploy \(.headSha[0:8]) \(.conclusion) \(.createdAt)"' 2>/dev/null
    printf '  origin/main is %s\n' "$(git rev-parse --short origin/main)"
fi

printf '\n%d finding(s). The judgement half of the review is in SKILL.md.\n' "$FINDINGS"
exit "$FINDINGS"
