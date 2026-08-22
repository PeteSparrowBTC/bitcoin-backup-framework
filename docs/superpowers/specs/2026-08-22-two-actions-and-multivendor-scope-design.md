# Design: two actions, and a framework for two seeds from two vendors

Date: 2026-08-22

Two changes that arrived together and turn out to be one change. The framework starts
saying out loud that it supports two separate actions, generating seeds and backing seeds
up, either of which is useful without the other. And it narrows its subject to large
holdings, where the recommended wallet is 2-of-2 multisig across two vendors, which removes
the single-seed case from the document.

They are one change because the second is what makes the first necessary. A framework that
recommends two cosigner seeds has to say who generates them and when, and a reader who
already holds both has to be able to skip that half without reading around it.

## 1. Scope

The framework is for large holdings. The recommended wallet is 2-of-2 multisig, both
cosigner keys held by one owner, each key on hardware from a different maker.

The single-seed case leaves the document. Today it is the main line and multisig is an
upgrade at the end of section 11; that inverts.

Other quorum shapes (2-of-3 keys, 3-of-5, anything else) work in the tools and are not
covered here. The document says so once and does not hedge further.

## 2. The two actions, and the three journeys

Generating produces one seed per cosigner, from dice, with an origin you can recompute.
Backing up takes the seeds you hold and produces the cards and the encrypted payload.

| Journey | Who it is |
| --- | --- |
| Both, one sitting | No wallet yet |
| Backup only | Arrives holding two cosigner seeds already trusted |
| Generation only | Wants keys they can vouch for, not ready to build the backup |

All three are supported destinations, including the third, which is section 6.

## 3. Which action owns the dice

The backup key exists only to lock the payload, so it belongs to the backup action. There is
exactly one of it however many cosigners there are, because the tool puts every cosigner seed
into one payload behind one key and one set of cards.

| Journey | Sheets of dice numbers |
| --- | --- |
| Both, 2-of-2 | Three: one per cosigner seed, one for the key |
| Backup only | One, for the key |
| Generation only, 2-of-2 | Two, one per cosigner seed |

No two sheets are ever the same sheet, and there are now two ways to get that wrong rather
than one.

A seed and the key: the key becomes derivable from the wallet it protects, so the cards stop
protecting anything. Both tools already refuse this.

Two cosigner seeds: a quorum whose keys are not independent, which is a 2-of-2 that fails as
one unit. Nothing currently refuses this.

`dice-to-seed` clears the roll log when the mode changes, and deliberately keeps it when the
requested mode is the one already in effect, so that pressing the button you are on cannot
destroy fifty rolls (`ModeSwitch.Apply`). Rolling a second cosigner seed is not a mode change,
so the second seed is derived from a hash of both sheets. The seeds are unrelated, so this is
not the collapse above, but it silently breaks the property the dice were for: cosigner two
cannot be recomputed from the sheet a reader believes produced it. The generation instructions
must therefore say to clear the rolls or restart the app between seeds. Whether the tool
should refuse this instead is an open item.

### The printable roll sheet

`dice-to-seed` pull request 33 adds it: `printable/roll-sheet.html`, shipped as its own release
asset under `SHA256SUMS`, open at the time of writing on `feat/check-rolls-against-paper`.

The reason for the paper is sharper than the one first written here, and the framework should
adopt it rather than paraphrase it. Every check in this system compares the typed roll log
against another conversion of that same typed log: a second implementation, `sha256sum`, Ian
Coleman. None of them can see a mis-press. Press 4 where the die showed 5 and both tools agree
perfectly, the counter still reads sixty, and the words are valid BIP-39 for a wallet the dice
never made. The paper is the only independent record of what the dice actually showed, so
comparing it against the screen is the only check that can catch that error.

That exposes the same defect in this framework's own instructions. START-HERE tells the reader
to write each digit down as it lands, gives no reason, and then presents two tools agreeing as
the proof. So the document asks for a second plaintext copy of the seed and never asks for the
comparison that would justify the risk. It is the criticism the tool's changelog makes of
itself, and it applies here word for word. The comparison becomes a numbered step immediately
before deriving, and the document says why the paper exists.

