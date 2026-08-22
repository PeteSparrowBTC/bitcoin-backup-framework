# Two actions, and two seeds from two vendors: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the framework into a document for large holdings whose recommended wallet is 2-of-2 keys across two vendors, which names its two supported actions (generating seeds, backing seeds up) and adopts the roll sheet comparison that catches a mis-press.

**Architecture:** Prose changes to four markdown documents plus one new document, in an order that never leaves the published pages contradicting themselves for longer than one commit. The framework keeps its thirteen numbered sections and its single-document form; a new sibling page does the routing. `scripts/generate-content.py` splits the markdown into the Hugo tree, so any new page has to be registered in two places in that script, and every cross-reference is rewritten mechanically and then checked.

**Tech Stack:** Markdown, Python 3 (the content generator and the link checker), Hugo 0.164.0 extended with the Hextra theme as a Go module, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-08-22-two-actions-and-multivendor-scope-design.md`

## Global Constraints

- **No em dashes or en dashes** anywhere in the prose. Use a colon, semicolon, comma, parentheses, or a sentence break.
- **No self-describing rhetoric.** The document states what is true; it does not praise its own candour. Avoid "honest", "pretend", and adverbs such as "quietly".
- **Headings are sentence case.** Jargon is glossed at first use, and the register stays jurisdiction-neutral: the reader is a smart non-specialist.
- **Every threshold carries its noun.** Write "2-of-2 keys" and "2-of-3 cards". A bare "2-of-2" or "2-of-3" is a defect, because both numbers now appear in one document and mean different things.
- **The backup tool's default is 3-of-5 cards**, so the instruction to change it to 2-of-3 cards has to survive every edit.
- **Never push to main and never merge a pull request.** Work on the branch `two-actions-and-multivendor-scope`, which already exists and already carries the spec.
- **Commits end with** `*Collaboration by Claude*` on its own line, in italics.
- **The new page is `ACTIONS.md`**, titled "Generate, back up, or both", served at `/actions/`.
- `content/` is generated and gitignored. Never edit it; never commit it.
- **What this plan specifies, and what it does not.** Each step names the claims an edit has to make, the anchors it has to produce, and the checks it has to pass. It does not write the final sentences. The prose is the deliverable, and storing the same prose twice is what this repository's build exists to prevent, so the executor writes it under the style constraints above.

---

### Task 1: The scope statement

Declare the new subject at the top of the framework, and make section 12 say who the document is not for. Nothing else in the document is consistent with this yet, which is why it goes first: every later task is measured against it.

**Files:**
- Modify: `README.md:24-32` (the opening paragraph), `README.md:49-51` (the one-sentence version), `README.md:1259-1290` (section 12)
- Verify: `scripts/generate-content.py` (run, not modified)

**Interfaces:**
- Consumes: nothing.
- Produces: the phrases every later task reuses verbatim: "large holdings", "2-of-2 keys", "two vendors", "cosigner seed". Section 12 gains a bullet whose lead-in is **Not for modest holdings.**

- [ ] **Step 1: Write the failing check**

There is no test framework for prose here, so the check is a grep that must come back empty. Save it as the task's assertion and run it before editing, to see it fail:

```bash
cd "$(git rev-parse --show-toplevel)"
# The document must say what it is for. Expect a match after this task, none before.
grep -c "large holdings" README.md
```

Expected before editing: `1` (only section 11's existing "For large holdings, graduate the wallet"), which is the sentence this task makes redundant.

- [ ] **Step 2: Rewrite the opening paragraph**

Replace the audience sentence. The current text promises that a password manager and two-factor authentication equip the reader for everything below, which is no longer true when the recommendation is two hardware wallets from different makers plus a recovery-critical descriptor.

Keep: the "trust no one" framing, the link to section 3 and section 10 as an audit of an existing setup, and the note that the principles are tool-agnostic.

Add, in the framework's own register: this is for large holdings; the recommended wallet is 2-of-2 keys, both held by one owner, each on hardware from a different maker; and the job is backing those seeds up, with generating them as a supported action rather than a precondition.

- [ ] **Step 3: Rewrite the one-sentence version**

`README.md:49-51` currently reads "everything digital hangs off a small physical root of trust that only you control". Singular root. With two cosigner keys there are two roots and neither is sufficient alone, which is the stronger sentence and the one to write.

- [ ] **Step 4: Answer the two questions the premise provokes**

A reader who meets "2-of-2 keys" asks two things at once, and the opening answers both or it reads
as a mistake against the usual advice.

Why not 2-of-3 keys: redundancy against a lost or dead device comes from the backup, which holds
both cosigner seeds, so a third key adds no protection and costs a third secret and a wider
spending surface, since any two of three can spend. 2-of-2 keys is the tightest spending rule and
the fewest secrets, and it pairs one to one with two makers.

What a dead device costs: one offline session, not the coins. Take the payload and enough cards to
the retired machine, restore that cosigner seed, load it onto a new device. The machine this
framework retires from the network is exactly the machine a restore needs, so retiring it keeps the
spare part rather than spending one. Do not write a dead device as a loss.

- [ ] **Step 5: Add the exclusion bullet to section 12**

Section 12 lists what the framework deliberately does not do. Add a bullet stating that it is not sized for modest holdings, that a single-key wallet with the same backup is a reasonable thing to want and is not what this document describes, and where such a reader should go instead. Place it before the existing "No claim that solo covers everything" bullet.

Then reconcile the existing "No maximal-security theater" bullet, which cites the Glacier protocol's 93 pages and says the framework spends its complexity budget only where a named failure mode demands it. It now has to name the failure mode that a second vendor buys, which is a maker's defect satisfying the quorum alone.

- [ ] **Step 6: Run the generator**

```bash
python scripts/generate-content.py
```

Expected: exits 0 and prints a line ending `15 framework pages, 2 sibling pages, 33 anchors mapped`. The counts must not change in this task; a change means a heading was altered accidentally.

- [ ] **Step 7: Check the constraints**

```bash
# No em or en dashes.
grep -n '[—–]' README.md; echo "exit: $?"
# Every threshold carries its noun.
grep -nE '2-of-2' README.md | grep -vE '2-of-2 keys'; echo "exit: $?"
```

Expected: no output from either grep, and `exit: 1` from each, which is what grep returns when it matches nothing.

- [ ] **Step 8: Commit**

```bash
git add README.md
git commit -m "Say the framework is for large holdings, and who it is not for" \
  -m "The opening promised that a password manager and two-factor authentication equipped the reader for everything below. Two makers and a recovery-critical descriptor is a different reader, and section 12 now says so rather than leaving them to follow a plan sized for somebody else." \
  -m "*Collaboration by Claude*"
