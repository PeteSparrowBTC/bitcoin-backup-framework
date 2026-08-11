# What else is out there

This framework is one answer among many, and the others are worth knowing about
before you commit to this one. This page is a map: what each project is, where
to find it, and how it relates to the choices made here.

**What this page is not.** It is not a review. Except where noted, each entry is
described from the project's own documentation rather than from having run it,
and none of the endorsements or criticisms of any project here are based on an
audit. Treat every line as a pointer to read for yourself, and note that two of
the tools listed were written by the same author as this framework, which is
disclosed on each.

**A word on categories.** People use "backup" for several different jobs, and
projects that sound comparable often are not. Splitting a secret, storing it,
generating it in the first place, and passing it on after death are four
problems, and a tool that solves one usually does not touch the others.

---

## 1. Ways to split a secret

The scheme decides what a "piece" of your backup is and how many you need.

| Scheme | Where | What it is |
| --- | --- | --- |
| **SLIP-39** | [github.com/satoshilabs/slips](https://github.com/satoshilabs/slips/blob/master/slip-0039.md) | Shamir's Secret Sharing with a defined encoding: a threshold of n pieces recovers, fewer reveal nothing. Its own 1,024-word list, so shares are 20 or 33 words and are not BIP-39 phrases. Native in Trezor Model T, Safe 3 and Safe 5. **This framework uses it**, to split the key that encrypts the backup rather than the seed itself ([why](README.md#4-inventory-the-secrets-you-actually-hold)) |
| **SeedXOR** | [seedxor.com](https://seedxor.com/) | Coinkite's scheme, in Coldcard firmware. Splits a seed by XOR rather than by Shamir's polynomials, and each part is itself a valid BIP-39 phrase. The important difference: **it has no threshold.** Every part is required, so it protects against theft and makes loss strictly more likely |
| **codex32** | [github.com/BlockstreamResearch/codex32](https://github.com/BlockstreamResearch/codex32), [secretcodex32.com](https://secretcodex32.com/) | Shamir's Secret Sharing plus a strong error-correcting checksum, designed to be computed **by hand**, with paper wheels called volvelles instead of a computer. Intellectually the most interesting entry here, because it removes the computer from the trusted set entirely. Its own README says it is "currently under construction and far from production-ready", that "no wallets currently support such secrets", and "do not use this scheme with real money" |
| **SSKR** | [github.com/BlockchainCommons/bc-sskr](https://github.com/BlockchainCommons/bc-sskr) | Blockchain Commons' sharding format, used across their SmartCustody material |
| **Multisig** | Bitcoin itself | Not a backup scheme, and frequently proposed instead of one. Several independent keys sign, and no complete secret is ever assembled. It protects the *use* of keys; each key still needs backing up, which is the problem this framework addresses. The two compose ([§11](README.md#11-involving-others-later-the-upgrade-path)) |

## 2. Tools that produce the backup

Software that turns a seed into the artifacts you store.

| Tool | Where | What it is |
| --- | --- | --- |
| **slip39-backup** | [github.com/PeteSparrowBTC/slip39-backup](https://github.com/PeteSparrowBTC/slip39-backup) | The tool this framework uses. Encrypts seed, passphrase, descriptor and notes into one file, and splits only the key. MIT. *Written by this framework's author* |
| **Superbacked** | [superbacked.com](https://superbacked.com/) | Desktop app by Sun Knudsen. Shamir shares rendered as encrypted QR codes. Source is published, and its licence permits personal use while prohibiting redistribution, so it is readable but not forkable. Offers plausible deniability through a second passphrase that opens a decoy, which the tool used here does not |
| **Hyperbacked** | [github.com/Twometer/hyperbacked](https://github.com/Twometer/hyperbacked) | An open reimplementation of the same idea in Rust, MIT licensed, producing encrypted QR codes in a PDF |
| **seQRets** | [seqrets.app](https://seqrets.app/) | Encrypts then splits, with each share as a scannable QR code. Validates BIP-39 phrases and SLIP-39 shares. Not examined closely enough here to compare fairly |

## 3. Devices that generate the seed

Relevant because a backup cannot be stronger than the secret it preserves
([§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting)), and
because several of these carry backup features of their own.

| Device | Where | Notes |
| --- | --- | --- |
| **Krux** | [selfcustody.github.io/krux](https://selfcustody.github.io/krux/) | Open-source firmware that turns off-the-shelf Kendryte K210 boards (Maix Amigo, M5StickV and others) into an offline signer. Note the category: it is a **signing device, not a backup framework**, though it carries backup-adjacent features including encrypted mnemonic storage and a mnemonic XOR similar to SeedXOR. Entropy from camera, words, D6 or D20. Its d6 handling is the reference point this guide's dice arithmetic was checked against |
| **SeedSigner** | [seedsigner.com](https://seedsigner.com/) | Air-gapped, camera-based, built from commodity parts. Dice entropy built in |
| **Coldcard** | [coldcard.com](https://coldcard.com/) | Coinkite's dedicated signer. Dice entropy, SeedXOR. Also the subject of the 2026 defect that [§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting) is built around |
| **Blockstream Jade** | [blockstream.com/jade](https://blockstream.com/jade/) | Open-source hardware signer |
| **Trezor** | [trezor.io](https://trezor.io/) | The only major vendor with native SLIP-39, which it markets as Shamir Backup |
| **dice-to-seed** | [github.com/PeteSparrowBTC/dice-to-seed](https://github.com/PeteSparrowBTC/dice-to-seed) | Not a device: a converter for checking that a device turned your rolls into the words it should have. *Written by this framework's author* |

## 4. Written protocols and guides

The closest comparisons to this document.

| Guide | Where | What it is |
| --- | --- | --- |
| **Glacier Protocol** | [glacierprotocol.org](https://glacierprotocol.org/) | The most rigorous published cold-storage protocol, at 93 pages, and the reason [§12](README.md#12-what-this-framework-deliberately-does-not-do) treats complexity as its own risk: its own community has noted that most people attempting it are more likely to lose funds than gain security. Largely unmaintained |
| **10x Security Bitcoin Guide** | [btcguide.github.io](https://btcguide.github.io/) | Michael Flaxman's multisig guide, built on the argument that a fault-tolerant setup lets you survive one or more catastrophic mistakes. Where this framework protects the backup of a key, that one removes the single key |
| **SmartCustody** | [smartcustody.com](https://www.smartcustody.com/) | Blockchain Commons. A risk-modelling exercise rather than a recipe: itemise your assets, name your adversaries, then resolve each. The source of the adversary list referenced in [§13](README.md#13-what-we-read-and-what-each-source-changed) |
| **Cryptoasset Inheritance Planning** | Pamela Morgan, book | The standard work on the part this framework deliberately leaves out ([§12](README.md#12-what-this-framework-deliberately-does-not-do)) |

## 5. Inheritance and timelocks

This framework is not an inheritance plan
([§12](README.md#12-what-this-framework-deliberately-does-not-do)). These are
where that problem is actually addressed.

| Approach | Where | What it is |
| --- | --- | --- |
| **Liana** | [wizardsardine.com/liana](https://wizardsardine.com/liana/) | A wallet built on Miniscript spending policies, so a recovery path unlocks after a period of inactivity. Enforced on-chain, with no third party required |
| **Nunchuk** | [nunchuk.io](https://nunchuk.io/) | Multisig and Miniscript, including timelocked inheritance, with the timelock enforced on-chain so it survives the company |
| **Casa**, **Unchained** | [casa.io](https://casa.io/), [unchained.com](https://www.unchained.com/) | Collaborative custody: the provider holds one key of a multisig and participates in inheritance claims. The inheritance logic is run by the provider rather than by the chain, which is the trade to weigh |

## 6. Durable media

Storage is a separate question from the scheme
([§8](README.md#8-storing-the-shares-the-object-and-where-it-goes)): metal
answers durability, never confidentiality.

Jameson Lopp's independent stress tests, cited in
[§13](README.md#13-what-we-read-and-what-each-source-changed), remain the
reference for which products survive fire, crushing and corrosion. Cryptosteel,
Blockplate and similar plate and capsule products are the category.

---

## Where this framework sits

Most of the guides above answer "how do I hold keys safely". This one answers a
narrower question: **given that you already have a secret worth keeping, how do
you back it up so that neither theft nor loss can take it.** That is why it
composes with rather than competes against multisig, and why it says so little
about wallet choice.

The two ideas it does not share with most of this list: the thing that gets
split is a key to an encrypted payload rather than the seed itself, so the
backup can hold a passphrase and a descriptor as well
([§4](README.md#4-inventory-the-secrets-you-actually-hold)); and the setup is
designed to work with zero trusted parties, with other people as a later
upgrade rather than a prerequisite
([§11](README.md#11-involving-others-later-the-upgrade-path)).
