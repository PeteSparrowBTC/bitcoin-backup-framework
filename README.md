# From Zero to a Complete Backup Strategy: Solo Edition

If you have been meaning to take real custody of your bitcoin for a year or
two and keep postponing it, this document is for you. It is a complete
framework for securing a Bitcoin seed phrase, its passphrase, and the digital
accounts around them, whether you are starting from nothing or already have
a strategy you have never pressure-tested (the rules in [§3](#3-the-rules) and the failure
matrix in [§10](#10-failure-mode-matrix-what-saves-you) work just as well as an audit of an existing setup). It is
written for someone who wants to **trust no one** and does not want to become
a security expert to get this right. If you already use a password manager
and two-factor authentication, you are equipped for everything below.

**This is not an inheritance plan.** It is built for one living individual,
and it trusts no one. That has a price: **by default, if you die, your
bitcoin is lost.** [Phase C](#phase-c-the-access-plan-without-trusting-anyone-an-evening)
leaves your estate a thread to pull (a plan in a
bank box your executor can eventually reach), and [§11](#11-involving-others-later-the-upgrade-path) shows how to upgrade
when you are ready to involve people. Real inheritance planning requires
people and legal instruments; it is a chapter this guide intends to add, not a
question it has closed.

Every step works with zero trusted parties; involving other people is an
optional upgrade layered on at the end ([§11](#11-involving-others-later-the-upgrade-path)), never a prerequisite. The
principles are tool-agnostic; the worked example uses the
[SLIP-39 + age backup tool](https://github.com/PeteSparrowBTC/slip39-backup)
plus the Bitwarden password manager.

> **The one-sentence version:** everything digital hangs off a small physical
> root of trust that only you control; nothing online is ever *sufficient* to
> spend your bitcoin, and nothing single is ever *necessary* to recover it.

**About this document.** It is an open collaboration between a human,
**Pete Sparrow**, and an AI, **Claude** (Anthropic's Fable model). The
framework emerged from a long working conversation between the two.
Before settling on the design, we
reviewed the established books, papers, protocols, and sites on self-custody
and inheritance planning, and where the literature pushed back on our
choices, we changed them. [§13](#13-what-we-read-and-what-each-source-changed) lists each source and what it contributed or
challenged.

---

## 1. What you are protecting, and the two ways you lose

Every secret you hold can fail in exactly two directions:

| Failure direction | Example | Who wins |
|---|---|---|
| **Theft** (someone else gets it) | burglar finds seed words in a drawer; malware reads your unlocked vault | the attacker |
| **Loss** (nobody gets it, including you) | house fire; forgotten password; you die and nobody can decode your system | entropy |

Most people defend hard against theft and then lose everything to loss.
**Loss is the more common failure.** A good framework defends both directions
at once, and every design decision below is justified against one or the other.

Secrets also differ in *kind*, and the kind dictates the protection:

- **Bearer secrets**: whoever holds it owns the asset, irrevocably.
  A BIP-39 seed (the 12/24 words behind your wallet) is the canonical
  example. There is no "reset password" for a drained wallet. These justify
  heavy machinery: threshold splitting, geographic distribution, metal
  storage.
- **Revocable secrets**: a leak is bad but survivable; you can rotate it.
  A password-manager master password (with 2FA on the account) is revocable.
  These deserve *simple, recoverable* backups; the enemy is forgetting, not
  finding.

Applying bearer-grade machinery to revocable secrets makes them harder to
recover for no real gain. Applying revocable-grade carelessness to bearer
secrets is how coins get stolen. Match the protection to the kind.

## 2. Before you back it up: is the secret worth protecting?

A backup preserves a secret exactly as strong as it was the moment it was
created. It cannot add strength that was never there. Perfect discipline
applied to a weak secret gives you a weakness that is faithfully copied,
distributed across three locations, and drilled once a year.

There is an asymmetry here worth stating before anything else. **You cannot
look at a seed and tell whether it is random.** A seed built from 40 bits of
entropy looks exactly like one built from 128: twenty-four ordinary words,
valid checksum, imports fine everywhere. Randomness is a property of the
process that produced the words, never of the words themselves, and no
inspection, checksum or test transaction will reveal the difference. **A
passphrase is the opposite.** You know how it was chosen, because you chose
it, and that makes its weakness measurable. So the two halves of this section
ask different questions: for the seed, was the process trustworthy; for the
passphrase, is this particular string strong.

### The seed: you can only audit the process

Why this matters is not hypothetical. In July 2026 Coinkite disclosed that a
build regression dating to March 2021 had stopped its hardware wallets from
calling their hardware random number generator during seed creation, falling
back to a weak software source with no visible sign. Seeds made on affected
Mk2 and Mk3 devices carry roughly 40 bits of entropy instead of the intended
128, and Mk4, Mk5 and Q seeds roughly 72. Attackers drained about 1,816 BTC
from more than 5,200 addresses. Every one of those owners could have followed
every rule in this document and still lost everything, because the defect was
in the secret and not in its storage. Firmware updates corrected future seed
generation and did nothing at all for seeds already made. No owner could have
detected it by examining their words.

Since the output tells you nothing, only the process is auditable:

- **Supply your own randomness.** Every device worth using lets you mix in
  dice. At least 50 fair, private, independent rolls get hashed directly into
  the seed, bypassing the device generator. This is the only path that does
  not require trusting a black box you cannot inspect, and it is exactly what
  separated a non-event from a loss in July 2026.
- **Know what verification does and does not prove.** Checking the wallet
  fingerprint in independent software, confirming a receive address on a
  second device, and sending a small test transaction all catch a swapped,
  counterfeit or lying device. **None of them detect weak entropy**, because a
  weak seed derives addresses perfectly correctly. Do them anyway; just do not
  read a passing check as evidence of randomness.
- **In multisig, diversify vendors.** A 2-of-3 built from two devices by the
  same maker is not protected against that maker's defect: one flaw satisfies
  the threshold alone. Different vendors for different cosigners is the point,
  and it is the specific lesson of the Coldcard event.
- **Rotate on disclosure, before you protect.** When a defect affecting your
  device and firmware is announced, treat the seed as compromised and move the
  coins before building backups around it. Rule 7 is why: superseded shares
  plus a superseded `payload.age` stay a working backup forever, so
  distributing first means travelling to every location later to destroy what
  you left there.

### The passphrase: strength you can actually assess

BIP-39 turns your words and your passphrase into a wallet using
PBKDF2-HMAC-SHA512 with **2,048 iterations**. That number is the entire work
factor protecting the passphrase, and it is small. A password manager uses
something like 600,000 iterations, or Argon2id, for the same job. Each BIP-39
guess costs roughly 4,000 SHA-512 compressions, so one modern GPU tries on the
order of a million candidates per second and a small rack tries hundreds of
millions. Any passphrase a person invented and can recall unaided sits inside
that range.

**Why `Barcelona2019!` is not a good passphrase.** Three separate reasons, any
one of which is enough:

1. **It is a pattern, not a secret.** Capitalised word, four-digit year,
   trailing punctuation is among the first rule sets a cracking tool applies
   to a wordlist. The capital and the `!` contribute about two bits between
   them, not the complexity their shape suggests.
2. **It is biography.** If Barcelona and 2019 mean something to you, they mean
   something to anyone who reads your social media. Targeted attacks begin by
   building a wordlist from your life: cities, years, pets, children, teams,
   streets.
3. **It is small.** Well under 30 bits against a rule-based attacker, which at
   the speeds above is seconds of work once the mnemonic is known.

The instinct it satisfies, one capital and one number and one symbol, was
built for 1990s login policies where an attacker got three tries before
lockout. Offline cracking with your seed words in hand has no attempt limit.

**What a good passphrase looks like:**

- **Generated, never invented.** Dice or a password manager's generator.
  Human choice is the vulnerability, and it is the one part of this you can
  fully control.
- **Sized to its job.** If you treat the passphrase as the thing that saves
  you when the seed leaks, it must be as strong as the seed: about ten
  diceware words, or twenty-plus random characters. If seed storage is sound
  and the passphrase is a genuine second factor, five to six diceware words is
  defensible.
- **Written down, stored apart from the seed.** Memory-only is total loss with
  no recovery path, and storing it beside the seed defeats its purpose. In
  this framework it lives inside `payload.age` while the shares live
  elsewhere, which separates them by construction.
- **Plain ASCII, no leading or trailing spaces.** Wallets differ in unicode
  normalisation, and a passphrase that recovers on one wallet but not another
  is a live loss risk.
- **Tested before funding.** There is no wrong-passphrase error. Every
  passphrase is valid and opens a different, empty wallet. A typo does not
  look like a typo; it looks like your coins are gone.

### One seed, several passphrases

Reusing one mnemonic with different passphrases, to run several wallets or,
worse, to stand up several cosigners of one multisig, looks like it multiplies
security. It does not. The risk vectors:

1. **A single root.** The mnemonic is the common ancestor of every derived
   wallet. Anything that exposes it, a weak generator, a photographed card, a
   cloud sync, one burgled location, degrades all of them in the same instant.
   Independent wallets fail one at a time; these fail together.
2. **The searches are independent, so costs add rather than multiply.** Given
   the mnemonic and one cosigner's public key, an attacker tests candidate
   passphrases against that key alone. Ordinary use hands them those keys:
   spending from a multisig publishes the cosigner public keys on chain, and
   the descriptor sits in every backup and every watch-only wallet.
3. **Multisig in form, single-sig in risk.** A quorum's value comes from its
   keys being independent. Derive them from one seed and a single compromise,
   plus a fast key-derivation function, reaches all of them.
4. **The backup collapses too.** One `payload.age` then holds the seed and
   every passphrase, so whoever opens it holds the whole quorum. The multisig
   buys nothing at backup time.
5. **Operational confusion.** Which passphrase belongs to which wallet, with
   no error shown on a wrong entry, is a durable way to lose funds with no
   attacker involved at all.

**The specific case: same seed, 2-of-2, `Barcelona2019!` and `Cat2025`.**

If the mnemonic never leaks, both wallets rest on the mnemonic, and the
passphrases are not doing the work you imagine. If the mnemonic does leak,
which is the exact scenario passphrases exist for, the attacker needs both
keys, tests each passphrase separately against its own public key, and pays
the *sum* of the two costs. Sums are dominated by their largest term.
Generously calling `Barcelona2019!` 25 bits and `Cat2025` 20 bits, the pair is
worth log2(2^25 + 2^20), or about 25 bits: **the 2-of-2 is worth roughly what
its stronger passphrase is worth alone.** The second passphrase bought a
rounding error, and 2^25 guesses is a few seconds of GPU time.

Even in the attacker's worst case, where the public keys are somehow unknown
and the search really is multiplicative, 45 bits is hours on rented hardware.

What helps is what this section keeps returning to: two independently
generated seeds, on devices from different vendors, each with its own
generated passphrase if you want one. Then an attacker has to succeed twice,
against unrelated roots, with no shortcut from one to the other.

This section is a precondition check, not a hardware guide. Which device to
buy, and how each handles dice entropy, changes faster than this document can
track; [§13](#13-what-we-read-and-what-each-source-changed) lists sources that
maintain that material properly.

## 3. The rules

One precondition and eight rules generate the whole framework. When in doubt,
check a decision against these.

**Rule 0, the precondition: a backup cannot be stronger than the secret it
preserves.** Audit how the seed was generated and how strong the passphrase
is before investing in protecting them
([§2](#2-before-you-back-it-up-is-the-secret-worth-protecting)). Everything
below assumes real entropy at the root.

1. **Acyclic dependencies**: no loops in "what unlocks what." No secret may
   be stored *only* inside something it unlocks. (Master password inside the
   vault: loop. Email password only in a vault whose login requires email
   verification: loop.) Draw the graph; it must terminate in…
2. **A physical root of trust (Layer 0).** Paper in guarded locations. This
   layer depends on *nothing digital*: no device, no account, no company
   staying in business. Why paper and not a USB stick or a hardened phone?
   Because anything digital either is encrypted (then its key needs a home,
   and the problem starts over) or is not (then it is strictly worse than
   paper: silently copyable and readable by any finder). Paper is readable
   with eyes: no password, no electricity, no surviving software, no flash
   memory fading in a drawer. That property is what lets it sit at
   the *root* of the graph.
3. **Nothing online is sufficient to spend.** A full compromise of any one
   online account or device (password manager included) must yield, at
   worst, encrypted files and privacy leaks, never spendable keys.
4. **Nothing single is necessary to recover.** No single location, device,
   memory, or company may be a single point of failure. Redundancy for
   availability; thresholds for confidentiality.
5. **Ciphertext is cheap; keys are precious.** Encrypted blobs
   (`payload.age`, encrypted vault exports) may be replicated freely:
   USB sticks, cloud, an email to yourself. The *keys* to them live only in
   Layer 0 (and your head). Guard few things hard rather than many things
   weakly.
6. **An untested backup is a hypothesis.** Until you have executed the
   recovery end-to-end from the written instructions alone, you do not have a
   backup, only a plan. Drill it ([section 9](#9-the-annual-drill)). In a solo system this
   matters double: you are the only error-detection there is.
7. **Trust is additive, never foundational.** The system must be fully
   functional with zero trusted parties. Every grant of trust is a later,
   revocable enhancement ([§11](#11-involving-others-later-the-upgrade-path)). Never distribute artifacts of an undrilled
   system: superseded shares plus a superseded `payload.age` remain a
   working backup forever.
8. **Secrets are reconstructed only in the clean room.** The one moment your
   seed exists in one place is recovery. Do it only in the same offline,
   leave-no-trace environment used to create the backup (Tails Linux on a
   spare computer), never on a daily-use machine. This rule exists because
   the published criticism of share-based backups ([§13](#13-what-we-read-and-what-each-source-changed)) is precisely that
   the reconstruction moment is where malware wins; a clean room removes
   that moment from the reach of malware entirely.

## 4. Inventory: the secrets you actually hold

Before placing anything, list what exists. For a typical self-custody setup:

| # | Secret | Kind | Sufficient to spend BTC? | Where it will live |
|---|---|---|---|---|
| 1 | BIP-39 seed words (+ optional BIP-39 passphrase) | bearer | yes | **only inside `payload.age`**, never stored raw |
| 2 | SLIP-39 shares (protecting random key `k`) | bearer (threshold) | only threshold-many **+** `payload.age` | Layer 0: separate locations you alone control |
| 3 | `payload.age` (encrypted wallet payload) | ciphertext | no (useless without `k`) | replicated: vault attachment + offline copies |
| 4 | Wallet descriptor / xpubs | recovery-critical metadata | no (privacy leak only) | inside `payload.age`; copy in vault |
| 5 | Password-manager master password | revocable | no | your head + Layer 0 sheet |
| 6 | Password-manager 2FA recovery code | revocable | no | Layer 0 sheet |
| 7 | Vault-export password | revocable | no | Layer 0 sheet |
| 8 | Email account credentials | revocable | no | vault (cycle broken by #6, see [§7](#7-known-traps-each-has-bitten-real-people)) |

Jargon, once: **SLIP-39 shares** are word lists produced by splitting a
secret so that any 2 of 3 (your choice of threshold) can rebuild it and
fewer reveal nothing. A **wallet descriptor** is the small text that tells
wallet software how your wallet derives its addresses. **`payload.age`** is
one encrypted file produced by the backup tool.

Why not simply split the seed words themselves with SLIP-39 and skip the
encryption layer? Because **SLIP-39 alone cannot hold your whole backup**.
It is a secret-*splitting* scheme, not a container: it encodes one short
binary secret (16 or 32 bytes in every interoperable implementation, room
for the seed's own entropy and nothing else), and it has no defined place
for a BIP-39 passphrase, a wallet descriptor, cosigner details, or notes.
Split the seed raw and every one of those still needs a home, which
recreates the original storage problem for pieces that are just as
recovery-critical. This is not a flaw in SLIP-39 (splitting a small secret
is what the standard is for); it is a mismatch that appears when SLIP-39
alone is treated as a complete backup. The two-layer design resolves it:
the small SLIP-39 secret is spent on a random key `k`, and the payload,
which can be any size, travels encrypted under it.

**Why not simply write the seed down?** A seed on paper, or stamped into metal,
is the simplest backup there is, and it recovers in any wallet, forever, with no
software. The case against it comes down to what each additional copy costs you.

A plaintext seed is spend-sufficient by itself, so **every copy is a complete
attack surface**. Redundancy and exposure move together: one copy risks loss, two
copies mean an attacker needs to reach only one of two places, and a third makes
that easier again. You are trading loss-resistance against theft-resistance on
fixed terms, and both failure directions matter
([§1](#1-what-you-are-protecting-and-the-two-ways-you-lose)).

The encrypted design does not abolish that trade; it puts a dial on it. A share
reveals nothing and a payload without its key reveals nothing, so an attacker
needs threshold-many shares **and** the payload: two different classes of
artifact, normally kept in different places. Adding shares while the threshold
stays put does still help an attacker, who needs the same number and now has more
places to take them from. The difference is that the threshold moves too. Going
from 2-of-3 to 3-of-5 survives two lost shares instead of one *and* demands three
compromised locations instead of two: better in both directions at once, paid for
in locations to set up and check rather than in security. A plaintext backup has
no such dial, because its threshold is permanently one.

Two lesser advantages. A plaintext seed announces itself, since a list of
twenty-four words is recognisable to anyone who has heard of bitcoin, which is
what matters for the renovator, the house move, and the estate sale. And it
holds only the seed, leaving the passphrase and descriptor to find homes of
their own, which is the problem described just above.

What plaintext genuinely wins is recovery. BIP-39 words can be typed into
almost any wallet, by almost anyone, decades from now, while SLIP-39 plus age
needs software that speaks both. That cost is real. It is paid down by both
being published standards with several independent implementations, and by the
manual recovery guide included in every bundle, which is exactly why that guide
exists and why a printed copy belongs with your access plan.

**Metal is a medium, not a scheme.** Durability, meaning paper burns and steel
does not, is a separate question from confidentiality. Stamp SLIP-39 shares into
metal and you get both properties at once
([§8](#8-storing-the-shares-the-object-and-where-it-goes)). What this framework avoids is
not metal; it is a readable seed sitting in one place.

Note what this table achieves: **row 1 never exists in storable form.** The
[SLIP-39 + age tool](https://github.com/PeteSparrowBTC/slip39-backup)
encrypts the seed, passphrase, descriptor, and notes into `payload.age` using
a random 32-byte key `k`, and SLIP-39 splits only `k`. The security boundary
is *possession of threshold-many shares AND the `payload.age` file*: no
single artifact anywhere is sufficient. This is also what makes the solo
version workable: even someone who found **every** share would hold only
`k`, never the wallet, without `payload.age`.

## 5. The architecture: three layers

```
 LAYER 0 - PHYSICAL ROOT OF TRUST (depends on nothing, held only by you)
 ┌───────────────────────────────────────────────────────────────┐
 │  SLIP-39 share cards (33 words)   Recovery Sheet (×2 copies)  │
 │  2-of-3, three locations you      • PM master password        │
 │  alone control (home fireproof    • PM 2FA recovery code      │
 │  pouch / bank box / one more)     • vault-export password     │
 │                                   • access plan (bank box)    │
 └───────────────┬───────────────────────────┬───────────────────┘
                 │ threshold of shares → k   │ unlocks the account
                 ▼                           ▼
 LAYER 1 - PASSWORD MANAGER (online, zero-knowledge)
 ┌───────────────────────────────────────────────────────────────┐
 │  payload.age (attachment)  ← ciphertext only; k is NOT here   │
 │  verification-record.txt, descriptor copy, all daily logins,  │
 │  email credentials; Emergency Access dead-man switch (§6.5)   │
 └───────────────┬───────────────────────────────────────────────┘
                 │ encrypted export + payload.age, refreshed together
                 ▼
 LAYER 2 - OFFLINE REPLICAS (cheap, promiscuous)
 ┌───────────────────────────────────────────────────────────────┐
 │  USB stick(s): encrypted vault export + payload.age copy      │
 │  (bank box / home pouch; ciphertext everywhere is fine)       │
 └───────────────────────────────────────────────────────────────┘
```

No home safe is assumed anywhere. The home copy lives in a **fireproof
document pouch** (sold for passports, roughly the price of a restaurant
dinner) among your other papers; the guarded anchor is a **bank
safe-deposit box**, for most people the cheapest "location you alone
control but your estate can eventually reach."

Check the design against the rules:

- **Vault compromised** (malware, phishing): attacker gets `payload.age`
  (ciphertext), xpubs (privacy leak), and your logins (rotate them). No `k`,
  no coins. Rule 3 holds.
- **Any one share location burns**: 2-of-3 still recovers `k`. Rule 4 holds.
- **You forget the master password**: Recovery Sheet. Rule 4 holds.
- **Password manager company disappears**: Layer 2 export + `payload.age`
  copy. Rule 4 holds.
- **Recovery Sheet stolen**: the finder can enter the vault → you rotate
  everything in it; still no coins (rule 3 already held). Bad day, not a
  catastrophe, and why the sheet lives somewhere you would *notice* was
  opened.

## 6. Setup from zero: the ordered checklist

Do these in order; each phase depends on the previous one. None of them
requires more than an afternoon, and the phases can be weeks apart. The
system is useful from [Phase A](#phase-a-establish-the-digital-root-an-afternoon)
onward.

### Phase A: establish the digital root (an afternoon)

1. Create a Bitwarden account (or equivalent zero-knowledge manager) with a
   strong master password you can *type daily*: a 4-5 word random
   passphrase. Daily typing is your memorization mechanism.
2. Enable TOTP 2FA. **Print the 2FA recovery code immediately**; this is the
   most commonly skipped step and the most common lockout cause.
3. Choose a separate vault-export password.
4. Write the **Recovery Sheet**: master password, 2FA recovery code, export
   password, and one paragraph telling a future reader (including future
   *you*) what this sheet is. Make **two copies**, sealed with a signature
   across the flap: one in the bank box, one in the home fireproof pouch.
5. Set up **Emergency Access** (Bitwarden Premium) with a **2-4 week waiting
   period**. Yes, even in a solo framework: this is not "giving someone
   access now." The contact holds nothing usable today. They can only file a
   request, you are notified, and access happens only if you fail to veto
   for the whole waiting period, which is precisely the mechanism working
   when you are in a hospital bed. It is revocable in one click, unilaterally.
   Scope check: it reaches your *vault* (someone can manage your accounts
   and bills), never your coins; `payload.age` without shares is noise. If
   no candidate exists yet, skip and note it as an open item ([§11](#11-involving-others-later-the-upgrade-path)).

### Phase B: back up the seed (one offline session)

6. Download the tool's AppImage and verify its checksum (see the tool's
   [TAILS_INSTRUCTIONS.md](https://github.com/PeteSparrowBTC/slip39-backup/blob/main/TAILS_INSTRUCTIONS.md)).
7. Boot Tails **offline**, run the tool, Owner mode: enter seed words,
   optional BIP-39 passphrase, and (**do not skip this**) the wallet
   descriptor. For multisig, the descriptor is as recovery-critical as the
   seeds. For a solo setup, set the group shape to **2-of-3** (the tool
   defaults to 3-of-5, which assumes five homes; three locations you alone
   control is realistic, five rarely is).
8. From the generated `output.zip`, immediately split the contents:
   - **shares → three self-controlled homes** ([§8](#8-storing-the-shares-the-object-and-where-it-goes)): copy each
     share's 33 words onto a card *before you leave the offline session*, then
     place the cards: home pouch, bank box, and one more that is yours rather
     than borrowed. **One location, one card**, and [§8](#8-storing-the-shares-the-object-and-where-it-goes)
     has the full list of homes, including the ones to avoid. The zips are
     transport; the cards are the backup.
   - **`payload.age` → Bitwarden attachment** in a dedicated entry, together
     with `verification-record.txt`.
   - **`payload.age` → Layer 2 USB stick(s)** as well. Bitwarden's export
     does **not** include attachments ([§7](#7-known-traps-each-has-bitten-real-people)), and shares alone cannot recover
     without it. Replicate it generously; it is ciphertext.
   - Delete `output.zip`. It is a distribution package, not a keepsake.
9. Before funding the wallet seriously: **dry-run recovery** in Recoverer
   mode with threshold-many shares + `payload.age`, and check the
   verification record. Rules 6 and 8: the dry run happens on Tails too.

### Phase C: the access plan, without trusting anyone (an evening)

10. Write the **access plan** and put it **in the bank box**. This is more
    than a note about the coins; it is the document that answers the fear
    every parent holding bitcoin has: *"if I'm gone, my family has no idea
    what a seed phrase is."* It contains:
    - **An inventory**: this wallet, but also exchange accounts, other
      digital assets, and where the password vault is: everything a
      survivor would otherwise never find.
    - **The recovery steps, written for a smart but non-technical reader**
      (your spouse, your kids' guardian): *"gather any 2 of the 3 share
      envelopes (locations listed below) + the file `payload.age` from
      Bitwarden (via Emergency Access) or the USB stick in this box; start
      the included AppImage on the offline computer; use Recoverer mode;
      take this to a professional if you get stuck; the envelopes alone
      are worthless to a thief, so showing them to a helper is safe."*
    - **Who can help**, in what order: a named tech-comfortable friend, a
      lawyer, a reputable recovery service, so the reader is never alone
      with a puzzle.
    - **A date, and a promise to re-date it.** Update it on life events:
      move, new wallet, marriage or divorce, a location change. A stale
      access plan fails exactly when it is needed.
11. This grants **nothing while you live**; nobody knows the plan exists.
    But a bank box is reachable by your estate's executor through the legal
    process that settles an estate (probate, in many jurisdictions), so the
    plan upgrades "if I die, the coins are gone" to "my estate has a real
    chance." Be clear-eyed about what this is: **a thread for your survivors
    to pull, not an inheritance plan**; it depends on a diligent executor
    finding and following it. Make sure your will mentions **that the box
    exists**: a breadcrumb, never a secret (see the will trap in [§7](#7-known-traps-each-has-bitten-real-people)).

### Phase D: make it a system, not an event (recurring)

12. Quarterly (or after significant vault changes): refresh the encrypted
    vault export + `payload.age` copy on the Layer 2 USB, *together*.
13. Annually: full recovery drill ([§9](#9-the-annual-drill)). Solo systems have no second pair of
    eyes; the drill is the only audit you get.

## 7. Known traps (each has bitten real people)

- **Keys or seeds in the will.** In most jurisdictions a will becomes a
  **public record** when the estate is settled. Anything written in it is
  published. The will gets one breadcrumb ("there is a safe-deposit box at
  [bank]") and never a password, seed word, share, or instruction. The
  access plan lives *in* the box; the will only points at the box.
- **Bitwarden exports exclude attachments.** Your vault export does *not*
  contain `payload.age`. Back the file up separately
  ([Phase B](#phase-b-back-up-the-seed-one-offline-session) step 8) or the
  export gives false confidence.
- **The email ↔ vault cycle.** Without 2FA, Bitwarden's new-device login
  wants an email verification code; if your email password lives only in the
  vault, a fresh machine deadlocks. TOTP 2FA + the printed recovery code
  breaks the cycle; that alone justifies step 2.
- **A digital Layer 0.** A USB stick, a Tails persistent volume, or a
  hardened phone cannot sit at the root: encrypted, the key needs a home and
  the problem starts over; unencrypted, it is worse than paper (rule 2).
  Phones add a correlated failure: the device holding your 2FA recovery is
  usually the 2FA device itself. Digital copies are welcome as
  *supplements*, never as the root.
- **Raw SLIP-39 on the seed words alone.** Splitting the bare seed (as some
  hardware wallets offer) feels complete but is not: the SLIP-39 secret
  carries the seed's entropy and nothing else ([§4](#4-inventory-the-secrets-you-actually-hold)). If your wallet has a
  BIP-39 passphrase, the shares recover a seed that opens the *wrong*
  wallet (an empty one), and the passphrase that opens the right one was
  never in the backup. The passphrase and descriptor end up unprotected,
  co-located with shares, or nowhere. Split a key, encrypt the whole
  payload under it, and the problem disappears.
- **One seed, several passphrases, called multisig.** Deriving several
  cosigners from a single mnemonic produces a quorum that fails as one unit,
  and because each passphrase can be tested against its own public key the
  search costs add instead of multiplying. A 2-of-2 built this way is worth
  about what its stronger passphrase is worth alone
  ([§2](#2-before-you-back-it-up-is-the-secret-worth-protecting)).
- **Splitting the master password with SLIP-39.** Tempting symmetry, wrong
  tool: the master password is a *revocable* secret whose dominant risk is
  forgetting, and SLIP-39 wants a small binary secret, not text. A plaintext
  Recovery Sheet in guarded locations is the proportionate answer ([§1](#1-what-you-are-protecting-and-the-two-ways-you-lose)).
  Save the threshold machinery for the bearer secret.
- **Descriptor amnesia.** Multisig funds behind a lost descriptor can be
  unrecoverable even with every seed in hand. The descriptor belongs inside
  `payload.age` *and* anywhere else convenient; it is not spend-sufficient.
- **Storing the raw seed "just in case" somewhere digital.** The entire
  design collapses if a plaintext copy of row 1 exists in a photo, note, or
  cloud drive. It exists only inside `payload.age`. Ever.
- **Recovering on a daily-use computer.** The reconstruction moment is when
  the whole seed exists in one place; on an everyday machine that is exactly
  where malware waits (rule 8). Recovery happens on offline Tails, full stop.
- **Distributing before drilling.** Old shares + an old `payload.age` are a
  valid backup *forever*. If you hand out artifacts and then redesign, you
  must chase down and destroy every superseded copy. Stabilize solo, drill
  once, then distribute (rule 7).

## 8. Storing the shares: the object, and where it goes

### The object

The tool's output is a distribution package, not a backup. Each
`share-K-of-N.zip` holds one SLIP-39 mnemonic (33 words) and a short read-me.
**The zip is transport; the words are the backup.** Copy the words onto
something physical, then delete the share zips along with `output.zip`
([Phase B](#phase-b-back-up-the-seed-one-offline-session)). A file left on a USB
stick is a storage decision with a shelf life, not the default.

Two ways to get the words out of the offline session:

- **Copy them by hand.** Thirty-three words per share, ninety-nine for a 2-of-3,
  about an hour done carefully. No device joins the trusted set, so rule 8 holds
  without an exception. SLIP-39 words carry a checksum, so a miscopied word is
  refused at recovery rather than silently yielding the wrong key, and the dry
  run (Phase B, step 9) is what proves your copies while it is still cheap to
  find out.
- **Print them, on a printer kept for this.** Faster, and it removes
  transcription risk. The cost is that the printer joins the trusted set:
  connect it by cable, and prefer one with no wireless hardware at all over one
  with wireless switched off. A laser printer retains the last page as a drum
  image and its spool can survive a power cycle, so the printer lives with your
  backups rather than on the office desk.

Not a QR code. This tool emits words on purpose: they can be checked by eye and
stamped into metal, and they do not need a working scanner decades from now.

### What is written on it

Enough for a person who is entitled to it, nothing for a person who is not.

**Write:** the words, numbered; which share this is and how many are needed
("share 2, any 2 of 3 recover"); and **the date it was made**. The date is the
one people leave off and the one that matters. Rule 7 makes superseded shares a
standing hazard, and you visit these locations once a year: an undated card
found in a drawer cannot be told apart from a current one. When you re-split,
the new date is what makes the old cards visibly old, and you still destroy
them.

**Do not write:** any seed word, the BIP-39 passphrase, or where the other
shares live. The last is the one that looks helpful. A card listing all three
locations turns any single compromised location into a map of the whole set, and
gives back the geographic separation the rest of this section buys. Locations
belong in the access plan, in the bank box
([Phase C](#phase-c-the-access-plan-without-trusting-anyone-an-evening)).

Seal each one as the Recovery Sheet is sealed (Phase A, step 4): an envelope,
signature across the flap. That is what turns "each location is tamper-evident"
into a mechanism rather than an intention.

### Media, per location

- **Laser toner, not inkjet, and never thermal receipt paper**, which fades to
  blank within a few years. Handwriting in pencil or a pigment pen outlasts most
  printer ink.
- **The home card faces fire**: fireproof pouch as the minimum, stamped metal as
  the upgrade. Bank-box copies can stay paper, where the climate is stable and
  fire is not the threat.
- **Label the envelope so it survives a house move.** The most common way a
  share dies is not a burglar or a flood; it is someone clearing a drawer who
  has no idea what they are holding. "Important documents, do not discard,
  [your name]" costs nothing and does not say bitcoin.

### The three homes

**One location, one share. Never two.** Two different cards in one envelope,
one drawer, or one deposit box is a spendable quorum sitting in a single
place, and it turns your 2-of-3 into a 1-of-2 while everything still looks
correct from the outside. This is the one error in this section that costs
you the whole design, and it happens by drift rather than by decision: the
bank box already holds the access plan and a Recovery Sheet copy, so it is
the natural place for a second card to end up "for now". Check the box, not
your intentions.

For 2-of-3, pick three homes such that:

- **No two share a disaster domain**: not all in one building or flood
  plain. Home + a bank box across town + an office is a workable minimum;
  a second bank in another city is better.
- **Each is guarded or tamper-evident**: you want to *know* if a location
  was emptied, even though a single share reveals nothing.
- **You can reach two of the three within your recovery-time tolerance.**
  Days of latency is fine (and mild duress protection: nobody can force you
  to produce a quorum in your living room when one share is behind bank
  opening hours). Weeks of travel is a design smell.
- **The anchor location should be estate-reachable.** A bank box is opened
  for your executor through the legal process; a buried cache is not. At
  least the box holding the access plan must have this property.
- **The home share faces fire, not burglars.** A fireproof pouch is the
  minimum; for durability beyond paper, stamped **metal share plates** are
  the upgrade. Independent stress tests (fire, crush, corrosion) of
  commercial products exist ([§13](#13-what-we-read-and-what-each-source-changed)), and the bank-box copies can stay paper.
  Note what goes on the plate: a **SLIP-39 share**, never a plaintext seed.
  Metal answers durability, not confidentiality, and stamping the seed itself
  gives up the property the whole design is built on
  ([§4](#4-inventory-the-secrets-you-actually-hold)).
- Convenient default: home fireproof pouch, bank deposit box (anchor:
  access plan + Recovery Sheet + share), and a third that is yours rather
  than borrowed: a second bank's box, a property you own, or a storage unit
  in your name.

### Where the cards can live

| Location | What it gives you | What it costs |
| --- | --- | --- |
| **Home, fireproof pouch** | The default first home. Cheap, always reachable, and your family finds it, which is a feature | Shares a fire and flood domain with everything else you own, which the pouch is there to answer |
| **Bank deposit box** | The anchor, and the one common option your estate can reach through legal process | Opening hours (also duress protection), typically uninsured contents, drilled if you stop paying, and in some jurisdictions sealed or inventoried at death, which is both how the estate reaches it and why it is slow |
| **Second bank, another city** | The strongest third location: independent disaster domain, guarded, estate-reachable | A trip, and a second annual fee |
| **A property you own** | Holiday home, garage, a rental under your control. Genuinely separate domain, fully yours | Only exists if you have one, and empty properties are burgled more often than occupied ones |
| **Self-storage unit** | In your name, your own padlock as real tamper-evidence, usually reachable at any hour | Miss enough payments and the contents are auctioned, with less warning than a bank gives. Not estate-reachable unless the access plan names it |
| **A relative's or friend's home** | The cheapest independent location most people already have (see below) | Their disasters become yours, and it is the option most likely to lapse when a relationship changes, without anyone deciding that it should |
| **Lawyer, notary, or accountant** | Professional custody, estate-reachable, often free if they already hold your will | Slow to retrieve, and you are trusting an institution to still exist and to still have it |
| **Workplace drawer or pedestal** | Convenient, and separate from home | Not a location you control. Your employer can open it, it offers no tamper-evidence, and it disappears the day you change jobs, leaving a live card in a building you can no longer enter. Rule 7 makes that permanent until you re-split. Treat it as temporary, never as one of the three |
| **Home safe** | Deters an opportunist burglar | Shares the fire domain with the house unless it is genuinely fire-rated, and it advertises that something is worth taking. This framework assumes none |
| **Buried or hidden cache** | Nothing this framework wants | Rejected in [§12](#12-what-this-framework-deliberately-does-not-do): obscurity holds until the one renovation or house move, and no executor will ever find it |
| **Vehicle or boat** | Nothing | Heat, theft, and it moves |
| **Cloud, email, or any online storage** | Nothing worth the cost | It breaks the rule 3 margin. Vault compromise is supposed to yield ciphertext and no coins; a card stored online means an attacker holding your vault has a share *and* `payload.age`, and needs only one more. Replicate the payload online instead, which is what rule 5 is for |

**On a relative's home**, the framework is stricter than its own arithmetic
requires, and it is worth being clear why. Rule 7 says trust is never
foundational, but the security boundary here is threshold-many cards **plus**
`payload.age`, and one sealed card is neither. Handing it to your brother is
not a grant of trust in rule 7's sense, and it becomes one only if he could
ever hold a second card as well. So this option is open to you today. Do not
combine it with making the same person your Emergency Access contact
([Phase A](#phase-a-establish-the-digital-root-an-afternoon), step 5), which
would give one person the payload and a card at once.

### Duplicating a card, or re-splitting

A tempting shortcut: keep the 2-of-3 and store a second copy of one card
somewhere, rather than generating a new split. It is a real option with a
measurable cost, and there is one version of it you should not do.

What duplication does not change is the number of break-ins an attacker
needs, which is still two. What it changes is how many pairs of locations
work, meaning how much choice the attacker has about which two:

| Scheme | Locations | Break-ins for theft | Losses survived | Do the extra copies form a quorum alone? |
| --- | --- | --- | --- | --- |
| 2-of-3, distinct | 3 | 2 | any 1 | no |
| 2-of-3, one card duplicated | 4 | 2 | any 2 but one combination | no |
| 2-of-3, **every** card duplicated | 6 | 2 | any 3 | **yes** |
| 3-of-5, distinct | 5 | 3 | any 2 | no |
| 3-of-6, distinct | 6 | 3 | any 3 | no |

Read the last column first. **Duplicating every card builds a second complete
backup**, because the three spare copies hold one of each between them and
recover the wallet without touching the originals. That would be harmless if
all six locations were equally good, and they never are: your first three are
the best you have, so the spares are by definition the weaker three. You have
made a complete copy of your wallet out of your weakest locations, and an
attacker takes the easy copy while your bank box goes untouched. Duplicating
*one* card does not do this, because someone holding the spare still has to
reach a strong location for a second, different card.

At the same number of locations, re-splitting dominates. 3-of-6 survives the
same three losses as full duplication while demanding three break-ins instead
of two, and leaves no weak subset that recovers on its own. There is no
trade-off to weigh between those two; one is better in every direction.

Against that, keep the count small for a reason that has nothing to do with
attackers. Rule 7 means a superseded card stays a working backup forever, so
every re-split obliges you to visit each location and destroy what is there.
Three locations makes that an afternoon; six makes it a project, projects get
postponed, and old cards stay in circulation, which is the hazard rule 7 names.
The annual drill ([§9](#9-the-annual-drill)) grows the same way.

So, in order of preference:

- **Three good locations: 2-of-3, distinct.** The default, and right for most
  people.
- **A fourth location that is weaker than the others: duplicate one card into
  it**, choosing the card whose location is most likely to be *lost* rather
  than robbed. Bounded cost, real gain, and the pair counts as one location
  when you re-check the disaster-domain and reach-in-time rules above.
- **Five or six locations you would genuinely trust: re-split to 3-of-5 or
  3-of-6.** Better in both directions, and nothing to keep track of.
- **Never duplicate every card**, at any location count.
- **Duplicate `payload.age` freely** before you consider duplicating any card
  at all. It is ciphertext (rule 5), it costs nothing, it adds no theft risk,
  and cards without it recover nothing.

## 9. The annual drill

Once a year, prove the chain from paper alone; offline Tails is the venue
(rule 8):

1. Take the home Recovery Sheet copy and a Layer 2 USB. Assume all your
   devices are gone and your memory is blank.
2. On a clean machine, log into Bitwarden using only the sheet (password +
   2FA recovery code path).
3. Open the vault export with the export password; confirm it is current.
4. Retrieve `payload.age` (from vault attachment *and* confirm the USB copy
   matches).
5. Gather 2 of the 3 shares (rotate which two each year; this audits the
   locations too) and run Recoverer mode on Tails; verify against
   `verification-record.txt`.
6. Read the access plan as if you were the person executing it, ideally
   the least technical person who might have to. Fix everything that made
   you hesitate. (When you eventually involve someone, [§11](#11-involving-others-later-the-upgrade-path), the real test
   is *them* executing it while you watch silently.)
7. Reseal, redistribute, note the drill date on the sheet and the plan.

Fifteen minutes of drill per year is the difference between a backup and a
belief.

## 10. Failure-mode matrix: what saves you

| Scenario | What saves you |
|---|---|
| Your device's random number generator was defective | **nothing in this framework; a perfect backup preserves the flaw.** [§2](#2-before-you-back-it-up-is-the-secret-worth-protecting) is the only defence: your own dice entropy, vendor diversity in multisig, and rotation when a defect is disclosed |
| Forgotten master password | Recovery Sheet (Layer 0) |
| Lost phone / 2FA device | 2FA recovery code on the sheet |
| House fire destroys home pouch + devices | bank-box sheet copy; 2-of-3 tolerates the lost share; cloud vault intact |
| Bitwarden outage / account loss / company failure | Layer 2 export + `payload.age` copy |
| Vault fully compromised (malware, phishing) | rule 3: attacker holds ciphertext + logins → rotate; coins untouched |
| Malware on the machine you recover with | rule 8: you never recover on an online machine, so this scenario is designed out |
| Recovery Sheet stolen | rotate master password, export password, re-secure; coins untouched |
| One share location destroyed | threshold margin; re-split to a fresh 2-of-3 promptly, you are now at zero margin |
| **Two share locations destroyed at once** | **nothing. This is the limit of 2-of-3; geographic separation is what makes it unlikely, and [§11](#11-involving-others-later-the-upgrade-path) is what fixes it properly** |
| A share is found by a stranger | reveals nothing alone (and even all shares yield only `k` without `payload.age`); re-split at leisure |
| `payload.age` lost everywhere | **unrecoverable. This is the artifact to replicate generously (rule 5)** |
| You are incapacitated | Emergency Access (vault: bills, email, accounts) after the waiting period; **coins wait**, no solo mechanism covers them ([§11](#11-involving-others-later-the-upgrade-path)) |
| You die | **by default: the coins are lost.** This framework is not an inheritance plan. The access plan in the bank box gives your estate a chance (a diligent executor, the will breadcrumb, the legal process); [§11](#11-involving-others-later-the-upgrade-path) is the real fix |
| You die and no will mentions the box | nothing; the thread was never tied to anything |

## 11. Involving others later: the upgrade path

The solo framework is complete but has a known coverage boundary: every
scenario where **you are the failed component**. Others are not a nicer
version of what you can do alone; they cover a disjoint set:

1. **Incapacity, for the coins.** Emergency Access covers the vault while
   you are alive-but-unable; nothing solo authorizes anyone to act on the
   wallet. Only a pre-designated person can.
2. **A robust death path.** The legal process plus the access plan works,
   but it is slow and assumes a diligent executor. A person who already
   knows the system exists turns "archaeologically recoverable" into
   "actually recovered."
3. **Duress resistance.** A quorum that physically requires another human
   (or a bank's opening hours) cannot be extracted from you at gunpoint in
   your living room.
4. **Someone knows it exists.** The silent failure of solo systems is being
   perfect and invisible: the fireproof pouch that gets sold with the
   house. One person who merely knows *that* a system exists (not its
   contents) prevents this.

Note the pattern: everything on this list is about scenarios where you are
compromised, which is exactly why the grants feel uncomfortable, and exactly
why they cannot be self-provided. The discomfort and the irreplaceability are
the same property.

When you have the right person (the test: someone you would hand your
unlocked phone), the upgrade is incremental, and nothing already built gets
redone:

- **Name them in Emergency Access** if you skipped step 5, or shorten the
  waiting period you chose.
- **Sign the legal instruments.** A durable power of attorney (the document
  that lets a named person act for you if you cannot; names and forms vary
  by country) is the legal complement to Emergency Access: the technical
  switch covers your vault, the legal one covers everything a vault does
  not. The inheritance-planning literature ([§13](#13-what-we-read-and-what-each-source-changed)) treats this as the
  foundation, not an extra. Keys and seeds still never appear in any legal
  document; those become public.
- **Give them a sealed envelope.** Full Recovery Sheet if the trust is
  there. If not, use the **split variant**: their envelope holds only the
  2FA recovery code + export password. Useless alone, but it completes the
  chain when combined with the estate-reachable bank box. (Cost: the master
  password then exists in only one physical copy plus your memory, a
  conscious loss-resilience trade.)
- **Re-split shares to 3-of-5** and hand one or two shares to holders in
  other cities. Tell them it is one useless-alone piece of a backup, so they
  guard it without being able to spend, and without panic. Collect and
  destroy the superseded 2-of-3 artifacts (rule 7).
- **Have them execute a dry run** of the access plan while you watch and
  say nothing. That, not your own re-reading, is the real test of whether
  the plan works without you (rule 6).
- **Tell your executor the access plan exists.** Existence, not contents:
  minimal disclosure, zero access granted.
- **For large holdings, graduate the wallet itself to multisig.** The
  security literature's strongest criticism of share-based backups ([§13](#13-what-we-read-and-what-each-source-changed)) is
  that shares must be recombined in one place to spend; a multisig wallet
  (e.g. 2-of-3 keys, each on its own hardware, each signing independently)
  never assembles a complete secret anywhere. The two compose cleanly:
  **multisig protects the *use* of keys; this framework protects the
  *backup* of each key.** The backup tool already supports per-cosigner
  seeds and stores the descriptor (which multisig makes truly
  recovery-critical) inside `payload.age`.

Each step is independently revocable and independently useful. Take them in
any order, years apart, as trust arrives.

## 12. What this framework deliberately does not do

- **No brain-only secrets besides the master password.** Memory is a single
  point of failure with a 100% eventual failure rate.
- **No "clever" hiding places** (book pages, freezer, buried caches).
  Obscurity protects until the one renovation, house move, or estate sale
  that doesn't know the secret. Guarded-but-boring beats hidden-and-clever.
- **No custom cryptography.** SLIP-39 for the split, age for the encryption,
  a zero-knowledge password manager for daily secrets. Every component is a
  standard your heirs' future tools will still speak.
- **No maximal-security theater.** The most rigorous published cold-storage
  protocol ([§13](#13-what-we-read-and-what-each-source-changed)) runs 93 pages and its own community notes that most people
  attempting it are *more* likely to lose funds than to gain security.
  Complexity is itself a risk axis; this framework spends its complexity
  budget only where a named failure mode demands it.
- **No claim that solo covers everything.** Death (beyond a thread for your
  estate), incapacity (for the coins), and duress are open items until [§11](#11-involving-others-later-the-upgrade-path),
  written down as open items because a known gap beats a false sense of
  coverage.

## 13. What we read, and what each source changed

This framework was not invented in a vacuum. We reviewed the established
literature (books, protocols, published criticism, and curated research)
and adjusted the design where the evidence pushed back:

- **Pamela Morgan, *Cryptoasset Inheritance Planning: A Simple Guide for
  Owners*** (2018): the standard work on the subject, by an attorney who
  spent years teaching cryptoasset owners. It shaped
  [Phase C](#phase-c-the-access-plan-without-trusting-anyone-an-evening): the heir note
  grew into a full **access plan** (inventory, helpers, dating and update
  triggers), the **keys-never-in-a-will** trap comes from her explanation
  that wills become public records, and the **have-the-reader-execute-the-
  dry-run** test in [§11](#11-involving-others-later-the-upgrade-path) is her method. Her four audit criteria (a plan must
  be *secure, usable, resilient, efficient*) are a good lens for [§9](#9-the-annual-drill).
- **Christopher Allen & Shannon Appelcline, *#SmartCustody*** (Blockchain
  Commons, 2020; free, openly licensed): a risk-modeling method built on
  **27 personified adversaries** ("Death / Incapacitation," "Coercion,"
  "Key Fragility"…). Our failure-mode matrix ([§10](#10-failure-mode-matrix-what-saves-you)) is the compact version of
  their exercise; running your own setup through their full adversary list
  is the recommended graduation from this document.
- **Glacier Protocol** (glacierprotocol.org): the maximal end of
  cold-storage rigor, and the cautionary tale behind [§12](#12-what-this-framework-deliberately-does-not-do). Its own ecosystem
  documents that the 93-page ceremony causes more loss than it prevents for
  non-experts. It validates the offline-Tails instinct while vindicating
  simplicity everywhere else.
- **The published Shamir criticism** ("Shamir Secret Snakeoil," Bitcoin
  Wiki; Casa and Jameson Lopp's writing): the strongest argument *against*
  a design like ours, namely that share-based backups must reconstruct the
  secret in one place. It produced **rule 8** (clean-room-only recovery),
  the explicit framing that reconstruction risk is mitigated rather than
  eliminated, and the **multisig graduation path** in [§11](#11-involving-others-later-the-upgrade-path) (multisig
  protects use; this framework protects backup; compose them).
- **Jameson Lopp's security research** (lopp.net): the field's best
  curated index, and the source of the **metal share plate** guidance in
  [§8](#8-storing-the-shares-the-object-and-where-it-goes). His independent stress tests (fire, crush, corrosion) of commercial
  seed-storage products are the reference when paper stops being enough.
- **The 2026 Coldcard entropy disclosure** (Coinkite's advisory; Wizardsardine's
  technical analysis): a live demonstration that backup discipline cannot
  rescue a secret that was weak at birth. It produced **rule 0** and
  [§2](#2-before-you-back-it-up-is-the-secret-worth-protecting) in full: the
  dice-entropy requirement, the vendor-diversity rule for multisig, the
  distinction between verifying a device and verifying its randomness, and the
  arithmetic showing that one seed with several passphrases adds far less than
  it appears to.

Further reading, in the order we would hand them to a friend: Morgan's book
first (it is written for non-experts and covers the human side), then
#SmartCustody (free PDF) when you want to pressure-test your own setup, then
Lopp's index when you want to go deeper on any single component.

---

## License

[MIT](LICENSE)

## Disclaimer

This document describes a strategy, not advice tailored to your situation.
You are solely responsible for your keys and your funds. Test everything
before trusting it with real value.

---

*Written together by Pete Sparrow (human) and Claude Fable (AI, Anthropic).
The collaboration is stated openly because provenance matters in security
documents: you should know how the thing you are trusting was made.*