```

---

### Task 2: Rule 0, and what two vendors buys

Section 2 is the precondition section and it is written for one seed. This task makes it two, and corrects the reason vendor diversity matters once the reader supplies their own entropy.

**Files:**
- Modify: `README.md:314-318` (rule 0), `README.md:108-170` (section 2's seed half)
- Verify: `scripts/generate-content.py` (run, not modified)

**Interfaces:**
- Consumes: "large holdings", "2-of-2 keys", "cosigner seed" from Task 1.
- Produces: the two-legged argument that Task 3 and Task 4 both cite. Leg one is your dice, so no vendor made your entropy. Leg two is two makers, so no single maker's other defects can satisfy the quorum alone. Also produces the mis-press caveat that Task 8 links to.

- [ ] **Step 1: Write the failing check**

```bash
cd "$(git rev-parse --show-toplevel)"
# The second-implementation bullet must admit what it cannot see.
grep -c "mis-press" README.md
```

Expected before editing: `0`.

- [ ] **Step 2: Make rule 0 plural**

`README.md:314-318` says "Audit how the seed was generated and how strong the passphrase is", and closes with "Everything below assumes real entropy at the root". Two cosigner seeds means two audits and two roots. Rewrite both sentences to say so without lengthening the rule; rule 0 is a precondition and its value is that it is short.

- [ ] **Step 3: Rewrite the vendor diversity bullet**

The bullet at `README.md:163-167` currently reads that a 2-of-3 built from two devices by the same maker is not protected against that maker's defect, and calls this the specific lesson of the Coldcard event. The Coldcard event was a random number generator regression, and supplying your own dice entropy removes that defect from every cosigner at once.

So the bullet keeps its advice and changes its reason. What per-maker risk remains: firmware, the signing path, and whether the screen tells the truth about an address. State the two legs explicitly, because a reader who has just rolled their own seeds could otherwise conclude that one maker is now acceptable.

- [ ] **Step 4: Add the mis-press caveat to the second-implementation bullet**

The bullet at `README.md:152-158` presents two tools agreeing as the proof of a correct conversion. It is blind to a typo: press 4 where the die showed 5 and both tools agree perfectly, `sha256sum` matches, and the words are valid BIP-39 for a wallet the dice never made.

Add that caveat, and say what does catch it: the paper record of what the dice showed, compared against the screen. This is the bullet Task 8 links to from the doing page.

Also make the second implementation a requirement rather than advice once there is more than one seed, because with two cosigner seeds every seed comes from one tool on one machine, so the tool is the single flaw that could reach both keys.

- [ ] **Step 5: Leave the passphrase half alone**

Section 2's second half argues for a BIP-39 passphrase entirely in single-seed terms. Whether the framework keeps recommending one per cosigner is open item 3 in the spec and is not decided here. Do not edit it, and do not let this task's edits imply an answer.

- [ ] **Step 6: Run the generator and check the constraints**

```bash
python scripts/generate-content.py
grep -n '[—–]' README.md; echo "exit: $?"
grep -nE '2-of-(2|3)' README.md | grep -vE '2-of-2 keys|2-of-3 cards'; echo "exit: $?"
```

Expected: generator exits 0 with the same counts as Task 1; both greps produce no output and `exit: 1`. The second grep will fail on section 2's old phrase "A 2-of-3 built from two devices", which this task rewrites, so a failure here means step 3 was left half done.

- [ ] **Step 7: Commit**

```bash
git add README.md
git commit -m "Audit two roots, and say what a second vendor still buys once you roll your own" \
  -m "Rule 0 assumed entropy at one root. And the vendor diversity bullet argued from the Coldcard generator regression, which your own dice removes from every cosigner at once, so the advice now argues from what is left: firmware, the signing path, and whether the screen tells the truth about an address." \
  -m "Also admits what two agreeing tools cannot see. They compare the typed log against another conversion of the same typed log, so a mis-press passes every check in the system." \
  -m "*Collaboration by Claude*"
