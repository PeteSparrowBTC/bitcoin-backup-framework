---
name: framework-review
description: Use when reviewing this backup framework for defects, drift, or gaps; when README.md, START-HERE.md, NUMBERS.md or LANDSCAPE.md may disagree with the tools they instruct people to run; when a sibling repo (dice-to-seed, slip39-backup, seed-generation) has changed; when checking whether the documented landscape of other projects is still accurate; or when asked what this framework should adopt from other frameworks.
---

# Reviewing the framework

## The core principle

Almost nothing in this document is a claim about itself. It is a claim about
other repositories (what a tool emits, what it is called, what it defaults to),
about other projects (what SmartCustody prescribes, what Superbacked offers),
and about arithmetic. **A review that reads only this repo's markdown will find
it perfectly self-consistent and still be worthless**, because the way this
document goes wrong is that the world moves and the prose does not.

So every pass below ends at a source outside this repository. Read the tool's
code, not the tool's README. Read the project's own documentation, not our
summary of it.

## The five passes

Run them in this order. Each one feeds the next.

### 1. Is the document consistent with itself

The four sources are `README.md` (the reference), `START-HERE.md` (the
quickstart), `NUMBERS.md` (the arithmetic), `LANDSCAPE.md` (the map). They are
edited separately and drift apart.

- Every instruction in the quickstart must exist in the reference. A step that
  lives only in `START-HERE.md` means the reference is incomplete, not that the
  quickstart is ahead.
- Every number quoted anywhere must be derived in `NUMBERS.md`.
- Every property `LANDSCAPE.md` claims this framework has must actually be
  instructed somewhere. Crediting ourselves with a design property we do not
  tell the reader to implement is the easiest error to make here.
- Step ordering must not contradict the rules in §3. Rule 7 in particular:
  anything that distributes artifacts before the drill contradicts §7's own
  list of traps.

Run `bash .claude/skills/framework-review/checks.sh` for the mechanical part
(ASCII box widths, unlinked `§` references, banned style constructions,
filename drift, stranded commits). It reports; it does not fix.

### 2. Do the tools still do what we say they do

This is where real defects live. Check the source, not the README, because a
tool's own README goes stale in the same way ours does.

| Claim in the framework | Where the truth is |
| --- | --- |
| what files the bundle contains, and their names | `Slip39Demo.Core/Bundle/OutputBundleBuilder.cs` |
| what is inside a share zip | `Slip39Demo.Core/Bundle/ShareFolder.cs` |
| what the recovery and verify documents say | `Slip39Demo.Core/Bundle/*Guide.cs`, `PayloadReadme.cs` |
| the default group shape | `Slip39Demo.UI/Pages/Owner.razor` |
| roll counts, entropy tables, the check code | `dice-to-seed/README.md` and `DiceToSeed.Core` |
| what dice do and do not buy | `Slip39Demo.UI/Pages/Owner.razor`, the backup-key panel |

**Check out the right branch first.** A sibling repo left on a feature branch
will show you the tool as it was, and you will confirm a claim that main has
already contradicted. `git log origin/main` in each sibling, always.

**Read the tools' candour and match it.** Where a tool discloses a limit in its
own interface (a generator it still depends on, a duress feature it lacks), the
framework must carry the same disclosure. A document more confident than the
software it drives is the worst failure available here.

### 3. Is the landscape still true

`LANDSCAPE.md` describes projects that release, change licence, and get
abandoned. Confirm before repeating: fetch each project's own page or repo,
check what it says about itself now, and check that every URL resolves. Note
the ones written by this framework's author and keep the disclosure attached.

Look for arrivals as well as changes. The question is not only "is this entry
still right" but "what shipped since the last review that belongs here".

### 4. What do the other frameworks do better

For each comparable project, ask what it prescribes that we do not, and whether
the omission was a decision or an oversight. SmartCustody's adversary list,
Yeti's instructions-with-every-copy, Liana's on-chain timelock, Superbacked's
decoy passphrase, Flaxman's remove-the-single-key argument: each is a specific
thing to answer rather than a general reputation to defer to.

A gap we chose is fine and belongs in §12. A gap we never noticed is a finding.

### 5. Who is not served

Re-read the opening paragraph's description of the reader, then check that the
document actually serves that person. The recurring miss is the reader who
already holds a seed, or coins, and arrives mid-way through a flow written for
someone starting from nothing.

## Producing the review

Write to `reviews/YYYY-MM-DD-framework-review.md`, newest facts first, and open
nothing until the review exists. Each finding carries a file and line reference,
what is wrong, and what makes it wrong (a source, a command, a computation).

Rank by what a reader would lose by following the document as written. A
sequencing defect that costs somebody three trips to a bank beats a broken
ASCII box, even though the box is more obviously wrong.

State plainly which findings you verified and which you inferred. "I read
`OutputBundleBuilder.cs` on origin/main" and "the README implies" are different
strengths of claim and the review is worth less if they read alike.

## Common mistakes

| Mistake | What it costs |
| --- | --- |
| Reading a sibling repo's README instead of its source | You confirm a claim the code contradicts |
| Reviewing a sibling repo on a stale local branch | Same, with more confidence |
| Grepping for a name that is a prefix of the corrected name | `payload.age` matches `payload.age.gpg.asc`, so a fix looks unshipped, or a stale mention hides |
| Treating the quickstart as authoritative | It is the derived document; a gap there is usually a gap in the reference |
| Fixing findings on a branch stacked on an unmerged branch | Work strands when the parent merges first. This has happened five times |
| Declaring the site correct from the markdown | The site is the last merged commit, not the working tree. Check `gh run list` |

## Scope

Review only. Do not edit the four source documents during a review pass: mixing
findings with fixes hides which finding a change answered. Fixes go in a
separate branch off `main`, one PR per theme, after the review is written.

Never push to `main` and never merge a pull request; see `CLAUDE.md`.
