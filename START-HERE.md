# Start here

This is the short version: what to do, in order. Every step links to the
reasoning in [the framework](README.md), so you can follow the plan straight
through, or read the reasoning behind any step. Read this page through once
before you begin anything.

**With seeds you hold, or with seeds you roll here.** Either way this page
ends in the same place: your seeds split across separate locations, so no
single place holds enough to steal your coins and no single loss destroys
them, plus written instructions a non-technical person could follow.

- **You already hold your seeds.** Start at step 1 and skip the seed rolls.
- **You need seeds too.** Roll them here, then carry straight on into the
  backup.

**Two seeds, twelve words each.** The wallet this page builds is 2-of-2 keys,
so it needs two cosigner seeds, and that count is fixed. Twelve words per seed
is enough, and it is the size the roll sheets here are cut to
([why](NUMBERS.md#one-sheet-for-every-secret-and-why-sixty-rolls-is-enough)).

Rolling dice is not a destination on this page. If making a seed is all you
came for, [dice-to-seed](https://github.com/PeteSparrowBTC/dice-to-seed) is the
tool and its own instructions are the guide.

[Which parts you need](ACTIONS.md) names the sheets each route prints and the
steps each one uses.

**What it costs.** Two evenings, a week of errands in between, and about an hour
a year afterwards.

**If a tool and this page disagree, follow the tool.** They are maintained
together, so a renamed file is renamed here in the same release, and a
disagreement means this page is the thing that needs fixing.

---

## Before you start

| | |
| --- | --- |
| **Dice** | One ordinary six-sided die, used for every roll session. Casino dice are not needed, and one is enough ([why one](NUMBERS.md#why-this-guide-says-one-die)) |
| **Printed roll sheets** | Three copies of [`roll-sheet-12-words.pdf`](https://github.com/PeteSparrowBTC/dice-to-seed/releases/latest/download/roll-sheet-12-words.pdf), verified and printed blank before you start, plus a spare. One sheet per secret: two cosigner seeds and the backup key, sixty rolls each ([step 1](#1-download-tails-and-the-tools-and-check-what-you-got) covers the checking) |
| **Paper and a pen** | Pencil or a pigment pen |
| **A spare computer** | Anything that boots from USB. Every Tails session on it runs with networking off, and that never changes once the stick has met a seed. Whatever else the machine boots is its own business ([the limit of that](README.md#the-clean-room-tails)) |
| **Three USB sticks** | One for Tails, and two for payload copies, because one goes in the bank box and one stays home |
| **[Tails](https://tails.net)** | An operating system that runs from the USB stick and forgets everything when you shut down. Free, and the one piece of software here that is not optional ([why](README.md#the-clean-room-tails)) |
| **A password manager** | Bitwarden or equivalent, with two-factor authentication |
| **Three storage places** | Home, a bank deposit box, and one more that is yours rather than borrowed. Pick them now, because step 6 is errands ([which places](README.md#8-storing-the-shares-the-object-and-where-it-goes)) |
| **A fireproof document pouch** | The kind sold for passports |

---

## 1. Download Tails and the tools, and check what you got

**Everything the offline session needs is gathered here.** After this the spare
computer has no network and no printer, so a download you skipped, a checksum
you did not compare or a sheet you did not print cannot be fetched from the
table later.

**Tails first.** The offline session runs on it. Follow
[tails.net/install](https://tails.net/install/), which walks you through writing
the image to a USB stick and then verifies it in your browser. Do the
verification. A tampered Tails is a
tampered everything ([what Tails is for, and why nothing else will
do](README.md#the-clean-room-tails)).

**Then the two tools**, onto a second USB stick. Two files, and the rest of each
releases page is not for you, including the source archives GitHub attaches to
every release.

From [dice-to-seed](https://github.com/PeteSparrowBTC/dice-to-seed/releases),
the `-tails.zip`. It carries the app and checks itself, and it refuses to open
the app if the check fails, so there is nothing left for you to do by hand. The
bare `.AppImage` beside it is the same program without that guard.

From [slip39-backup](https://github.com/PeteSparrowBTC/slip39-backup/releases),
the `.AppImage` and the `.sha256` file beside it. This one has no
self-checking bundle, so you compare the hash yourself once you are on Tails
([its own Tails instructions](https://github.com/PeteSparrowBTC/slip39-backup/blob/main/TAILS_INSTRUCTIONS.md)
carry the command).

**Verify, then print the roll sheets, while a network and a printer are both
easy to reach.** The sheet is
[`roll-sheet-12-words.pdf`](https://github.com/PeteSparrowBTC/dice-to-seed/releases/latest/download/roll-sheet-12-words.pdf), straight from
`dice-to-seed`'s latest release. It has sixty boxes and two purpose ticks at
the top, one for a seed and one for a backup key, which is every secret this
framework rolls ([why sixty covers all three](NUMBERS.md#one-sheet-for-every-secret-and-why-sixty-rolls-is-enough)).
[`SHA256SUMS`](https://github.com/PeteSparrowBTC/dice-to-seed/releases/latest/download/SHA256SUMS) covers it alongside the tools themselves, so
check it against that checksum before you print anything from it. Print three
copies, plus a spare, on this ordinary networked machine, before you boot
Tails. They print blank, so nothing filled in here ever goes near a printer.
The spare computer is offline from step 2 onward and has no printer of its
own, so a sheet spoiled at the table cannot be replaced from there, which is
what the spare is for.

---

## 2. Roll the dice, and hand each value straight to the backup tool

**20 to 90 minutes, depending on how many sheets you need. You end with all
three values in `slip39-backup`'s form and nothing written down.**

Boot Tails on the spare computer, **with networking off**. Everything from
here through step 5 happens in this one offline sitting, other than the test
spend at the end of step 5, which waits for a funded wallet and a different
machine.

**Open both tools before you roll anything.** `dice-to-seed` derives each
value and `slip39-backup` is where it goes, so the receiving field is ready
when the value appears and no value has to survive on paper in between. Each
derived value is shown twice: a single line meant for selecting and pasting,
and the same value grouped for anyone copying it by hand. Use the single
line.

You are producing randomness you can account for, because you cannot look at a
seed phrase and tell whether it was random
([why this matters](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting)).

**Which sheets you roll depends on where you joined.** Roll a fresh sheet for
each cosigner seed you are generating, and one more for the backup key. If you
already hold both cosigner seeds, bring them written down into this session and
nowhere else, and roll the key sheet alone.

Every sheet follows the same cycle:

1. Roll **60** times, filling every box, whether this sheet is a cosigner seed
   or the backup key ([where the count comes
   from](NUMBERS.md#why-99-rolls-is-not-256-bits)). A seed sheet derives twelve
   words; a key sheet derives 64 hex characters and a four-character check code
   ([what the hex is
   worth](NUMBERS.md#bytes-and-why-a-hex-character-is-half-a-byte)). Write
   each throw onto the sheet **as it lands**: not copied off the screen
   afterward, because a sheet is only an independent record of what the dice
   showed if it came from the dice rather than the app.
2. **Compare the sheet against the screen, row by row, before deriving
   anything.** The app shows the rolls in rows of ten, numbered by the
   position of the first roll, and the printed sheet numbers its own rows the
   same way, so this is a row-by-row read rather than a hunt through
   undifferentiated digits. It is the only check in the whole system that can
   catch a mis-press: every other check compares the typed log against
   another conversion of that same typed log
   ([why this matters](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting)).
3. Derive the value and paste it into the field it belongs in: the first seed
   into `slip39-backup`'s cosigner-one field, the second into cosigner two,
   the key and its check code into the backup-key fields.
4. Clear the log. Do this whether or not another sheet follows; it is also
   what makes the next one safe to roll, and it takes the derived value off
   the screen, so paste before you clear.

Keep one sheet in front of the machine at a time, and turn any other face
down and out of the way.

**Why nothing gets written down here.** A hand-copied seed is a transcription
error waiting to be found at recovery, and it is a second plain-text copy of
the words on top of the roll sheet that already holds them. Pasting removes
both. It also settles which cosigner is which, because the label lives in the
field you pasted into rather than on a piece of paper that has to stay with
the right words.

The passphrase is the one value that is typed rather than pasted, and it does
not come from these rolls. It has to be generated, and it belongs in its own
per-cosigner field, never on the same paper as a seed
([what makes one good, and where it lives](README.md#the-passphrase-strength-you-can-actually-assess)).

**Why separate sheets, and why they must not be shared.** Each cosigner seed
is its own secret, and the key that encrypts the backup payload is a third.
A seed's entropy comes straight out of the SHA-256 of your rolls, so
reusing a seed's sheet for the key would make the key derivable from the
wallet it is protecting; both tools defend this, `dice-to-seed` clears your
rolls when you switch modes and `slip39-backup` refuses a key that matches a
seed in the form. Sharing a sheet between the two cosigner seeds is the
sibling mistake and nothing refuses it: the seeds it produces are not
independent, so a 2-of-2 keys wallet built this way fails as one unit instead
of two. Clearing the log after every sheet is what keeps them apart.

**The same die for every sheet is correct.** A die has no memory, so each
sheet's rolls are independent of the others, and a second die would add
nothing except another object whose fairness you have not thought about. What
has to be fresh is the sheet, not the dice
([why one die for every sheet](NUMBERS.md#the-same-die-for-every-sheet)).

**One die, not a handful.** Throwing several at once and reading them in one go
is faster, and it adds a rule: the reading order has to be fixed before the
throw, because an order that depends on what the dice show is not random. The
rule is easy to state and easy to forget at roll eighty, the penalty for
forgetting is invisible in the result, and it grows with the number of dice
([the arithmetic](NUMBERS.md#why-this-guide-says-one-die)). One die has no rule
to forget. The cost is about a quarter of an hour per sheet.

**Do not re-roll a sheet because it looks wrong.** A run of 1s is exactly as
likely as any other sequence of the same length, and discarding a sheet
narrows the set your value is drawn from. Discard a roll only when the die is
cocked or leaves the table, which is a question about the throw and not about
the number.

**Do not start this step unless you can finish the sitting.** Step 4 wants the
wallet descriptor, the descriptor wants both cosigner keys, and the wallet has
to exist by then. Build it in this session with both devices on the table, or
arrive holding the descriptor already. Rolling seeds today and building the
backup next week means the words have to survive the gap on something, and a
piece of paper holding a seed in plain text is the artifact this whole design
exists to remove. Nothing here is urgent enough to be worth that
([why the order is this way](README.md#why-the-wallet-comes-before-the-backup)).

---

## 3. Check the answer

**A few minutes per value. The rolls come back off the sheet, which is not
destroyed yet.**

**Check every derived value against a second implementation.** Read the
rolls back off the sheet and run them through a second tool. The conversion
is deterministic, so any correct tool produces the same answer from the same
rolls, and two tools agreeing is the proof; which one you ran first does not
matter. The key is reproducible with one command:
`printf '%s' "$ROLLS" | sha256sum`.

If two tools disagree, stop and find out why before going further.

---

## 4. Make the backup

**30 minutes, same offline session. You end with three share cards and the
payload file.**

Run [slip39-backup](https://github.com/PeteSparrowBTC/slip39-backup) in Owner
mode ([full instructions](https://github.com/PeteSparrowBTC/slip39-backup/blob/main/TAILS_INSTRUCTIONS.md)).

1. **Leave the top-level seed-words field empty** and enter both cosigner
   seeds' words in the per-cosigner fields beneath it. The top field is there
   for a single-sig or shared-seed backup, and filling it builds a different
   wallet from the one you rolled. Each cosigner has its own passphrase
   field, so enter the BIP-39 passphrase belonging to that seed if it has
   one: a passphrase that does not reach the payload is not backed up, and
   nothing reports that to you later. Then **the wallet descriptor**, which
   is the text telling wallet software how your addresses are derived. Do not
   skip the descriptor
   ([why](README.md#4-inventory-the-secrets-you-actually-hold)). A passphrase
   is optional here, and if you are inventing one on the spot, do not: it has
   to be generated and it has to be written down somewhere that is not beside
   the seed
   ([what makes one good](README.md#the-passphrase-strength-you-can-actually-assess)).
2. **Paste the backup key you rolled**, rather than letting the tool generate
   one. Otherwise the key protecting every copy of your backup comes from a
   generator you cannot check.
3. Set the shape to **2-of-3 cards**, meaning three cards of which any two recover.
4. **Write the three share cards.** Each share is 33 words. Print the words and
   the supplied `share-qr.png` together, on a printer that has never been on a
   network, or copy the words by hand. Put on each card: the words, which share
   it is and how many are needed, and **the date**
   ([what goes on a card, and what must not](README.md#8-storing-the-shares-the-object-and-where-it-goes)).
5. **Keep four things out of `output.zip`, then delete it**: the payload file
   `payload.age.gpg.asc`, `verification-record.txt`, and `MANUAL-RECOVERY.txt`
   and `VERIFY-THIS-BACKUP.txt`. Print the manual once per share location. The
   zip is a distribution package, not a keepsake, but three of those four are
   things you will want years from now and cannot regenerate.

---

## 5. Prove it works, before anything leaves the room

**An hour, still in the same offline session.**

1. **Dry-run the recovery.** Gather two of the three cards you just wrote, plus
   the payload file, run Recoverer mode, and check the result against
   `verification-record.txt`. This is what proves your handwriting as much as it
   proves the tool.
2. **Destroy every roll sheet, all three of them.** A record of a seed you
   brought from outside this procedure is never touched by any instruction
   on this page; that is the backup-only reader's own paper, and it stays
   theirs. The sheets are different: each one is a secret in plain text and
   the only unprotected copy of it, and the dry run has just proved the
   payload is what protects them now
   ([why this is the trap it is](README.md#7-known-traps-each-has-bitten-real-people)).
   Burn them, or shred them and separate the pieces, which is what the
   largest type on each sheet already says.
3. **Shut the session down, and keep the stick offline for good.** Tails
   forgets the seeds when it powers off, so what carries forward is the rule
   rather than the contents: no Tails session on this stick ever gets
   networking, including the restore years from now
   ([why that is the rule, and what it does not cover](README.md#the-clean-room-tails)).
4. **Test spend**, once the wallet holds anything. Send a small amount in, then
   send it out again. Receiving proves nothing; spending proves the whole path.
   This happens on your everyday machine, not in the Tails session you just
   shut down.

**Why this comes before the errands rather than after.** Shares you have already
placed in three locations are a working backup forever. Find a fault after the
week of driving and you are driving it again to collect and destroy what you
left, which is the last trap in
[§7](README.md#7-known-traps-each-has-bitten-real-people). An untested backup is
a plan, not a backup, and it is cheapest to find that out while every card is
still on the table in front of you.

---

## 6. Put everything where it goes

**A week of errands. You end with three sealed locations.**

**One location, one card. Never two.** Two cards in one place is a complete
backup sitting in one place.

| What | Where |
| --- | --- |
| Share card 1 | Home, in the fireproof pouch |
| Share card 2 | Bank deposit box |
| Share card 3 | Your third place: another bank, a property you own, a storage unit in your name |
| A printed `MANUAL-RECOVERY.txt` | In each of the three envelopes, with the card |
| `payload.age.gpg.asc` | Password manager attachment, in its own entry |
| The same file again | Both payload USB sticks: one in the bank box, one in the home pouch. Replicate freely; it is ciphertext behind two locks |
| At least one payload copy | Somewhere holding no share card |
| `verification-record.txt` | The password-manager entry with the payload, and both payload USB sticks: it is what a recovery is checked against, in the annual drill as much as in the dry run |

Seal each card in an envelope with your signature across the flap, so you can
tell if a location was opened. Label it so it survives a house move: "important
documents, do not discard, [your name]", which does not say bitcoin.

[Which places qualify, and which to avoid](README.md#8-storing-the-shares-the-object-and-where-it-goes).

---

## 7. Write the access plan

**An evening. You end with a document in the bank box.**

Written for a smart non-technical reader, such as your partner or your children's
guardian. It contains an inventory of everything you hold, the recovery steps in
plain language, who can help in what order, and a date you promise to refresh
([what to write](README.md#phase-c-the-access-plan-without-trusting-anyone-an-evening)).

This grants nobody anything while you live. Make sure your will mentions **that
the box exists**, which is a breadcrumb and never a secret.

---

## Once a year

Fifteen minutes ([the drill in full](README.md#9-the-annual-drill)):

- Recover from paper alone, on Tails, assuming your devices and memory are gone
- Rotate which two locations you visit, which audits the locations as well
- Read the access plan as the person who would have to execute it
- Re-date the plan and the cards, reseal, redistribute

---

## Where the reasoning lives

| If you want to know | Read |
| --- | --- |
| Why any of this, in one page | [The rules](README.md#3-the-rules) |
| Where every number here comes from | [How the numbers work](NUMBERS.md) |
| What each primitive here guarantees | [How the cryptography works](CRYPTOGRAPHY.md) |
| What other people have built | [What else is out there](LANDSCAPE.md) |
| Why dice rather than the device | [§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting) |
| Why encrypt and split, rather than write the seed down | [§4](README.md#4-inventory-the-secrets-you-actually-hold) |
| Where cards go, and why not everywhere | [§8](README.md#8-storing-the-shares-the-object-and-where-it-goes) |
| What actually goes wrong for people | [§7](README.md#7-known-traps-each-has-bitten-real-people) |
| What saves you in each disaster | [§10](README.md#10-failure-mode-matrix-what-saves-you) |
| What this does not cover | [§12](README.md#12-what-this-framework-deliberately-does-not-do) |
| Bringing other people in later | [§11](README.md#11-involving-others-later-the-upgrade-path) |

<!-- revision:start -->
**Revised 2026-08-28.**
<!-- revision:end -->