```

---

### Task 3: The ordered checklist

Section 6 is the worked example, and it currently produces one seed and one key. This task makes it two cosigner seeds and one key, adds the roll sheet, adds the paper comparison, and gives the generation-only journey a labelled exit.

**Files:**
- Modify: `README.md:651-736` (Phase B), `README.md:563-650` (Phase A, the download and clean room steps)
- Verify: `scripts/generate-content.py` (run, not modified)

**Interfaces:**
- Consumes: the two-legged argument and the mis-press caveat from Task 2.
- Produces: two anchors that Task 7 and Task 8 both link to. Phase B keeps its existing anchor `phase-b-back-up-the-seed-one-offline-session`; the generation-only exit is an H4 inside Phase B whose heading text must be exactly `If you are stopping after generating`, giving the anchor `if-you-are-stopping-after-generating`.

- [ ] **Step 1: Write the failing check**

```bash
cd "$(git rev-parse --show-toplevel)"
grep -c "roll-sheet.html" README.md
grep -c "If you are stopping after generating" README.md
```

Expected before editing: `0` and `0`.

- [ ] **Step 2: Add printing the roll sheet to the online step**

Phase B's step 6 is the "while still online" step. `dice-to-seed` publishes `roll-sheet.html` as its own release asset, covered by `SHA256SUMS` with the AppImage and the Tails bundle. It is printed on an ordinary networked machine during preparation, because an amnesic offline session is the wrong place to be arranging a printer, and it is blank, so printing it carries nothing.

Say all of that in two sentences, and add the rule that nothing filled in ever goes near a printer, because a spooler, an internal disk and a network queue are memory this framework cannot audit.

One sheet per roll session. For the recommended shape that is three: one per cosigner seed, one for the backup key.

- [ ] **Step 3: Make the rolling step produce two cosigner seeds**

The roll and conversion steps assume one seed. They now produce two, on a fresh sheet each, and the instruction has to include clearing the rolls between seeds.

State why explicitly: `dice-to-seed` clears the roll log when the mode changes and deliberately keeps it when the requested mode is the one already in effect, so that pressing the button you are on cannot destroy fifty rolls. Rolling a second cosigner seed is not a mode change, so without clearing, the second seed is derived from a hash of both sheets and cannot be recomputed from the sheet that appears to have produced it.

- [ ] **Step 4: Add the paper comparison as a numbered step**

Immediately before deriving, the reader compares the sheet against the screen, row by row. The app shows the log in rows of ten numbered by the position of the first roll, and the printed sheet numbers its rows identically, so the comparison is a row-by-row read rather than a hunt through undifferentiated digits.

This is the only check in the system that can catch a mis-press, and the step says so, citing section 2.

- [ ] **Step 5: Add the table discipline rule**

Two filled seed sheets exist at once, because sheets survive until the dry run proves the backup, and the sheet deliberately carries no name, no date and no label. So: one sheet in front of the machine at a time, the other face down and out of the way, and the words card carries which cosigner is which, because the card is the artifact designed to be kept.

- [ ] **Step 6: Add the generation-only exit**

A new H4 inside Phase B, heading text exactly `If you are stopping after generating`. It says what the reader is holding: two seeds written on paper, in one place, with nothing backed up. It says the dice sheets are still destroyed in that sitting, because a sheet is a seed in plain text. It says not to fund the wallet beyond pocket change until the backup exists. And it says the machine still never goes online again.

- [ ] **Step 7: Reconcile the destroy step**

The existing step that destroys the roll logs names two of them, one for the seed and one for the key. It now names three and makes the count the instruction: three sheets in, three sheets destroyed, in the sitting that made them.

- [ ] **Step 8: Run the generator and check the constraints**

```bash
python scripts/generate-content.py
```

Expected: exits 0. The framework page count stays 15 because this task adds an H4 rather than an H2, but the anchor count rises, so the line now reads `34 anchors mapped`. A count of 33 means the new heading was written at the wrong level.

```bash
grep -n '[—–]' README.md; echo "exit: $?"
grep -c "If you are stopping after generating" README.md
grep -c "### If you are stopping after generating" content/framework/6-setup-from-zero-the-ordered-checklist.md
```

Expected: no dashes; the heading present exactly once.

- [ ] **Step 9: Commit**

```bash
git add README.md
git commit -m "Roll two cosigner seeds, compare them against paper, and let a reader stop there" \
  -m "The worked example produced one seed and one key. It now produces two cosigner seeds and one key, on a fresh printed sheet each, with the rolls cleared between seeds because the tool keeps the log when the mode does not change." \
  -m "The comparison against paper is a numbered step of its own, immediately before deriving, because it is the only check here that can catch a mis-press. And generating without backing up is now a labelled exit that says what the reader is holding rather than an omission." \
  -m "*Collaboration by Claude*"
