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
([why](NUMBERS.md#twelve-words-per-cosigner-seed-and-why-that-is-enough)).

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
| **Printed roll sheets** | Two of [`roll-sheet-12-words.pdf`](https://github.com/PeteSparrowBTC/dice-to-seed/releases/latest/download/roll-sheet-12-words.pdf), which has sixty boxes, one sheet per cosigner seed; and one of [`roll-sheet-24-words.pdf`](https://github.com/PeteSparrowBTC/dice-to-seed/releases/latest/download/roll-sheet-24-words.pdf), which has 111, for the backup key. Verified and printed blank before you start, plus a spare of each ([step 1](#1-download-tails-and-the-tools-and-check-what-you-got) covers both) |
| **Value cards** | Blank card stock, one for each value you derive: two cosigner seeds and the backup key, so three, plus a spare, set aside in [step 1](#1-download-tails-and-the-tools-and-check-what-you-got). Not the share cards step 4 makes later |
| **Paper and a pen** | Pencil or a pigment pen. Not a thermal printer receipt |
| **A spare computer** | Anything that boots from USB. It is offline for all of this, and once it has met the seed it never connects to a network again, ever |
| **Three USB sticks** | One for Tails, and two for payload copies, because one goes in the bank box and one stays home |
| **[Tails](https://tails.net)** | An operating system that runs from the USB stick and forgets everything when you shut down. Free, and the one piece of software here that is not optional ([why](README.md#the-clean-room-tails)) |
| **A password manager** | Bitwarden or equivalent, with two-factor authentication |
| **Three storage places** | Home, a bank deposit box, and one more that is yours rather than borrowed. Pick them now, because step 6 is errands ([which places](README.md#8-storing-the-shares-the-object-and-where-it-goes)) |
| **A fireproof document pouch** | The kind sold for passports |

---

## 1. Download Tails and the tools, and check what you got

**This is the only step that happens online.**

**Tails first.** Everything after this happens on it, and it is the one download
here that can be verified properly rather than approximately. Follow
[tails.net/install](https://tails.net/install/), which walks you through writing
the image to a USB stick and then verifies it in the browser, or with an OpenPGP
signature if you would rather. Do the verification. A tampered Tails is a
tampered everything ([what Tails is for, and why nothing else will
do](README.md#the-clean-room-tails)).

**Then the two tools.** From the releases pages of
[dice-to-seed](https://github.com/PeteSparrowBTC/dice-to-seed/releases) and
[slip39-backup](https://github.com/PeteSparrowBTC/slip39-backup/releases), take
everything each release publishes rather than only the app, and copy it onto a
second USB stick. `dice-to-seed` offers a `-tails.zip` that checks itself and
will not open the app if the check fails, so take that one and there is nothing
left for you to do by hand.

**Verify, then print the roll sheets, while a network and a printer are both
easy to reach.** `dice-to-seed` publishes two sheets, straight from its latest
release, and they differ only in how many boxes they carry.
[`roll-sheet-12-words.pdf`](https://github.com/PeteSparrowBTC/dice-to-seed/releases/latest/download/roll-sheet-12-words.pdf) has sixty, which is one cosigner
seed, and you need two of it, because this framework builds its wallet from
two cosigner seeds.
[`roll-sheet-24-words.pdf`](https://github.com/PeteSparrowBTC/dice-to-seed/releases/latest/download/roll-sheet-24-words.pdf) has 111, which is the backup key,
and you need one.
[`SHA256SUMS`](https://github.com/PeteSparrowBTC/dice-to-seed/releases/latest/download/SHA256SUMS) covers both sheets alongside the tools
themselves, so check each one against that checksum before you print anything
from it. Print three sheets in all, plus a spare of each, on this ordinary
networked machine, before you boot Tails. They print blank, so nothing filled
in here ever goes near a printer. The spare computer is offline from step 2
onward and has no printer of its own, so a sheet spoiled at the table cannot
be replaced from there, which is what the spares are for. Set aside a blank
value card for each of the three values, plus a spare, for the same reason.

**The one part that has to happen while you have a network.** Open each release's
build log and confirm that the fingerprint recorded there is the one you are
holding. Every other check works as well later on the offline machine. This one
needs somewhere else to compare against, so it does not
([what each check proves, and what it does not](README.md#phase-b-back-up-the-seed-one-offline-session)).

---

## 2. Roll the dice, and derive each value

**20 to 90 minutes, depending on how many sheets you need. You end with each
value written on its value card.**

Boot Tails on the spare computer, **with networking off**. Everything from
here through step 5 happens in this one offline sitting, other than the test
spend at the end of step 5, which waits for a funded wallet and a different
machine.

You are producing randomness you can account for, because you cannot look at a
seed phrase and tell whether it was random
([why this matters](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting)).

**Which sheets you roll depends on where you joined.** Roll a fresh sixty-box
sheet for each cosigner seed you are generating, and the 111-box sheet for the
backup key. If you already hold both cosigner seeds, bring them written down
into this session and nowhere else, and roll the key sheet alone.

Every sheet follows the same cycle:

1. Roll the number of times the sheet in front of you asks for: **60** for a
   cosigner seed, **111** for the backup key, which derives 64 hex characters
   and a four-character check code instead of words ([where those counts come
   from](NUMBERS.md#why-99-rolls-is-not-256-bits), and [what the hex is
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
3. Derive the value, write it onto its value card, and verify what you wrote
   against the screen too.
4. Clear the log. Do this whether or not another sheet follows; it is also
   what makes the next one safe to roll.

Keep one sheet in front of the machine at a time, and turn any other face
down and out of the way. The value card carries which cosigner is which; the
sheet never does.

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

**If the wallet is not built yet, this is where you wait.** The backup needs
the wallet descriptor and the descriptor needs both cosigner keys, so a reader
who rolled seeds today may have to build the wallet before step 4 can run. Do
step 3 first: checking what you rolled against a second implementation matters
either way. Destroy every sheet you rolled in this sitting regardless, the key
sheet included: a sheet is a secret in plain text whether or not the backup is
finished today. Keep the value cards until the backup is proved, and keep them
apart while they wait, each sealed in its own envelope in a different place.
One card is one cosigner seed and cannot spend by itself; two in one drawer
are the wallet in plain text. Do not fund the wallet beyond pocket change
until the backup exists, and the machine that has held a cosigner seed in
memory still never connects to a network again
([the full version of this pause](README.md#the-pause-between-generating-and-backing-up)).

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
2. **Destroy every roll sheet and every value card this procedure told you
   to write, whichever sitting you wrote it in.** That reaches the cosigner
   cards from a generating sitting days or weeks before this one, not only
   what this sitting itself produced: the payload is the copy that survives
   now, which is exactly why the cards can go. A record of a seed you
   brought from outside this procedure is never touched by any instruction
   on this page; that is the backup-only reader's own paper, and it stays
   theirs. Until burned, everything else here is a seed or the backup key
   in plain text and the only unprotected copy of it, and the dry run has
   just proved the payload is what protects them now
   ([why this is the trap it is](README.md#7-known-traps-each-has-bitten-real-people)).
   This goes further than the pause in step 2, which keeps the value cards
   because the backup does not exist yet. Finishing the backup ends that:
   the payload is what survives from here on.
3. **Retire the spare computer from the network.** It has had your seeds in
   memory, and that is the end of its online life. Shut it down, put it away,
   and do not connect it to anything again
   ([why, given that Tails forgets](README.md#the-clean-room-tails)).
4. **Test spend**, once the wallet holds anything. Send a small amount in, then
   send it out again. Receiving proves nothing; spending proves the whole path.
   This happens on your everyday machine, not the one you just retired.

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
