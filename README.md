# From Zero to a Complete Backup Strategy — Solo Edition

A framework for securing a Bitcoin seed phrase, its passphrase, and the digital
accounts around them — written for someone who currently has **no strategy at
all** and wants to **trust no one**. Every step here works with zero trusted
parties; involving other people is an optional upgrade layered on at the end
(§10), never a prerequisite. The principles are tool-agnostic; the worked
example uses the
[SLIP-39 + age backup tool](https://github.com/PeteSparrowBTC/slip39-backup)
plus the Bitwarden password manager.

> **The one-sentence version:** everything digital hangs off a small physical
> root of trust that only you control; nothing online is ever *sufficient* to
> spend your bitcoin, and nothing single is ever *necessary* to recover it.

---

## 1. What you are protecting, and the two ways you lose

Every secret you hold can fail in exactly two directions:

| Failure direction | Example | Who wins |
|---|---|---|
| **Theft** (someone else gets it) | burglar finds seed words in a drawer; malware reads your unlocked vault | the attacker |
| **Loss** (nobody gets it — including you) | house fire; forgotten password; you die and nobody can decode your system | entropy |

Most people defend hard against theft and then lose everything to loss.
**Loss is the more common failure.** A good framework defends both directions
at once, and every design decision below is justified against one or the other.

Secrets also differ in *kind*, and the kind dictates the protection:

- **Bearer secrets** — whoever holds it owns the asset, irrevocably.
  A BIP-39 seed is the canonical example. There is no "reset password" for a
  drained wallet. These justify heavy machinery: threshold splitting,
  geographic distribution, metal storage.
- **Revocable secrets** — a leak is bad but survivable; you can rotate it.
  A password-manager master password (with 2FA on the account) is revocable.
  These deserve *simple, recoverable* backups — the enemy is forgetting, not
  finding.

Applying bearer-grade machinery to revocable secrets makes them harder to
recover for no real gain. Applying revocable-grade carelessness to bearer
secrets is how coins get stolen. Match the protection to the kind.

## 2. The rules

Seven rules generate the whole framework. When in doubt, check a decision
against these.

1. **Acyclic dependencies.** No secret may be stored *only* inside something
   it unlocks. (Master password inside the vault: cycle. Email password only
   in a vault whose login requires email verification: cycle.) Draw the "what
   unlocks what" graph; it must have no loops and must terminate in…
2. **A physical root of trust (Layer 0).** Paper in guarded locations. This
   layer depends on *nothing digital* — no device, no account, no company
   staying in business. Why paper and not a USB stick or a hardened phone?
   Because anything digital either is encrypted (then its key needs a home,
   and the problem recurses) or is not (then it is strictly worse than
   paper — silently copyable and readable by any finder). Paper is readable
   with eyes: no password, no electricity, no surviving software, no flash
   memory quietly bit-rotting in a drawer. That property is what lets it sit
   at the *root* of the graph.
3. **Nothing online is sufficient to spend.** A full compromise of any one
   online account or device — password manager included — must yield, at
   worst, ciphertext and privacy leaks, never spendable keys.
4. **Nothing single is necessary to recover.** No single location, device,
   memory, or company may be a single point of failure. Redundancy for
   availability; thresholds for confidentiality.
5. **Ciphertext is cheap; keys are precious.** Encrypted blobs
   (`payload.age`, encrypted vault exports) may be replicated promiscuously —
   USB sticks, cloud, an email to yourself. The *keys* to them live only in
   Layer 0 (and your head). Guard few things hard rather than many things
   weakly.
6. **An untested backup is a hypothesis.** Until you have executed the
   recovery end-to-end from the written instructions alone, you do not have a
   backup — you have a plan. Drill it (section 8). In a solo system this
   matters double: you are the only error-detection there is.
7. **Trust is additive, never foundational.** The system must be fully
   functional with zero trusted parties. Every grant of trust is a later,
   revocable enhancement (§10) — and never distribute artifacts of an
   undrilled system, because superseded shares plus a superseded
   `payload.age` remain a working backup forever.

## 3. Inventory — the secrets you actually hold

Before placing anything, list what exists. For a typical self-custody setup:

| # | Secret | Kind | Sufficient to spend BTC? | Where it will live |
|---|---|---|---|---|
| 1 | BIP-39 seed words (+ optional BIP-39 passphrase) | bearer | yes | **only inside `payload.age`** — never stored raw |
| 2 | SLIP-39 shares (protecting random key `k`) | bearer (threshold) | only threshold-many **+** `payload.age` | Layer 0: separate locations you alone control |
| 3 | `payload.age` (encrypted wallet payload) | ciphertext | no (useless without `k`) | replicated: vault attachment + offline copies |
| 4 | Wallet descriptor / xpubs | recovery-critical metadata | no (privacy leak only) | inside `payload.age`; copy in vault |
| 5 | Password-manager master password | revocable | no | your head + Layer 0 sheet |
| 6 | Password-manager 2FA recovery code | revocable | no | Layer 0 sheet |
| 7 | Vault-export password | revocable | no | Layer 0 sheet |
| 8 | Email account credentials | revocable | no | vault (cycle broken by #6 — see §6) |

Note what this table achieves: **row 1 never exists in storable form.** The
[SLIP-39 + age tool](https://github.com/PeteSparrowBTC/slip39-backup)
encrypts the seed, passphrase, descriptor, and notes into `payload.age` using
a random 32-byte key `k`, and SLIP-39 splits only `k`. The security boundary
is *possession of threshold-many shares AND the `payload.age` file* — no
single artifact anywhere is sufficient. This is also what makes the solo
version workable: even someone who found **every** share would hold only
`k`, never the wallet, without `payload.age`.

## 4. The architecture — three layers

```
 LAYER 0 — PHYSICAL ROOT OF TRUST (depends on nothing, held only by you)
 ┌───────────────────────────────────────────────────────────────┐
 │  SLIP-39 share zips/mnemonics     Recovery Sheet (×2 copies)  │
 │  2-of-3, three locations you      • PM master password        │
 │  alone control (home fireproof    • PM 2FA recovery code      │
 │  pouch / bank box / office)       • vault-export password     │
 │                                   • heir letter (bank box)    │
 └───────────────┬───────────────────────────┬───────────────────┘
                 │ threshold of shares → k   │ unlocks the account
                 ▼                           ▼
 LAYER 1 — PASSWORD MANAGER (online, zero-knowledge)
 ┌───────────────────────────────────────────────────────────────┐
 │  payload.age (attachment)  ← ciphertext only; k is NOT here   │
 │  verification-record.txt, descriptor copy, all daily logins,  │
 │  email credentials; Emergency Access dead-man switch (§5.5)   │
 └───────────────┬───────────────────────────────────────────────┘
                 │ encrypted export + payload.age, refreshed together
                 ▼
 LAYER 2 — OFFLINE REPLICAS (cheap, promiscuous)
 ┌───────────────────────────────────────────────────────────────┐
 │  USB stick(s): encrypted vault export + payload.age copy      │
 │  (bank box / home pouch; ciphertext everywhere is fine)       │
 └───────────────────────────────────────────────────────────────┘
```

No home safe is assumed anywhere. The home copy lives in a **fireproof
document pouch** (sold for passports, ~€30) among your other papers; the
guarded anchor is a **bank safe-deposit box** — for most people the cheapest
"location you alone control but your estate can eventually reach."

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
  catastrophe — and why the sheet lives somewhere you would *notice* was
  opened.

## 5. Setup from zero — the ordered checklist

Do these in order; each phase depends on the previous one.

### Phase A — establish the digital root (an afternoon)

1. Create a Bitwarden account (or equivalent zero-knowledge manager) with a
   strong master password you can *type daily* — a 4–5 word random
   passphrase. Daily typing is your memorization mechanism.
2. Enable TOTP 2FA. **Print the 2FA recovery code immediately** — this is the
   most commonly skipped step and the most common lockout cause.
3. Choose a separate vault-export password.
4. Write the **Recovery Sheet**: master password, 2FA recovery code, export
   password, and one paragraph telling a future reader (including future
   *you*) what this sheet is. Make **two copies**, sealed with a signature
   across the flap: one in the bank box, one in the home fireproof pouch.
5. Set up **Emergency Access** (Bitwarden Premium) with a **2–4 week waiting
   period**. Yes, even in a solo framework — this is not "giving someone
   access now." The contact holds nothing usable today: they can only file a
   request, you are notified, and access happens only if you fail to veto
   for the whole waiting period — which is precisely the mechanism working
   when you are in a hospital bed. It is revocable in one click, unilaterally.
   Scope check: it reaches your *vault* (digital caretaker duty), never your
   coins — `payload.age` without shares is noise. If no candidate exists yet,
   skip and note it as an open item (§10).

### Phase B — back up the seed (one Tails session)

6. Download the tool's AppImage and verify its checksum (see the tool's
   [TAILS_INSTRUCTIONS.md](https://github.com/PeteSparrowBTC/slip39-backup/blob/main/TAILS_INSTRUCTIONS.md)).
7. Boot Tails **offline**, run the tool, Owner mode: enter seed words,
   optional BIP-39 passphrase, and — **do not skip this** — the wallet
   descriptor. For multisig, the descriptor is as recovery-critical as the
   seeds. For a solo setup, set the group shape to **2-of-3** (the tool
   defaults to 3-of-5, which assumes five homes; three locations you alone
   control is realistic, five rarely is).
8. From the generated `output.zip`, immediately split the contents:
   - **share zips → three self-controlled homes** (§7): home pouch, bank
     box, one more (second bank's box, locked drawer at work).
   - **`payload.age` → Bitwarden attachment** in a dedicated entry, together
     with `verification-record.txt`.
   - **`payload.age` → Layer 2 USB stick(s)** as well. Bitwarden's export
     does **not** include attachments (§6), and shares alone cannot recover
     without it — replicate it generously; it is ciphertext.
   - Delete `output.zip`. It is a distribution package, not a keepsake.
9. Before funding the wallet seriously: **dry-run recovery** in Recoverer
   mode with threshold-many shares + `payload.age`, and check the
   verification record. Rule 6.

### Phase C — the posthumous path, without trusting anyone (an evening)

10. Write the **heir letter** and put it **in the bank box**: what exists,
    where the three shares are, that the tool lives at its
    [GitHub repository](https://github.com/PeteSparrowBTC/slip39-backup) /
    on the Layer 2 USB, and the literal steps: *"gather any 2 share zips +
    the file `payload.age` from Bitwarden (via Emergency Access) or the USB
    stick; boot the included AppImage; use Recoverer mode."* Write for the
    least technical person who might have to execute it.
11. This grants **nothing while you live** — nobody knows the letter exists.
    But a bank box is reachable by your estate's executor through probate,
    so the letter converts "coins die with me" into "recoverable through the
    legal process." Make sure your will (or wherever your estate starts)
    mentions that the box exists; a breadcrumb, not a secret.

### Phase D — make it a system, not an event (recurring)

12. Quarterly (or after significant vault changes): refresh the encrypted
    vault export + `payload.age` copy on the Layer 2 USB, *together*.
13. Annually: full recovery drill (§8). Solo systems have no second pair of
    eyes; the drill is the only audit you get.

## 6. Known traps (each has bitten real people)

- **Bitwarden exports exclude attachments.** Your vault export does *not*
  contain `payload.age`. Back the file up separately (Phase B step 8) or the
  export gives false confidence.
- **The email ↔ vault cycle.** Without 2FA, Bitwarden's new-device login
  wants an email verification code; if your email password lives only in the
  vault, a fresh machine deadlocks. TOTP 2FA + the printed recovery code
  breaks the cycle — that alone justifies step 2.
- **A digital Layer 0.** A USB stick, a Tails persistent volume, or a
  hardened phone cannot sit at the root: encrypted, the key needs a home and
  the problem recurses; unencrypted, it is worse than paper (rule 2). Phones
  add a correlated failure — the device holding your 2FA recovery is usually
  the 2FA device itself. Digital copies are welcome as *supplements*, never
  as the root.
- **Splitting the master password with SLIP-39.** Tempting symmetry, wrong
  tool: the master password is a *revocable* secret whose dominant risk is
  forgetting, and SLIP-39 wants a 16–32-byte binary secret, not text. A
  plaintext Recovery Sheet in guarded locations is the proportionate answer
  (§1). Save the threshold machinery for the bearer secret.
- **Descriptor amnesia.** Multisig funds behind a lost descriptor can be
  unrecoverable even with every seed in hand. The descriptor belongs inside
  `payload.age` *and* anywhere else convenient — it is not spend-sufficient.
- **Storing the raw seed "just in case" somewhere digital.** The entire
  design collapses if a plaintext copy of row 1 exists in a photo, note, or
  cloud drive. It exists only inside `payload.age`. Ever.
- **Distributing before drilling.** Old shares + an old `payload.age` are a
  valid backup *forever*. If you hand out artifacts and then redesign, you
  must chase down and destroy every superseded copy. Stabilize solo, drill
  once, then distribute (rule 7).

## 7. Choosing locations you alone control

For 2-of-3, pick three homes such that:

- **No two share a disaster domain** — not all in one building or flood
  plain. Home + a bank box across town + an office is a workable minimum;
  a second bank in another city is better.
- **Each is guarded or tamper-evident** — you want to *know* if a location
  was emptied, even though a single share reveals nothing.
- **You can reach two of the three within your recovery-time tolerance.**
  Days of latency is fine (and mild duress protection: nobody can force you
  to produce a quorum in your living room when one share is behind bank
  opening hours). Weeks of travel is a design smell.
- **The anchor location should be estate-reachable.** A bank box is opened
  for your executor through probate; a buried cache is not. At least the
  box holding the heir letter must have this property.
- Convenient default: home fireproof pouch, bank deposit box (anchor: heir
  letter + Recovery Sheet + share), locked drawer or small box at your
  workplace / second bank.

## 8. The annual drill

Once a year, prove the chain from paper alone — Tails is the ideal venue:

1. Take the home Recovery Sheet copy and a Layer 2 USB. Pretend all your
   devices are gone and your memory is blank.
2. On a clean machine, log into Bitwarden using only the sheet (password +
   2FA recovery code path).
3. Open the vault export with the export password; confirm it is current.
4. Retrieve `payload.age` (from vault attachment *and* confirm the USB copy
   matches).
5. Gather 2 of the 3 shares (rotate which two each year — this audits the
   locations too) and run Recoverer mode; verify against
   `verification-record.txt`.
6. Read the heir letter as if you were the executor. Fix everything that
   made you hesitate.
7. Reseal, redistribute, note the drill date on the sheet.

Fifteen minutes of drill per year is the difference between a backup and a
belief.

## 9. Failure-mode matrix — what saves you

| Scenario | What saves you |
|---|---|
| Forgotten master password | Recovery Sheet (Layer 0) |
| Lost phone / 2FA device | 2FA recovery code on the sheet |
| House fire destroys home pouch + devices | bank-box sheet copy; 2-of-3 tolerates the lost share; cloud vault intact |
| Bitwarden outage / account loss / company failure | Layer 2 export + `payload.age` copy |
| Vault fully compromised (malware, phishing) | rule 3: attacker holds ciphertext + logins → rotate; coins untouched |
| Recovery Sheet stolen | rotate master password, export password, re-secure; coins untouched |
| One share location destroyed | threshold margin; re-split to a fresh 2-of-3 promptly — you are now at zero margin |
| **Two share locations destroyed at once** | **nothing — this is 2-of-3's honest limit; geographic separation is what makes it unlikely, and §10 is what fixes it properly** |
| A share is found by a stranger | reveals nothing alone (and even all shares yield only `k` without `payload.age`); re-split at leisure |
| `payload.age` lost everywhere | **unrecoverable — this is the artifact to replicate generously (rule 5)** |
| You are incapacitated | Emergency Access (vault: bills, email, accounts) after the waiting period; **coins wait** — no solo mechanism covers them (§10) |
| You die | heir letter in the bank box, reached through probate; Emergency Access speeds up the vault side |
| You die and no will mentions the box | little — which is why Phase C step 11 is a step |

## 10. Involving others later — the upgrade path

The solo framework is complete but has a known coverage boundary: every
scenario where **you are the failed component**. Others are not a nicer
version of what you can do alone — they cover a disjoint set:

1. **Incapacity, for the coins.** Emergency Access covers the vault while
   you are alive-but-unable; nothing solo authorizes anyone to act on the
   wallet. Only a pre-designated person can.
2. **A robust death path.** Probate-plus-letter works, but it is slow and
   assumes a diligent executor. A person who already knows the system exists
   turns "archaeologically recoverable" into "actually recovered."
3. **Duress resistance.** A quorum that physically requires another human
   (or a bank's opening hours) cannot be extracted from you at gunpoint in
   your living room.
4. **Someone knows it exists.** The quiet failure of solo systems is being
   perfect and invisible — the fireproof pouch that gets sold with the
   house. One person who merely knows *that* a system exists (not its
   contents) prevents this.

Note the pattern: everything on this list is about scenarios where you are
compromised — which is exactly why the grants feel uncomfortable, and exactly
why they cannot be self-provided. The discomfort and the irreplaceability are
the same property.

When you have the right person — the test is someone you would hand your
unlocked phone — the upgrade is incremental, and nothing already built gets
redone:

- **Name them in Emergency Access** if you skipped step 5, or shorten the
  waiting period you chose.
- **Give them a sealed envelope.** Full Recovery Sheet if the trust is
  there. If not, use the **split variant**: their envelope holds only the
  2FA recovery code + export password — useless alone, but it completes the
  chain when combined with the estate-reachable bank box. (Cost: the master
  password then exists in only one physical copy plus your memory — a
  conscious loss-resilience trade.)
- **Re-split shares to 3-of-5** and hand one or two shares to holders in
  other cities. Tell them it is one useless-alone piece of a backup, so they
  guard it without being able to spend — and without panic. Collect and
  destroy the superseded 2-of-3 artifacts (rule 7).
- **Tell your executor the heir letter exists.** Existence, not contents —
  minimal disclosure, zero access granted.

Each step is independently revocable and independently useful. Take them in
any order, years apart, as trust arrives.

## 11. What this framework deliberately does not do

- **No brain-only secrets besides the master password.** Memory is a single
  point of failure with a 100% eventual failure rate.
- **No "clever" hiding places** (book pages, freezer, buried caches).
  Obscurity protects until the one renovation, house move, or estate sale
  that doesn't know the secret. Guarded-but-boring beats hidden-and-clever.
- **No custom cryptography.** SLIP-39 for the split, age for the encryption,
  a zero-knowledge password manager for daily secrets. Every component is a
  standard your heirs' future tools will still speak.
- **No pretending solo covers everything.** Incapacity (for the coins) and
  duress are open items until §10 — written down as open items, because an
  honest gap beats a false sense of coverage.

---

## License

[MIT](LICENSE)

## Disclaimer

This document describes a strategy, not advice tailored to your situation.
You are solely responsible for your keys and your funds. Test everything
before trusting it with real value.

---

*Collaboration by Claude*