```

---

### Task 4: The traps and the failure matrix

Section 7 and section 10 both enumerate failures, and both enumerate them for one seed and one key.

**Files:**
- Modify: `README.md:772-838` (section 7), `README.md:1155-1179` (section 10)
- Verify: `scripts/generate-content.py` (run, not modified)

**Interfaces:**
- Consumes: the clear-the-rolls reasoning from Task 3, the two legs from Task 2.
- Produces: nothing later tasks depend on.

- [ ] **Step 1: Write the failing check**

```bash
cd "$(git rev-parse --show-toplevel)"
# The matrix must have a row for two cosigner seeds sharing one sheet.
grep -c "one sheet for two cosigner seeds" README.md
```

Expected before editing: `0`.

- [ ] **Step 2: Add the sibling trap to section 7**

Section 7's existing trap is "One seed, several passphrases, called multisig", which is about deriving cosigners from a single mnemonic. Keep it exactly as it is; it is still a trap and the reasoning is unchanged.

Add its sibling: two cosigner seeds rolled onto one sheet, or rolled without clearing the log between them. Say what each produces. Sharing a sheet gives a quorum whose keys are not independent, which is a 2-of-2 wallet that fails as one unit. Failing to clear the log gives two unrelated seeds, which is not that collapse, but the second seed cannot be recomputed from the sheet that appears to have produced it, so the property the dice were for is gone with no visible sign.

Note which of these the tools refuse. A seed and a key sharing a log is refused by both tools. Two cosigner seeds sharing a sheet is refused by nothing.

- [ ] **Step 3: Split the defective generator row in section 10**

The row at `README.md:1162` says nothing in the framework saves you from a defective device generator, and names as the defence your own dice entropy, vendor diversity in multisig, and rotation on disclosure. With two vendors as the premise rather than a mitigation, the row splits: one row for your entropy, which the dice answer, and one for a maker's other defects, which the second vendor answers and which no backup can reach.

- [ ] **Step 4: Update the roll log rows in section 10**

The row that says a roll log survived in a drawer names "log one" as the seed and "log two" as the key. It now names three sheets. The row for reusing one log across the seed and the key keeps its reasoning and gains a sibling row for one sheet used for two cosigner seeds, whose "what saves you" is nothing, and which no tool currently refuses.

- [ ] **Step 5: Run the generator and check the constraints**

```bash
python scripts/generate-content.py
grep -n '[—–]' README.md; echo "exit: $?"
grep -nE '2-of-(2|3)' README.md | grep -vE '2-of-2 keys|2-of-3 cards'; echo "exit: $?"
```

Expected: generator exits 0 with 34 anchors; both greps silent with `exit: 1`. Section 7's existing "superseded 2-of-3 artifacts" phrase is one the second grep will catch, so it needs its noun too.

- [ ] **Step 6: Commit**

```bash
git add README.md
git commit -m "Name the trap no tool refuses: two cosigner seeds on one sheet" \
  -m "Section 7 had the one-seed-many-passphrases trap and not its sibling. A shared sheet gives a 2-of-2 wallet whose keys are not independent, and an uncleared log gives a seed that cannot be recomputed from the sheet that appears to have made it. Both tools refuse a seed and a key sharing a log; nothing refuses this." \
  -m "The failure matrix also split its defective-generator row, because a second vendor is now the premise rather than a mitigation." \
  -m "*Collaboration by Claude*"
