#!/usr/bin/env bash
#
# Proves the external-request check can actually fail.
#
# This exists because the first version of that check only matched quoted
# attribute values, while Hugo's --minify emits them unquoted. It reported
# success on every input, including inputs that were full of external requests.
# A guard nobody has seen fail is not a guard.
#
# Each case below is a way a real page leaks a visit. The check must catch all
# of them, and must stay quiet about ordinary links, which are not leaks.
#
set -euo pipefail

CHECK="$(cd "$(dirname "$0")" && pwd)/check-no-external-requests.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

fails=0

expect() {
  # expect <want: pass|fail> <name> <filename> <content>
  local want="$1" name="$2" file="$3" body="$4"
  local dir="$TMP/case"
  rm -rf "$dir"; mkdir -p "$dir"
  printf '%s' "$body" > "$dir/$file"

  local got=pass
  bash "$CHECK" "$dir" >/dev/null 2>&1 || got=fail

  if [ "$got" = "$want" ]; then
    printf '  ok    %-44s (%s)\n' "$name" "$want"
  else
    printf '  BROKE %-44s (wanted %s, got %s)\n' "$name" "$want" "$got"
    fails=$((fails + 1))
  fi
}

echo "Cases that must FAIL the check:"
expect fail "unquoted script src"        page.html '<script src=https://cdn.example.com/a.js></script>'
expect fail "quoted script src"          page.html '<script src="https://cdn.example.com/a.js"></script>'
expect fail "protocol-relative src"      page.html '<img src=//tracker.example.com/p.gif>'
expect fail "unquoted stylesheet link"   page.html '<link rel=stylesheet href=https://fonts.example.com/c.css>'
expect fail "quoted stylesheet link"     page.html '<link rel="stylesheet" href="https://fonts.example.com/c.css">'
expect fail "preconnect"                 page.html '<link rel=preconnect href=https://fonts.gstatic.com>'
expect fail "icon from another host"     page.html '<link rel=icon href=https://example.com/f.ico>'
expect fail "srcset"                     page.html '<img srcset="https://cdn.example.com/x2.png 2x">'
expect fail "web font in css url()"      s.css    '@font-face{src:url(https://fonts.gstatic.com/s/x.woff2)}'
expect fail "css @import"                s.css    '@import url("https://fonts.googleapis.com/css?family=X");'
expect fail "external later in srcset"   page.html '<img srcset="/a.png 1x, https://cdn.example.com/b.png 2x">'

echo "Cases that must PASS the check:"
expect pass "same-origin assets"         page.html '<link rel=stylesheet href=/css/main.css><script src=/js/app.js></script>'
expect pass "ordinary outbound link"     page.html '<a href=https://github.com/example>source</a>'
expect pass "canonical is metadata"      page.html '<link rel=canonical href=https://example.com/page/>'
expect pass "rss alternate is metadata"  page.html '<link rel=alternate type=application/rss+xml href=https://example.com/f.xml>'
expect pass "relative css url()"         s.css    '@font-face{src:url(/fonts/x.woff2)}'
# The SVG namespace is an identifier, not an address. Hextra inlines icons this
# way, and treating it as a leak is what a substring search does.
expect pass "svg namespace in data uri"  s.css    'background:url("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27%3E")'
expect pass "inline svg xmlns"           page.html '<svg xmlns="http://www.w3.org/2000/svg"><path d=M0/></svg>'

echo
if [ "$fails" -ne 0 ]; then
  echo "$fails case(s) wrong. The check does not do what it claims." >&2
  exit 1
fi
echo "All cases behaved. The check catches leaks and ignores links."
