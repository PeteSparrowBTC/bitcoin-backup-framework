# From Zero to a Complete Backup Strategy

A framework for securing a Bitcoin seed phrase, its passphrase, and the digital
accounts around them — written for someone who currently has **no strategy at
all**. It is tool-agnostic in its principles, and uses the
[SLIP-39 + age backup tool](https://github.com/PeteSparrowBTC/Seed-Phrase-Storage-SLIP39)
plus the Bitwarden password manager as the worked example.

> **The one-sentence version:** everything digital hangs off a small physical
> root of trust; nothing online is ever *sufficient* to spend your bitcoin, and
> nothing single is ever *necessary* to recover it.

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

Six rules generate the whole framework. When in doubt, check a decision
against these.

1. **Acyclic dependencies.** No secret may be stored *only* inside something
   it unlocks. (Master password inside the vault: cycle. Email password only
   in a vault whose login requires email verification: cycle.) Draw the "what
   unlocks what" graph; it must have no loops and must terminate in…
2. **A physical root of trust (Layer 0).** Paper and metal in guarded
   locations. This layer depends on *nothing digital* — no device, no
   account, no company staying in business.
3. **Nothing online is sufficient to spend.** A full compromise of any one
   online account or device — password manager included — must yield, at
   worst, ciphertext and privacy leaks, never spendable keys.
4. **Nothing single is necessary to recover.** No single location, device,
   person, memory, or company may be a single point of failure. Redundancy
   for availability; thresholds for confidentiality.
5. **Ciphertext is cheap; keys are precious.** Encrypted blobs
   (`payload.age`, encrypted vault exports) may be replicated promiscuously —
   USB sticks, cloud, an email to yourself. The *keys* to them live only in
   Layer 0 (and your head). Guard few things hard rather than many things
   weakly.
6. **An untested backup is a hypothesis.** Until you have executed the
   recovery end-to-end from the written instructions alone, you do not have a
   backup — you have a plan. Drill it (section 8).

## 3. Inventory — the secrets you actually hold

Before placing anything, list what exists. For a typical self-custody setup:

| # | Secret | Kind | Sufficient to spend BTC? | Where it will live |
|---|---|---|---|---|
| 1 | BIP-39 seed words (+ optional BIP-39 passphrase) | bearer | yes | **only inside `payload.age`** — never stored raw |
| 2 | SLIP-39 shares (protecting random key `k`) | bearer (threshold) | only threshold-many **+** `payload.age` | Layer 0: distributed physical locations |
| 3 | `payload.age` (encrypted wallet payload) | ciphertext | no (useless without `k`) | replicated: vault attachment + offline copies |
| 4 | Wallet descriptor / xpubs | recovery-critical metadata | no (privacy leak only) | inside `payload.age`; copy in vault |
| 5 | Password-manager master password | revocable | no | your head + Layer 0 sheet |
| 6 | Password-manager 2FA recovery code | revocable | no | Layer 0 sheet |
| 7 | Vault-export password | revocable | no | Layer 0 sheet |
| 8 | Email account credentials | revocable | no | vault (cycle broken by #6 — see §6) |

Note what this table achieves: **row 1 never exists in storable form.** The
[SLIP-39 + age tool](https://github.com/PeteSparrowBTC/Seed-Phrase-Storage-SLIP39)
encrypts the seed, passphrase, descriptor, and notes into `payload.age` using
a random 32-byte key `k`, and SLIP-39 splits only `k`. The security boundary
is *possession of threshold-many shares AND the `payload.age` file* — no
single artifact anywhere is sufficient.

## 4. The architecture — three layers

```
 LAYER 0 — PHYSICAL ROOT OF TRUST (depends on nothing)
 ┌───────────────────────────────────────────────────────────────┐
 │  SLIP-39 share zips/mnemonics     Recovery Sheet (×2 copies)  │
 │  3-of-5, five separate locations  • PM master password        │
 │  (paper / metal / trusted hands)  • PM 2FA recovery code      │
 │                                   • vault-export password     │
 │                                   • heir instructions letter  │
 └───────────────┬───────────────────────────┬───────────────────┘
                 │ threshold of shares → k   │ unlocks the account
                 ▼                           ▼
 LAYER 1 — PASSWORD MANAGER (online, zero-knowledge)
 ┌───────────────────────────────────────────────────────────────┐
 │  payload.age (attachment)  ← ciphertext only; k is NOT here   │
 │  verification-record.txt, descriptor copy, all daily logins,  │
 │  email credentials, Emergency Access configured for executor  │
 └───────────────┬───────────────────────────────────────────────┘
                 │ encrypted export + payload.age, refreshed together
                 ▼
 LAYER 2 — OFFLINE REPLICAS (cheap, promiscuous)
 ┌───────────────────────────────────────────────────────────────┐
 │  USB stick(s): encrypted vault export + payload.age copy      │
 │  (safe / bank box; ciphertext everywhere is fine — rule 5)    │
 └───────────────────────────────────────────────────────────────┘
```

Check it against the rules:

- **Vault compromised** (malware, phishing): attacker gets `payload.age`
  (ciphertext), xpubs (privacy leak), and your logins (rotate them). No `k`,
  no coins. Rule 3 holds.
- **Any two share locations burn**: 3-of-5 still recovers `k`. Rule 4 holds.
- **You forget the master password**: Recovery Sheet. Rule 4 holds.
- **Password manager company disappears**: Layer 2 export + `payload.age`
  copy. Rule 4 holds.
- **Recovery Sheet stolen**: attacker can enter the vault → you rotate
  everything in it; still no coins (rule 3 already held). Bad day, not a
  catastrophe — and this is why the sheet lives somewhere you'd *notice* was
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
   password, and one paragraph telling a non-technical reader what this sheet
   is and what to do with it. Make **two copies**, sealed: e.g. home safe +
   bank deposit box (or a trusted relative's safe).
5. Set up **Emergency Access** (Bitwarden Premium): your executor/spouse can
   request access; you get a waiting period to veto. This is your built-in
   dead-man switch.

### Phase B — back up the seed (one Tails session)

6. Download the tool's AppImage and verify its checksum (see the tool's
   [TAILS_INSTRUCTIONS.md](https://github.com/PeteSparrowBTC/Seed-Phrase-Storage-SLIP39/blob/main/TAILS_INSTRUCTIONS.md)).
7. Boot Tails **offline**, run the tool, Owner mode: enter seed words,
   optional BIP-39 passphrase, and — **do not skip this** — the wallet
   descriptor. For multisig, the descriptor is as recovery-critical as the
   seeds. Default 3-of-5 single group is right for most people.
8. From the generated `output.zip`, immediately split the contents:
   - **share zips → five physical homes** (§7 below). Paper is acceptable;
     metal survives fire.
   - **`payload.age` → Bitwarden attachment** in a dedicated entry, together
     with `verification-record.txt`.
   - **`payload.age` → Layer 2 USB stick(s)** as well. Bitwarden's export
     does **not** include attachments (§6), and shares alone cannot recover
     without it — replicate it generously; it is ciphertext.
   - Delete `output.zip`. It is a distribution package, not a keepsake.
9. Before funding the wallet seriously: **dry-run recovery** in Recoverer
   mode with threshold-many shares + `payload.age`, and check the
   verification record. Rule 6.

### Phase C — the heir path (an evening)

10. Write the **heir letter** (stored with each Recovery Sheet copy): what
    exists, where the shares are, that the tool lives at its
    [GitHub repository](https://github.com/PeteSparrowBTC/Seed-Phrase-Storage-SLIP39) /
    on the Layer 2 USB, and the literal steps: *"gather any 3 share zips +
    the file `payload.age` from Bitwarden (use Emergency Access) or the USB
    stick; boot the included AppImage; use Recoverer mode."* Write for the
    least technical person who might have to execute it.
11. Tell your executor the letter exists and where. A perfect system nobody
    knows about fails rule 4 at the human layer.

### Phase D — make it a system, not an event (recurring)

12. Quarterly (or after significant vault changes): refresh the encrypted
    vault export + `payload.age` copy on the Layer 2 USB, *together*.
13. Annually: full recovery drill (§8).

## 6. Known traps (each has bitten real people)

- **Bitwarden exports exclude attachments.** Your vault export does *not*
  contain `payload.age`. Back the file up separately (Phase B step 8) or the
  export gives false confidence.
- **The email ↔ vault cycle.** Without 2FA, Bitwarden's new-device login
  wants an email verification code; if your email password lives only in the
  vault, a fresh machine deadlocks. TOTP 2FA + the printed recovery code
  breaks the cycle — that alone justifies step 2.
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
- **Backups nobody else can operate.** If recovery requires *you* alive and
  remembering, rule 4 is violated at the human layer. The heir letter and
  Emergency Access are as load-bearing as the cryptography.

## 7. Choosing share locations

For 3-of-5, pick five homes such that:

- **No two share a disaster domain** — not all in one building, city block,
  or flood plain. Aim for at least two distinct cities/regions.
- **Any single location being emptied is survivable and noticeable** —
  a share alone reveals nothing, but you want to know it happened.
- **Trusted holders count as locations** (family, lawyer, close friend) —
  tell them it is *one useless-alone piece of a backup*, so they guard it
  without being able to spend, and without panic.
- **You can realistically visit 3 of the 5** within your recovery-time
  tolerance. Recovery latency of days is acceptable; weeks of international
  travel is a design smell.
- Convenient default: home safe, bank deposit box, parent/sibling, lawyer or
  second bank box, close friend in another city.

## 8. The annual drill

Once a year, prove the chain from paper alone — Tails is the ideal venue:

1. Take one Recovery Sheet and a Layer 2 USB. Pretend all your devices are
   gone and your memory is blank.
2. On a clean machine, log into Bitwarden using only the sheet (password +
   2FA recovery code path).
3. Open the vault export with the export password; confirm it is current.
4. Retrieve `payload.age` (from vault attachment *and* confirm the USB copy
   matches).
5. Gather threshold-many shares (rotate which ones each year — this audits
   the locations too) and run Recoverer mode; verify against
   `verification-record.txt`.
6. Read the heir letter as if you were the heir. Fix everything that made
   you hesitate.
7. Reseal, redistribute, note the drill date on the sheet.

Fifteen minutes of drill per year is the difference between a backup and a
belief.

## 9. Failure-mode matrix — what saves you

| Scenario | What saves you |
|---|---|
| Forgotten master password | Recovery Sheet (Layer 0) |
| Lost phone / 2FA device | 2FA recovery code on the sheet |
| House fire destroys home safe + devices | second sheet copy; 3-of-5 tolerates the lost share; cloud vault intact |
| Bitwarden outage / account loss / company failure | Layer 2 export + `payload.age` copy |
| Vault fully compromised (malware, phishing) | rule 3: attacker holds ciphertext + logins → rotate; coins untouched |
| Recovery Sheet stolen | rotate master password, export password, re-secure; coins untouched |
| Two share locations destroyed or share holder dies | threshold margin; re-split to a fresh 3-of-5 when margin thins |
| A share is found by a stranger | reveals nothing alone; re-split at leisure if worried |
| `payload.age` lost everywhere | **unrecoverable — this is the artifact to replicate generously (rule 5)** |
| You die | Emergency Access + heir letter + shares reachable by executor |
| You die *and* the executor is uninformed | nothing — which is why Phase C step 11 is a step |

## 10. What this framework deliberately does not do

- **No brain-only secrets besides the master password.** Memory is a single
  point of failure with a 100% eventual failure rate.
- **No "clever" hiding places** (book pages, freezer, buried caches).
  Obscurity protects until the one renovation, house move, or estate sale
  that doesn't know the secret. Guarded-but-boring beats hidden-and-clever.
- **No custom cryptography.** SLIP-39 for the split, age for the encryption,
  a zero-knowledge password manager for daily secrets. Every component is a
  standard your heirs' future tools will still speak.

---

## License

[MIT](LICENSE)

## Disclaimer

This document describes a strategy, not advice tailored to your situation.
You are solely responsible for your keys and your funds. Test everything
before trusting it with real value.

---

*Collaboration by Claude*