```

---

### Task 5: Section 11 loses its centrepiece

Section 11 is the upgrade path, and its strongest item is graduating to multisig for large holdings. That is now the premise, so the item goes and the section gains the rule that a human cosigner runs the document themselves.

**Files:**
- Modify: `README.md:1239-1258` (the graduation bullet and the disjoint lists rule)
- Verify: `scripts/generate-content.py` (run, not modified)

**Interfaces:**
- Consumes: "large holdings" and "2-of-2 keys" from Task 1.
- Produces: the third-list rule that Task 7's new page summarises in one sentence.

- [ ] **Step 1: Write the failing check**

```bash
cd "$(git rev-parse --show-toplevel)"
# The graduation bullet must be gone, and the cosigner rule present.
grep -c "graduate the wallet itself to multisig" README.md
grep -c "runs this document themselves" README.md
```

Expected before editing: `1` and `0`. After: `0` and `1`.

- [ ] **Step 2: Remove the graduation bullet and keep its argument**

The bullet at `README.md:1239-1247` carries an argument worth keeping even though its recommendation is now the premise: the literature's strongest criticism of share-based backups is that shares must be recombined in one place to spend, while a multisig wallet never assembles a complete secret anywhere, and the two compose because multisig protects the use of keys while this framework protects the backup of each key.

Move that argument to where the premise is stated, and write it as multi-vendor multisig rather than multisig, because the diversity is the half that makes the quorum mean anything. Delete the bullet from section 11.

- [ ] **Step 3: Add the third disjoint list**

Section 11's existing rule keeps two lists disjoint: a route to the payload, or a share, never both to the same person. Add the third. If another person holds a cosigner key, they run this document themselves, for their own key, and the two backups never touch: no payload of yours holds their seed, no payload of theirs holds yours, and neither of you holds the other's cards.

Say that this cuts against the section's direction of travel, which is about gradually involving people, because that is exactly why it has to be stated rather than left implied.

- [ ] **Step 4: Run the generator and check the constraints**

```bash
python scripts/generate-content.py
grep -n '[—–]' README.md; echo "exit: $?"
```

Expected: generator exits 0 with 34 anchors; grep silent.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "Move the multisig argument to the premise, and say a human cosigner runs this alone" \
  -m "Graduating to multisig was the strongest item in the upgrade path and is now the starting position, so the bullet goes and its argument moves to where the premise is stated: multi-vendor multisig protects the use of keys, this framework protects the backup of each key." \
  -m "Section 11 gains a third list that must stay disjoint from the other two. A cosigner who is another person runs this document for their own key, and neither backup ever holds the other's seed." \
  -m "*Collaboration by Claude*"
```

---

### Task 6: Roll counts are per sheet

`NUMBERS.md` derives the roll counts and says why 99 is not enough. It says it once, for one log.

**Files:**
- Modify: `NUMBERS.md` (the roll count derivation and the one-die section)
- Verify: `scripts/generate-content.py` (run, not modified)

**Interfaces:**
- Consumes: the three-sheet count from Task 3.
- Produces: the anchors Task 8 links to, which keep their current slugs: `why-99-rolls-is-not-256-bits` and `why-this-guide-says-one-die`.

- [ ] **Step 1: Write the failing check**

```bash
cd "$(git rev-parse --show-toplevel)"
grep -c "per sheet" NUMBERS.md
```

Expected before editing: `0`.

- [ ] **Step 2: Say the count is per sheet**

The derivation of 111 rolls for 24 words and 60 for 12 is unchanged; arithmetic does not move. What changes is that the count applies to each sheet, and the recommended shape has three of them. State that once, where the count is derived, and do not repeat it.

- [ ] **Step 3: Check the one-die section still holds**

The one-die argument is about a fixed reading order and the cost of forgetting it, and it is unaffected by how many sheets there are. Read it and confirm nothing in it assumes a single session. If it does, fix only that.

