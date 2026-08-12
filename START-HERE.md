# Start here

This is the short version: what to do, in order. Every step links to the
reasoning in [the framework](README.md), and you can ignore those links until
something surprises you. Read this page through once before you begin anything.

**What you end up with.** A wallet whose seed phrase you generated yourself and
can prove was not chosen for you, backed up so that no single place holds enough
to steal it and no single loss destroys it, plus written instructions a
non-technical person could follow.

**What it costs.** Two evenings, a week of errands in between, and about an hour
a year afterwards.

<!-- revision:start -->
**Revised 2026-08-12.** These steps name files and screens in two tools that
change. If that date is old, read the tools' own instructions alongside this
page rather than instead of it.
<!-- revision:end -->

**What it does not do.** It is not an inheritance plan, and by default your coins
are lost when you die. Step 7 leaves your estate a thread to pull, and
[§11](README.md#11-involving-others-later-the-upgrade-path) is the real fix, for
when you are ready to involve people.

---

## Before you start

| | |
| --- | --- |
| **Dice** | One ordinary six-sided die, used for both roll sessions. Casino dice are not needed, and neither is a handful ([why one](NUMBERS.md#why-this-guide-says-one-die)) |
| **Paper and a pen** | Pencil or a pigment pen. Not a thermal printer receipt |
| **A spare computer** | Anything that boots from USB. It never goes online during any of this |
| **Three USB sticks** | One for Tails, and two for payload copies, because one goes in the bank box and one stays home |
| **[Tails](https://tails.net)** | A operating system that runs from the USB stick and forgets everything when you shut down |
| **A password manager** | Bitwarden or equivalent, with two-factor authentication |
| **Three storage places** | Home, a bank deposit box, and one more that is yours rather than borrowed. Pick them now, because step 6 is errands ([which places](README.md#8-storing-the-shares-the-object-and-where-it-goes)) |
| **A fireproof document pouch** | The kind sold for passports |

---

## 1. Download the tools and check them

**Ten minutes, and it is the only step that happens online. Do not skip it and
do not defer it.**

From the releases pages of
[dice-to-seed](https://github.com/PeteSparrowBTC/dice-to-seed/releases) and
[slip39-backup](https://github.com/PeteSparrowBTC/slip39-backup/releases), take
each AppImage and its `SHA256SUMS`, then check what you took:

```bash
sha256sum -c --ignore-missing SHA256SUMS
```

Copy the checked files to a USB stick. You cannot do this later: the machine
that runs them has no network, so there is no way to fetch a checksum once you
are offline.

**Why bother, if it runs offline anyway.** The two answer different questions.
Tails decides whether your seed can get out. The checksum decides whether the
program deriving it is the one that was published. A tampered build needs no
network to hurt you, only words its author can also compute, and an offline
session will run it perfectly faithfully.

---

## 2. Roll the dice, twice

**30 to 45 minutes. You end with two roll logs on paper.**

You are producing randomness you can account for, because you cannot look at a
seed phrase and tell whether it was random
([why this matters](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting)).

1. **Log one, for the seed.** Roll **111** times for a 24-word seed, or **60**
   for 12 words ([where those counts come from](NUMBERS.md#why-99-rolls-is-not-256-bits)).
   Write each digit down as it lands.
2. **Log two, for the backup key.** Roll the same number again, on a **fresh
   log**. This is a different secret and must not reuse log one.

**Why two logs, and why they must not be shared.** The wallet seed is one
secret; the key that encrypts your backup file is another. On a 24-word seed the
seed's entropy *is* the SHA-256 of your rolls, so reusing the same log would make
your backup key derivable from the wallet it is protecting. Both tools defend
this: `dice-to-seed` clears your rolls when you switch modes, and `slip39-backup`
compares the key against your seed and refuses if they match.

**The same die for both logs is correct.** A die has no memory, so two sessions
with one die are two independent sets of rolls, and a second die would add
nothing except a second object whose fairness you have not thought about. What
has to be fresh is the log, not the dice.

**One die, not a handful.** Throwing several at once and reading them in one go
is faster, and it adds a rule: the reading order has to be fixed before the
throw, because an order that depends on what the dice show is not random. The
rule is easy to state and easy to forget at roll eighty, the penalty for
forgetting is invisible in the result, and it grows with the number of dice
([the arithmetic](NUMBERS.md#why-this-guide-says-one-die)). One die has no rule
to forget. The cost is about a quarter of an hour per log.

**Do not re-roll a log because it looks wrong.** Fifty 1s is exactly as likely as
any other fifty rolls, and discarding logs narrows the set your seed is drawn
from. Discard a roll only when the die is cocked or leaves the table, which is a
question about the throw and not about the number.

---

## 3. Convert the rolls, and check the answer

**20 minutes. You end with a seed phrase and a 32-byte key, both confirmed by
two independent tools.**

Boot Tails on the spare computer, **with networking off**.

1. Run [dice-to-seed](https://github.com/PeteSparrowBTC/dice-to-seed) and enter
   log one. It gives you your seed words.
2. Switch to **Rolling for a backup key** and enter log two. It gives you 64 hex
   characters and a four-character check code
   ([why 64, and what the check code is worth](NUMBERS.md#bytes-and-why-a-hex-character-is-half-a-byte)).
3. **Check both against a second implementation.** The conversion is
   deterministic, so any correct tool produces the same answer from the same
   rolls. Two tools agreeing is the proof; which one you ran first does not
   matter. The key is reproducible with one command:
   `printf '%s' "$ROLLS" | sha256sum`.

If two tools disagree, stop and find out why before going further.

---

## 4. Make the backup

**30 minutes, same offline session. You end with three share cards and the
payload file.**

Run [slip39-backup](https://github.com/PeteSparrowBTC/slip39-backup) in Owner
mode ([full instructions](https://github.com/PeteSparrowBTC/slip39-backup/blob/main/TAILS_INSTRUCTIONS.md)).

1. Enter the seed words, your BIP-39 passphrase if you use one, and **the wallet
   descriptor**, which is the text telling wallet software how your addresses
   are derived. Do not skip the descriptor
   ([why](README.md#4-inventory-the-secrets-you-actually-hold)). A passphrase is
   optional here, and if you are inventing one on the spot, do not: it has to be
   generated and it has to be written down somewhere that is not beside the seed
   ([what makes one good](README.md#the-passphrase-strength-you-can-actually-assess)).
2. **Paste the backup key from step 3**, rather than letting the tool generate
   one. Otherwise the key protecting every copy of your backup comes from a
   generator you cannot check.
3. Set the shape to **2-of-3**, meaning three shares of which any two recover.
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
2. **Destroy both roll logs.** Log one *is* your seed in plain text and log two
   *is* your backup key, and until they are burned they are the only unprotected
   copies of either. You have the words and the hex now, and the dry run has just
   proved it ([why this is the trap it is](README.md#7-known-traps-each-has-bitten-real-people)).
3. **Test spend**, once the wallet holds anything. Send a small amount in, then
   send it out again. Receiving proves nothing; spending proves the whole path.

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
| What other people have built | [What else is out there](LANDSCAPE.md) |
| Why dice rather than the device | [§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting) |
| Why encrypt and split, rather than write the seed down | [§4](README.md#4-inventory-the-secrets-you-actually-hold) |
| Where cards go, and why not everywhere | [§8](README.md#8-storing-the-shares-the-object-and-where-it-goes) |
| What actually goes wrong for people | [§7](README.md#7-known-traps-each-has-bitten-real-people) |
| What saves you in each disaster | [§10](README.md#10-failure-mode-matrix-what-saves-you) |
| What this does not cover | [§12](README.md#12-what-this-framework-deliberately-does-not-do) |
| Bringing other people in later | [§11](README.md#11-involving-others-later-the-upgrade-path) |