What the sheet is, as built: one page, plain HTML with no script and no external reference,
blank so it carries nothing until written on, rows of ten numbered by the position of the first
roll so the comparison is a row-by-row read rather than a hunt through undifferentiated digits,
heavier rules after rolls 50 and 60 with a legend, and 240mm of content against 275mm on A4. It
says destroy twice in the largest type on the page, says why, and says plainly that it is not a
backup. Its row labels are asserted against the app's arithmetic by a test, because a reader
already holding a printed copy cannot reprint it.

Printing happens on an ordinary networked machine during preparation, before booting, because an
amnesic offline session is the wrong place to be arranging a printer. So this belongs in step 1
of the doing page, the only step that happens online, and not in step 2 where the rolling is.

The sheet deliberately has no place to write which wallet it is: no name, no date, no label, no
amount. The exception is two tick boxes for the sheet's purpose, seed or backup key, which earn
their place because one log used for both makes the key derivable from the wallet it protects.

That exception was designed for one seed and one key. This framework has three sheets, two of
which tick the same box, and nothing on either says which cosigner it made. Both filled seed
sheets also exist at once, because sheets survive until the dry run proves the backup. Recovery
from a mixup is real but tedious: derive from a sheet and see whose words come out. Two ways to
close it, and only the first needs the tool.

1. Ordinal tick boxes, one of two and two of two. They carry no identity, and they arguably help
   the owner more than a finder, since a finder learns that the sheet alone cannot spend.
2. Table discipline alone: never two filled seed sheets in one place, with the words card
   carrying the association rather than the sheet.

Open item 5.

## 4. What two vendors buys, once you bring your own dice

Section 2 currently ties vendor diversity to the Coldcard event, which was a random number
generator regression. Supplying your own entropy removes that defect from every cosigner at
once, so the reason for diversity changes rather than disappearing: firmware, the signing
path, and whether the screen tells the truth about an address are all still per-maker.

So the recommendation has two independent legs, and the document should present them as two:

1. Your dice, so no vendor made your entropy.
2. Two makers, so no single maker's other defects can satisfy the quorum alone.

The second leg is also why 2-of-2 rather than the more usual 2-of-3. Redundancy against a lost
or dead device comes from the backup, which holds both cosigner seeds, so a third key adds no
protection and costs a third secret and a wider spending surface, since any two of three can
spend. 2-of-2 is the tightest spending rule and the fewest secrets, and it pairs one to one
with two makers.

A dead device is therefore not a loss and must not be written as one. It costs one offline
session: take the payload and enough cards to the retired machine, restore that cosigner seed,
load it onto a new device. The machine the framework retires from the network is exactly the
machine a restore needs, so retiring it keeps the spare part rather than spending one.

## 5. Other people holding cosigner keys

The framework's multisig is one owner with two keys. If another person holds a cosigner key,
they run this document themselves, for their own key, and the two backups never touch: no
payload of yours holds their seed, no payload of theirs holds yours, and neither of you holds
the other's cards.

This belongs beside section 11's existing rule about keeping the two lists disjoint, because
it adds a third list that must stay separate from both. It also cuts against that section's
direction of travel, which is about gradually involving people, so it has to be stated rather
than implied.

## 6. Generation only, and what it has to admit

Someone who stops after generating holds two seeds written on paper, in one place, and has
backed up nothing. The dice sheets still get destroyed in that sitting, because a sheet is a
seed in plain text. The page says not to fund the wallet beyond pocket change until the backup
exists, and the machine still never goes online again.

Supported with a stated cost, rather than supported without one.

## 7. The new page

One page, above the framework in the sidebar, which states the two actions, the three
journeys, the single-owner 2-of-2 position, and the rule in section 5. It says which parts of
the framework each journey needs, and it is the page the short doing page forks from.

Working name "Generate, back up, or both". Not settled.

It is self-contained for the recommended path and does not survey generation methods. Section
9 is why.

## 8. Edits to existing documents

Exact wording belongs in the implementation plan. This is the list of what contradicts the new
scope and therefore cannot be left alone.