- [ ] **Step 4: Run the generator and check the constraints**

```bash
python scripts/generate-content.py
grep -n '[—–]' NUMBERS.md; echo "exit: $?"
```

Expected: generator exits 0; grep silent.

- [ ] **Step 5: Commit**

```bash
git add NUMBERS.md
git commit -m "Say the roll count is per sheet, because there are now three of them" \
  -m "The arithmetic is unchanged. What changed is that 111 rolls is a property of one sheet and the recommended shape needs three, so the derivation says so where the count is derived rather than leaving it to the reader to multiply." \
  -m "*Collaboration by Claude*"
```

---

### Task 7: The new page

One page that names the two actions and routes the reader, registered in the generator so it becomes a site page, and linked from the documents that need it.

**Files:**
- Create: `ACTIONS.md`
- Modify: `scripts/generate-content.py:63-66` (`SIBLING_PAGES`), `scripts/generate-content.py:374-377` (`STANDALONE`)
- Verify: `scripts/generate-content.py` (run), `scripts/check-links.py` (CI, see step 6)

**Interfaces:**
- Consumes: every phrase produced by Tasks 1 through 6.
- Produces: the file `ACTIONS.md`, mapped to the slug `actions` and served at `/actions/`, whose H2 headings must be exactly `Generating seeds`, `Backing seeds up`, and `Which parts you need`, giving the anchors `generating-seeds`, `backing-seeds-up` and `which-parts-you-need`. Task 8 links to `ACTIONS.md` by filename, which the generator rewrites.

- [ ] **Step 1: Write the failing check**

```bash
cd "$(git rev-parse --show-toplevel)"
python scripts/generate-content.py | tail -1
```

Expected before editing: the summary line ends `2 sibling pages, 34 anchors mapped`. After this task it must read `3 sibling pages`.

- [ ] **Step 2: Write `ACTIONS.md`**

Sections, in this order, with the exact H2 headings named in Interfaces above.

An opening that states the two actions and that either is useful without the other.

`Generating seeds` covers what it produces (one seed per cosigner, from dice, with an origin you can recompute), that it is optional if you already hold seeds you trust, and that stopping here is supported, linking to `README.md#if-you-are-stopping-after-generating`, the exit Task 3 creates.

`Backing seeds up` covers what it produces (three cards, the encrypted payload, the written instructions) and that it takes the seeds you hold whatever their origin, subject to rule 0.

`Which parts you need` is the routing table: three journeys, and for each one which sections of the framework to read and how many sheets of dice numbers it needs. Three for both actions, one for backup only, two for generation only.

Then the position statements, short: one owner holding both cosigner keys, each on hardware from a different maker; if another person holds a key they run this document themselves, per Task 5; and 2-of-2 keys with other shapes supported by the tools and not covered here.

Links to the framework are written as `](README.md#anchor)` and links to the numbers page as `](NUMBERS.md#anchor)`, because that is what works when the file is read on GitHub. The generator rewrites both for the site.

- [ ] **Step 3: Register the page in the generator**

Two edits, and both are needed. `SIBLING_PAGES` is what `retarget()` walks to rewrite `](ACTIONS.md#...)` links found in other documents. `STANDALONE` is what actually writes the page. Missing the first gives dead links from other pages; missing the second gives a page that no file exists for.

```python
SIBLING_PAGES = {
    "NUMBERS.md": "numbers",
    "LANDSCAPE.md": "landscape",
    "ACTIONS.md": "actions",
}
```

```python
STANDALONE = [
    ("ACTIONS.md", "actions", "Generate, back up, or both", 2),
    ("NUMBERS.md", "numbers", "How the numbers work", 4),
    ("LANDSCAPE.md", "landscape", "What else is out there", 5),
]
```

- [ ] **Step 4: Move the framework below the new page**

The new page sits above the framework in the sidebar, so the framework's weight changes from 2 to 3. That weight is passed in the `write()` call for `framework/_index.md`:

```python
write(
    "framework/_index.md",
    {"title": yaml_quote("The framework"), "weight": 3},
    retarget(preamble, from_depth=1),
)
```

- [ ] **Step 5: Run the generator**

```bash
python scripts/generate-content.py | tail -1
ls content/actions/_index.md
grep -n "weight" content/actions/_index.md content/framework/_index.md
```

Expected: the summary line reads `3 sibling pages`; the page file exists; weights are 2 for actions and 3 for framework.

- [ ] **Step 6: Check the links, which needs the built site**

