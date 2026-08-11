#!/usr/bin/env bash
#
# Fails if the built site would make a request to any host but its own.
#
# The promise is to the visitor: opening a page must not tell a third party that
# you opened it. So this checks what the *browser fetches on its own* and
# deliberately ignores ordinary links, which a reader chooses to follow.
#
# Fetched automatically, therefore checked:
#   - src= and srcset= on any element
#   - href= on <link> when rel is a fetching kind (stylesheet, icon, preload …)
#   - url(...) and @import in CSS
#
# Not fetched, therefore ignored:
#   - href= on <a>
#   - <link rel=canonical> and rel=alternate, which are metadata
#
# Attribute values are matched quoted OR unquoted, because Hugo's --minify
# removes quotes wherever it can. An earlier version of this check only matched
# quoted values, so it passed on every input and proved nothing. If you change
# the patterns, run scripts/test-no-external-requests.sh, which asserts that a
# planted external reference is still caught.
#
# Usage:  scripts/check-no-external-requests.sh [dir]      (default: public)
#
set -euo pipefail

DIR="${1:-public}"

if [ ! -d "$DIR" ]; then
  echo "check-no-external-requests: no such directory: $DIR" >&2
  exit 2
fi

# A value is external when it names a scheme-ful or protocol-relative host.
# Same-origin references are root-relative or bare paths and match none of these.
EXTERNAL='(https?:)?//'

# rel values that cause the browser to fetch the href without being asked.
FETCHING_REL='stylesheet|icon|apple-touch-icon|manifest|preload|prefetch|preconnect|dns-prefetch|modulepreload'

findings=""

# --- src= and srcset= on anything --------------------------------------------
# srcset holds a comma-separated candidate list, so it is split before matching;
# an external URL in the second candidate leaks exactly as much as in the first.
src_hits="$(
  grep -rhoE '(src|srcset)=("[^"]*"|'"'"'[^'"'"']*'"'"'|[^][:space:]>]+)' "$DIR" \
    --include='*.html' --include='*.js' 2>/dev/null \
  | sed -E 's/^[a-z]+=//; s/^["'"'"']//; s/["'"'"']$//' \
  | tr ',' '\n' \
  | sed -E 's/^[[:space:]]+//; s/[[:space:]].*$//' \
  | grep -E "^$EXTERNAL" || true
)"
[ -n "$src_hits" ] && findings+="$src_hits"$'\n'

# --- <link> tags whose rel makes the href a fetch -----------------------------
link_hits="$(
  grep -rhoE '<link[^>]*>' "$DIR" --include='*.html' 2>/dev/null \
  | grep -EI "rel=(\"|')?($FETCHING_REL)" \
  | grep -oE 'href=("[^"]*"|'"'"'[^'"'"']*'"'"'|[^][:space:]>]+)' \
  | sed -E 's/^href=//; s/^["'"'"']//; s/["'"'"']$//' \
  | grep -E "^$EXTERNAL" || true
)"
[ -n "$link_hits" ] && findings+="$link_hits"$'\n'

# --- CSS: url(...) and @import ------------------------------------------------
# This is where web fonts hide, and a font request leaks the visit as surely as
# an analytics beacon does.
#
# The value is unwrapped and matched from its start rather than searched for a
# host anywhere inside it. Searching found "//www.w3.org/2000/svg" inside an
# inline data: URI, which is an XML namespace and is never requested: a failure
# that would have taught everyone to ignore this check.
css_values="$(
  {
    { grep -rhoE 'url\([^)]*\)' "$DIR" --include='*.css' --include='*.html' 2>/dev/null \
      | sed -E 's/^url\(//; s/\)$//'; } || true
    { grep -rhoE '@import[[:space:]]+("[^"]*"|'"'"'[^'"'"']*'"'"')' "$DIR" \
      --include='*.css' --include='*.html' 2>/dev/null \
      | sed -E 's/^@import[[:space:]]+//'; } || true
  } | sed -E 's/^[[:space:]]*//; s/[[:space:]]*$//; s/^["'"'"']//; s/["'"'"']$//'
)"
css_hits="$(printf '%s' "$css_values" | grep -E "^$EXTERNAL" || true)"
[ -n "$css_hits" ] && findings+="$css_hits"$'\n'

# -----------------------------------------------------------------------------
findings="$(printf '%s' "$findings" | grep -v '^$' | sort -u || true)"

if [ -n "$findings" ]; then
  echo "FAIL: the built site would fetch from other hosts:" >&2
  printf '  %s\n' $findings >&2
  echo >&2
  echo "Every asset must be served from this site. Inline it or vendor it." >&2
  exit 1
fi

echo "OK: no external requests in $DIR"
