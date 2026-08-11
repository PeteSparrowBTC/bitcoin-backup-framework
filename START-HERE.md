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

**What it does not do.** It is not an inheritance plan, and by default your coins
are lost when you die. Step 5 leaves your estate a thread to pull, and
[§11](README.md#11-involving-others-later-the-upgrade-path) is the real fix, for
when you are ready to involve people.

---

## Before you start

| | |
| --- | --- |
| **Dice** | One ordinary six-sided die is enough. Five of them, ideally in five colours, make step 1 about five times faster and add one rule to follow. Casino dice are not needed ([why](https://github.com/PeteSparrowBTC/dice-to-seed#what-you-need)) |
| **Paper and a pen** | Pencil or a pigment pen. Not a thermal printer receipt |
| **A spare computer** | Anything that boots from USB. It never goes online during any of this |
| **Two USB sticks** | One for Tails, one for backup copies |
| **[Tails](https://tails.net)** | A operating system that runs from the USB stick and forgets everything when you shut down |
| **A password manager** | Bitwarden or equivalent, with two-factor authentication |
| **Three storage places** | Home, a bank deposit box, and one more that is yours rather than borrowed. Pick them now, because step 4 is errands ([which places](README.md#8-storing-the-shares-the-object-and-where-it-goes)) |
| **A fireproof document pouch** | The kind sold for passports |

---

## 1. Roll the dice, twice

**30 to 45 minutes. You end with two roll logs on paper.**

You are producing randomness you can account for, because you cannot look at a
seed phrase and tell whether it was random
([why this matters](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting)).

1. **Log one, for the seed.** Roll **111** times for a 24-word seed, or **60**
   for 12 words. Write each digit down as it lands.
2. **Log two, for the backup key.** Roll the same number again, on a **fresh
   log**. This is a different secret and must not reuse log one.

**Why two logs, and why they must not be shared.** The wallet seed is one
secret; the key that encrypts your backup file is another. On a 24-word seed the
seed's entropy *is* the SHA-256 of your rolls, so reusing the same log would make
your backup key derivable from the wallet it is protecting. Both tools defend
this: `dice-to-seed` clears your rolls when you switch modes, and `slip39-backup`
compares the key against your seed and refuses if they match.

**Speed, and the rule that comes with it.** Five dice thrown together turn 111
rolls into 23 throws. That is safe only if you fix the reading order **before**
the first throw: left to right where they land, or five different colours in an
order you have written down. Five dice are five independent rolls in whatever
order you read them, as long as the order does not depend on what they show.

Reading them sorted by value instead, which is the natural thing to do by
accident, throws most of the randomness away. Five dice have 7,776 ordered
outcomes and only 252 unordered ones, so sorting costs about five of the twelve
and a half bits the throw was worth. Discard any throw where a die is cocked or
leaves the table.

One die is the version with no rule to remember, at ten to eighteen minutes per
log instead of two to three.

**Do not re-roll a log because it looks wrong.** Fifty 1s is exactly as likely as
any other fifty rolls, and discarding logs narrows the set your seed is drawn
from.

---

## 2. Convert the rolls, and check the answer

**20 minutes. You end with a seed phrase and a 32-byte key, both confirmed by
two independent tools.**

Boot Tails on the spare computer, **with networking off**.

1. Run [dice-to-seed](https://github.com/PeteSparrowBTC/dice-to-seed) and enter
   log one. It gives you your seed words.
2. Switch to **Rolling for a backup key** and enter log two. It gives you 64 hex
   characters and a four-character check code.
3. **Check both against a second implementation.** The conversion is
   deterministic, so any correct tool produces the same answer from the same
   rolls. Two tools agreeing is the proof; which one you ran first does not
   matter. The key is reproducible with one command:
   `printf '%s' "$ROLLS" | sha256sum`.

If two tools disagree, stop and find out why before going further.

---

## 3. Make the backup

**30 minutes, same offline session. You end with three share cards and the
payload files.**

Run [slip39-backup](https://github.com/PeteSparrowBTC/slip39-backup) in Owner
mode ([full instructions](https://github.com/PeteSparrowBTC/slip39-backup/blob/main/TAILS_INSTRUCTIONS.md)).

1. Enter the seed words, any passphrase, and **the wallet descriptor**, which is
   the text telling wallet software how your addresses are derived. Do not skip
   it ([why](README.md#4-inventory-the-secrets-you-actually-hold)).
2. **Paste the backup key from step 2**, rather than letting the tool generate
   one. Otherwise the key protecting every copy of your backup comes from a
   generator you cannot check.
3. Set the shape to **2-of-3**, meaning three shares of which any two recover.
4. **Write the three share cards.** Each share is 33 words. Print the words and
   the supplied `share-qr.png` together, on a printer that has never been on a
   network, or copy the words by hand. Put on each card: the words, which share
   it is and how many are needed, and **the date**
   ([what goes on a card, and what must not](README.md#8-storing-the-shares-the-object-and-where-it-goes)).
5. **Destroy both roll logs.** Log one *is* your seed in plain text and log two
   *is* your backup key. You have the words and the hex now.
6. Save the payload files, then delete `output.zip`.

---

## 4. Put everything where it goes

**A week of errands. You end with three sealed locations.**

**One location, one card. Never two.** Two cards in one place is a complete
backup sitting in one place.

| What | Where |
| --- | --- |
| Share card 1 | Home, in the fireproof pouch |
| Share card 2 | Bank deposit box |
| Share card 3 | Your third place: another bank, a property you own, a storage unit in your name |
| `payload.age.gpg` | Password manager attachment, in its own entry |
| All payload forms | Both USB sticks. Replicate freely; it is ciphertext |
| At least one payload copy | Somewhere holding no share card |

Seal each card in an envelope with your signature across the flap, so you can
tell if a location was opened. Label it so it survives a house move: "important
documents, do not discard, [your name]", which does not say bitcoin.

[Which places qualify, and which to avoid](README.md#8-storing-the-shares-the-object-and-where-it-goes).

---

## 5. Write the access plan

**An evening. You end with a document in the bank box.**

Written for a smart non-technical reader, such as your partner or your children's
guardian. It contains an inventory of everything you hold, the recovery steps in
plain language, who can help in what order, and a date you promise to refresh
([what to write](README.md#phase-c-the-access-plan-without-trusting-anyone-an-evening)).

This grants nobody anything while you live. Make sure your will mentions **that
the box exists**, which is a breadcrumb and never a secret.

---

## 6. Prove it works

**An hour. Do this before the wallet holds anything you would miss.**

1. **Dry-run recovery** on Tails: gather two share cards plus a payload file, run
   Recoverer mode, and check the result against the verification record.
2. **Test spend.** Send a small amount in, then send it out again. Receiving
   proves nothing; spending proves the whole path.

An untested backup is a plan, not a backup.

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
| Why dice rather than the device | [§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting) |
| Why encrypt and split, rather than write the seed down | [§4](README.md#4-inventory-the-secrets-you-actually-hold) |
| Where cards go, and why not everywhere | [§8](README.md#8-storing-the-shares-the-object-and-where-it-goes) |
| What actually goes wrong for people | [§7](README.md#7-known-traps-each-has-bitten-real-people) |
| What saves you in each disaster | [§10](README.md#10-failure-mode-matrix-what-saves-you) |
| What this does not cover | [§12](README.md#12-what-this-framework-deliberately-does-not-do) |
| Bringing other people in later | [§11](README.md#11-involving-others-later-the-upgrade-path) |