`check-links.py` reads built HTML, so it needs Hugo. Hugo is not installed on the author's machine and the version is pinned to 0.164.0 extended with Hextra fetched as a Go module, so the honest instruction is that this check runs in CI on the pull request.

If you do have Hugo extended 0.164.0 and Go available:

```bash
scripts/build-site.sh
```

Expected: the script runs the generator, builds, runs the external-request guard, and ends with `build-site: output in public/`. Any dead anchor fails at the last step and names the page and the link.

If you do not: say so in the commit body rather than claiming the check passed.

- [ ] **Step 7: Commit**

```bash
git add ACTIONS.md scripts/generate-content.py
git commit -m "Add a page that names the two actions, and put it above the framework" \
  -m "One page saying that generating seeds and backing seeds up are separate, that either is useful alone, and which parts of the framework each of the three journeys needs. Registered in both places the generator needs: SIBLING_PAGES so links to it from other documents get rewritten, and STANDALONE so the page is written at all." \
  -m "*Collaboration by Claude*"
```

---

### Task 8: The doing page

`START-HERE.md` is the short ordered version. It stays one ordered list with a fork inside it, because two lists is how one offline sitting becomes two evenings with a plaintext seed in between.

**Files:**
- Modify: `START-HERE.md:7-16` (the opening), `START-HERE.md:35-48` (the kit list), `START-HERE.md:50-76` (step 1), `START-HERE.md:78-136` (step 2), `START-HERE.md:139-160` (step 3)
- Verify: `scripts/generate-content.py` (run, not modified)

**Interfaces:**
- Consumes: `ACTIONS.md` from Task 7, the Phase B anchors from Task 3, the section 2 caveat from Task 2, the NUMBERS anchors from Task 6.
- Produces: nothing later tasks depend on.

- [ ] **Step 1: Write the failing check**

```bash
cd "$(git rev-parse --show-toplevel)"
grep -c "ACTIONS.md" START-HERE.md
grep -c "against the paper" START-HERE.md
```

Expected before editing: `0` and `0`.

- [ ] **Step 2: Rewrite the opening fork**

The existing "Where the seed comes from" paragraph says the framework does not care where your seed came from and points at step 2. It now has to name the three journeys and link to `ACTIONS.md`, and it has to say two cosigner seeds rather than a seed.

- [ ] **Step 3: Add the printed sheets to the kit list**

The kit list gains the roll sheets, printed before anything starts, one per roll session, three for the recommended shape. The existing "Paper and a pen" row stays, because the words still get written by hand onto something that is kept.

- [ ] **Step 4: Add printing to step 1**

Step 1 is the only step that happens online, which is exactly why printing belongs there and not in step 2. Add taking `roll-sheet.html` from the release and printing it while blank, with the rule that nothing filled in goes near a printer.

- [ ] **Step 5: Make step 2 conditional and add the comparison**

Step 2 rolls twice for cosigner seeds and once for the key, on a fresh sheet each, with the rolls cleared between seeds. A reader who brought their own seeds rolls the key sheet only.

Then add the comparison as its own numbered instruction, before step 3 converts anything: read the sheet against the screen, row by row, rows of ten numbered by the position of the first roll. Say what it catches and link to the caveat Task 2 added, because the reason is the whole point and the tool's own history is that the paper was requested without it.

- [ ] **Step 6: Add the table discipline line**

One sheet in front of the machine at a time, the other face down, and the words card carries which cosigner is which. Keep it to two sentences; the argument for it lives in the framework.

- [ ] **Step 7: Run the generator and check the constraints**

```bash
python scripts/generate-content.py
grep -n "README.md" content/_index.md; echo "exit: $?"
grep -n '[—–]' START-HERE.md; echo "exit: $?"
```

Expected: the generator exits 0. The first grep must be silent: the generator already exits with an error if an unrewritten `README.md` link survives onto the front page, and this confirms the same for `ACTIONS.md` links by their absence from the output. No dashes.

- [ ] **Step 8: Commit**

```bash
git add START-HERE.md
git commit -m "Fork the doing page at the top, and compare the sheet against the screen before deriving" \
  -m "The page opens by naming the three journeys instead of assuming the reader starts from nothing, and step 2 becomes conditional: two cosigner seeds for someone generating, the key sheet alone for someone who brought their own." \
  -m "Printing the sheet moves to step 1, which is the only step that happens online, and the comparison against paper is its own instruction with its reason attached, because asking for a second plaintext copy of a seed without asking for the comparison is all of the cost and none of the benefit." \
  -m "*Collaboration by Claude*"
```

---

### Task 9: The sweep, and the dates