| Where | What has to change |
| --- | --- |
| README preamble | Audience is someone postponing custody who is told that a password manager and two-factor authentication equip them for everything below. Two makers and a recovery-critical descriptor is a different reader |
| README one-sentence version | Written for a single root of trust |
| Section 2 | Single-seed framing throughout; vendor diversity's rationale per section 4 above; the second-implementation check becomes a requirement rather than advice once there is more than one seed, and gains the caveat that it is blind to a mis-press |
| Section 3 | Rule 0 audits how the seed was generated, singular, and assumes real entropy at one root. Two cosigner seeds means two audits and two roots |
| Section 6 | The worked example is one seed and one key. Needs the second cosigner seed, the clear-the-rolls step, and a labelled exit for the generation-only journey |
| Section 7 | The one-seed-many-passphrases trap stays and gains a sibling: two cosigner seeds from one sheet |
| Section 10 | Three rows assume one seed and one key: the defective-generator row, where vendor diversity is now the premise rather than a mitigation; the surviving-roll-log row, which names log one as the seed and log two as the key; and the reused-log row, which needs a sibling for two cosigner seeds sharing one sheet |
| Section 11 | Loses its centrepiece, since multisig is now the premise. Keeps involving people, gains the third disjoint list |
| Section 12 | The complexity-budget and no-theater argument now has to say which side of that line a two-maker quorum sits on, and who this document is not for |
| START-HERE | Opens with the fork; step 1 gains printing the roll sheet, since that is the online step; step 2 becomes conditional, rolls twice for seeds, and gains the paper-against-screen comparison before deriving; stays one ordered list rather than splitting in two |
| NUMBERS | Roll counts are per sheet, and there are now up to three sheets |

## 9. Relationship to seed-generation, and what stays out

`PeteSparrowBTC/seed-generation` holds eleven documents on generating a seed: dice, coins and
cards, device generators, entropy, verification, the Coldcard incident. The plan of 2026-08-09
(`docs/superpowers/plans/2026-08-09-one-guide.md`) decided to merge it here by subtree under
`docs/generating`. That merge has not happened, and the repository has been untouched since 9
August. Its step 0, the Krux dash error, was corrected.

The merge stays out of scope for this change, for two reasons.

It is a different job with its own steps, including five chapters that plan lists as missing:
test spend, recovery rehearsal, verifying the device, the defect playbook, and the watch-only
backup. Doing it inside this change would bury both.

And its voice conflicts in a way that needs deciding first. `seed-generation` is deliberately
vendor-neutral, pointing at Coldcard, SeedSigner and Ian Coleman without preference, and the
2026-08-09 plan warns that merging it carelessly turns a neutral reference into a vendor pitch.
This change makes the framework more opinionated, not less: dice, two named tools, two makers,
one quorum shape. So the new page is written here and self-contained, and it points at
seed-generation as the survey of methods it is not.

## 10. Naming discipline

Two thresholds now appear in one document and they are different numbers: 2-of-2 keys to
spend, 2-of-3 cards to recover. Every mention carries its noun. A bare "2-of-2" or "2-of-3" is
a defect. The backup tool's own default is 3-of-5 cards, so the instruction to change it to
2-of-3 has to survive too.

## 11. Build consequences

- `generate-content.py`: the new page joins `STANDALONE`, and `retarget()` has to place links
  into it from README, START-HERE, NUMBERS and LANDSCAPE. The anchor map is built from
  README's headings alone today.
- Hugo weights reorder, since the new page sits above the framework.
- `check-links.py` is the check that every moved anchor still lands, and it needs the built
  site, which means CI rather than this machine.
- The revision dates on all four documents move, because the claims genuinely change.

## 12. Open items

1. The new page's name.
2. Whether `dice-to-seed` should refuse a second seed while a roll log is present, as an issue
   on that repository.
3. Whether the framework keeps recommending a BIP-39 passphrase per cosigner, which section 2
   argues for at length in single-seed terms and which interacts with a two-key quorum
   differently.
4. The roll sheet arrives with `dice-to-seed` pull request 33, which is open. The generation
   instructions depend on it landing.
5. Whether to ask for ordinal tick boxes on the roll sheet, so two seed sheets stay apart
   without either becoming identifiable.
