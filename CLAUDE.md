# Working in this repository

The product of this repository is `README.md`, a backup-strategy document. Treat edits to
it as edits to a published document, not to code.

## CRITICAL: main moves only through a pull request

- **Never push to main.** Not `git push origin main`, not a bare `git push` while main
  is checked out, not `git push origin HEAD:main`, and no `--force` variant. Open a pull
  request instead.
- **Never merge a pull request.** Not `gh pr merge`, not the REST API, not the web UI.
  Opening the PR is the agent's job; merging is the human's.
- Pushing feature branches (`git push -u origin <branch>`) is safe and expected.

### The three mechanisms, and what each actually does

| mechanism | what it actually does |
| --- | --- |
| GitHub branch protection on `main` | **The real enforcement.** Server-side, survives a reclone, applies to every client and to the web UI. Requires setup once per repo (below). |
| `.githooks/pre-push` | **Blocks locally**, so a mistake fails before the network round-trip and prints the way out. Opt in per clone: `git config core.hooksPath .githooks`. Bypassable with `--no-verify`, by design. |
| `.claude/settings.json` deny rules | Stops an agent from issuing the common main-targeting push and merge commands, plus the `gh api` verbs that could remove the protection itself. Matching is prefix-based and cannot cover every spelling, so it is a backstop for judgement, not a replacement. |

Deliberately **not** used: an `on: push` workflow that "prevents" direct pushes. Such a
workflow runs after the server has already accepted the push, so it can only report, never
block. A sibling repository had one that failed 39 of 39 runs, including every legitimate
merge, because `github.event.pull_request` is always null on a push event. A permanently red
check is worse than no check. This repository is public, so real server-side enforcement is
available and is used instead.

### Setup: enable branch protection (once per repo)

Requires admin on the repo. Because this repository is public, branch protection is
available on the free plan (private repos would need GitHub Pro or Team).

```bash
gh api -X PUT repos/PeteSparrowBTC/bitcoin-backup-framework/branches/main/protection --input - <<'JSON'
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0,
    "dismiss_stale_reviews": false,
    "require_code_owner_reviews": false
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
```

Why `required_approving_review_count` is 0: a pull request is still required, but a solo
maintainer can merge their own. GitHub does not allow self-approval, so any value above 0
would make every PR unmergeable until a second person exists. Raise it when there is one.

`enforce_admins: true` is what stops the repo owner from pushing to main directly. It does
not prevent merging a PR.

Verify:

```bash
gh api repos/PeteSparrowBTC/bitcoin-backup-framework/branches/main/protection \
  --jq '{pr_required: (.required_pull_request_reviews != null), admins_included: .enforce_admins.enabled}'
```

Equivalent UI path: Settings, Branches, Add branch ruleset, target `main`, tick "Require a
pull request before merging" and "Do not allow bypassing the above settings".

### Setup: enable Pages (once per repo)

The site at `petesparrowbtc.github.io/bitcoin-backup-framework/` is built and
deployed by `.github/workflows/pages.yml`, but the Pages site itself has to
exist before the workflow can deploy into it, and the workflow cannot create it.

```bash
gh api -X POST repos/PeteSparrowBTC/bitcoin-backup-framework/pages -f build_type=workflow
```

Equivalent UI path: Settings, Pages, Source: GitHub Actions.

Why this is not automated: `actions/configure-pages` accepts `enablement: true`,
and it fails. Creating a Pages site that has never existed needs repository
admin, which `GITHUB_TOKEN` does not have at any permission level, including
`pages: write`. Both placements were tried and both returned "Create Pages site
failed: Resource not accessible by integration". Once the site exists the
workflow deploys to it without any further permission, so this is a one-time
cost rather than a recurring one.

### Enable the local hook after cloning

```bash
git config core.hooksPath .githooks
```

Tested behaviour: a push targeting `main` exits 1 with instructions, a feature branch exits
0 silently.

## Writing style

Rules the README follows, and any edit to it must keep:

- **No em dashes.** Use a colon, semicolon, comma, parentheses, or a sentence break.
- **No self-describing rhetoric.** The document states what is true; it does not praise its
  own candour. Avoid "honest", "pretend", and atmospheric adverbs such as "quietly".
- **Jargon is glossed at first use** and the register stays jurisdiction-neutral: the reader
  is a smart non-specialist, not a bitcoin native.
- Section cross-references are clickable anchor links. If you add or retitle a section,
  re-check the anchors.