The last task is the one that catches what the other eight left behind, and it is the only task that changes the revision notes.

**Files:**
- Modify: `README.md`, `START-HERE.md`, `NUMBERS.md`, `ACTIONS.md` (revision notes and any stragglers), `LANDSCAPE.md` (only if it names a single-seed setup)
- Verify: `scripts/generate-content.py`, and `scripts/build-site.sh` in CI

**Interfaces:**
- Consumes: everything.
- Produces: a branch ready for a pull request.

- [ ] **Step 1: Sweep for thresholds without their noun**

```bash
cd "$(git rev-parse --show-toplevel)"
grep -nE '[0-9]-of-[0-9]' README.md START-HERE.md NUMBERS.md ACTIONS.md LANDSCAPE.md \
  | grep -vE '2-of-2 keys|2-of-3 cards|3-of-5 cards'
```

Expected: no output. Every other spelling is a defect by the naming rule, including the tool's 3-of-5 default, which must read "3-of-5 cards".

- [ ] **Step 2: Sweep for single-seed leftovers**

```bash
grep -niE "your seed phrase|the seed you|a single seed|one seed and one key" \
  README.md START-HERE.md ACTIONS.md
```

Expected: every hit is either inside a trap that is deliberately about one seed (section 7's one-seed-many-passphrases trap, which stays) or a defect. Read each one and decide; do not bulk edit.

- [ ] **Step 3: Sweep for dashes and curly quotes**

```bash
grep -n '[—–]' *.md; echo "exit: $?"
python -c "import glob,io,sys; bad=[(f,i+1) for f in glob.glob('*.md') for i,l in enumerate(io.open(f,encoding='utf-8')) if any(chr(c) in l for c in (8216,8217,8220,8221))]; [print('curly quote:',f,'line',n) for f,n in bad]; sys.exit(1 if bad else 0)"
```

Expected: no output from either.

- [ ] **Step 4: Move the revision dates**

Each of the four documents carries a hand-written date inside `<!-- revision:start -->` markers, and the date means the day a person last checked the claims. The claims genuinely changed, so all of them move to the date this work lands. `ACTIONS.md` gets a note of its own in the same form, because the generator stamps the build commit into every one of these blocks and a page without the markers gets no commit stamp.

- [ ] **Step 5: Run the generator, and confirm the markers**

```bash
python scripts/generate-content.py | tail -1
grep -rn "revision:start" content/ ; echo "exit: $?"
```

Expected: the summary line reads `3 sibling pages`. The second grep must be silent, because a surviving marker means a revision block was not substituted, which the generator also exits on.

- [ ] **Step 6: Push the branch and open the pull request**

```bash
git push -u origin two-actions-and-multivendor-scope
gh pr create --title "The framework is two seeds from two vendors, and it names its two actions" --body-file - <<'BODY'
Implements `docs/superpowers/specs/2026-08-22-two-actions-and-multivendor-scope-design.md`.

The framework is now for large holdings, and its recommended wallet is 2-of-2 keys held by one
owner on hardware from two makers. That removes the single-key case, which was most of the
document. It also names the two actions it supports, generating seeds and backing seeds up,
either of which is useful alone, on a new page above the framework.

And it adopts the roll sheet from `dice-to-seed` pull request 33, along with the reason it
exists: every check here compares the typed log against another conversion of the same typed
log, so none of them can see a mis-press. This document asked the reader to write every digit
down, gave no reason, and called two agreeing tools the proof. The comparison against paper is
now a numbered step with its reason attached.

Link checking runs here rather than locally, because Hugo is pinned to 0.164.0 extended with
Hextra as a Go module.

*Collaboration by Claude*
BODY
```

Never merge it. Opening it is the job; merging is the human's.

---

## Open questions this plan does not answer

1. **The passphrase.** Section 2 argues for a BIP-39 passphrase entirely in single-seed terms. Whether the framework recommends one per cosigner, one across the quorum, or none, interacts with a two-key wallet differently, and Task 2 step 5 deliberately leaves it untouched. It wants its own decision and probably its own change.
2. **`dice-to-seed` and two seed sheets.** Nothing in either tool refuses two cosigner seeds rolled onto one sheet, or the uncleared log between seeds. This plan writes instructions around both. Whether the tool should refuse them is a question for that repository.
3. **`seed-generation`.** Eleven documents of vendor-neutral generation material sit in a sibling repository, with a plan from 2026-08-09 to merge them here that has not run. Spec section 9 keeps it out of scope, and `ACTIONS.md` points at it as the survey of methods this framework is not.
