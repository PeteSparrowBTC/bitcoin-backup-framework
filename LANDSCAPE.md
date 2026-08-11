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

**And a word on kinds.** Three different things get compared as though they
were alternatives:

- **A method** teaches you to derive your own answer. It names no products and
  finishes with a decision you made. SmartCustody is the clearest example.
- **A procedure** hands you an answer and expects to be followed in order.
  Glacier, Yeti and this framework are procedures.
- **A tool** is software you run. It decides nothing about your setup.

Most projects are one of these. A few are several, and the useful question
about any of them is which part you are actually short of. If you do not know
whether a 2-of-3 fits your life, no tool will tell you and a procedure will
just answer for you.

**Where this framework sits on that axis:** it is a procedure plus the tools to
execute it, and it is deliberately not a method. It picks the scheme, the
threshold, the media and the locations, and states the reasoning so you can
disagree with a specific choice rather than the whole thing. If what you want
is to derive your own answer from your own threat model, SmartCustody is the
better starting point and this document is one of the things you might arrive
at.

---

## 1. Ways to split a secret

The scheme decides what a "piece" of your backup is and how many you need.

| Scheme | Where | What it is |
| --- | --- | --- |
| **SLIP-39** | [github.com/satoshilabs/slips](https://github.com/satoshilabs/slips/blob/master/slip-0039.md) | Shamir's Secret Sharing with a defined encoding: a threshold of n pieces recovers, fewer reveal nothing. Its own 1,024-word list, so shares are 20 or 33 words and are not BIP-39 phrases. Native in Trezor Model T, Safe 3 and Safe 5. **This framework uses it**, to split the key that encrypts the backup rather than the seed itself ([why](README.md#4-inventory-the-secrets-you-actually-hold)) |
| **SeedXOR** | [seedxor.com](https://seedxor.com/) | Coinkite's scheme, in Coldcard firmware. Splits a seed by XOR rather than by Shamir's polynomials, and each part is itself a valid BIP-39 phrase. The important difference: **it has no threshold.** Every part is required, so it protects against theft and makes loss strictly more likely |
| **codex32** | [github.com/BlockstreamResearch/codex32](https://github.com/BlockstreamResearch/codex32), [secretcodex32.com](https://secretcodex32.com/) | Shamir's Secret Sharing plus a strong error-correcting checksum, designed to be computed **by hand**, with paper wheels called volvelles instead of a computer. Intellectually the most interesting entry here, because it removes the computer from the trusted set entirely. Its own README says it is "currently under construction and far from production-ready", that "no wallets currently support such secrets", and "do not use this scheme with real money" |
| **SSKR** | [developer.blockchaincommons.com/sskr](https://developer.blockchaincommons.com/sskr/) | Blockchain Commons' sharding format, and **the closest relative to this framework's design**, which is worth stating plainly. Their documented construction encrypts the payload with a unique random symmetric key, shards that key, and stores the shares: the same two layers, down to the same cipher family. One difference decides everything downstream, and it is described below |
| **Multisig** | Bitcoin itself | Not a backup scheme, and frequently proposed instead of one. Several independent keys sign, and no complete secret is ever assembled. It protects the *use* of keys; each key still needs backing up, which is the problem this framework addresses. The two compose ([§11](README.md#11-involving-others-later-the-upgrade-path)) |

### Is "encrypt the payload, split the key" an existing design?

Yes, in three separate places, and it is worth laying them side by side because
the differences are where the argument actually is.

| | the key comes from | split with | where the ciphertext lives | to recover you need |
| --- | --- | --- | --- | --- |
| **SLIP-39 on its own** (Trezor) | a passphrase | Shamir, over the encrypted secret | nowhere: the shares *are* the secret | threshold-many shares **and** the passphrase |
| **SSKR + Gordian Envelope** | a random symmetric key | SSKR | inside every envelope, beside a share | threshold-many envelopes |
| **Superbacked**, **Hyperbacked** | a user passphrase, via Argon2 | Shamir (`sss-cli` in Superbacked's case) | inside every block | threshold-many blocks **and** the passphrase |
| **This framework** | a random 32-byte key, no passphrase | SLIP-39 | one separate file, replicated freely | threshold-many shares **and** the payload |

**SLIP-39 already does encrypt-then-split, internally.** Its specification
encrypts the master secret with a passphrase into an Encrypted Master Secret,
and splits *that*. So the shape is inside the standard this framework uses. What
differs is the purpose: SLIP-39's inner layer adds a passphrase factor to the
secret being split, while the layer here adds a **container**, which is what
lets one backup hold a passphrase and a descriptor as well as a seed
([§4](README.md#4-inventory-the-secrets-you-actually-hold)).

**And that inner passphrase is deliberately left empty here**, for a reason the
specification states outright: "passphrases are not validated in any way.
Decrypting an EMS with any passphrase will produce data usable as the Master
Secret, regardless of whether it is the original data or not." A mistyped
SLIP-39 passphrase therefore yields a different, entirely valid-looking wallet
with no error, which is the same silent failure
[§7](README.md#7-known-traps-each-has-bitten-real-people) records for BIP-39
passphrases. This framework already carries one unvalidated passphrase, the
BIP-39 one, and documents the trap it creates. Carrying a second would double
the number of ways to arrive at a valid wallet that is not yours.

**What this survey did not find** is another project combining all three of a
random key rather than a passphrase-derived one, SLIP-39 as the splitting layer,
and the ciphertext kept apart from the shares. That is a statement about what
these searches turned up and not a claim of novelty: the nearest neighbours
above each differ in one axis, and if something combines all three it belongs on
this page.

**SSKR and this framework, and the difference that matters.** Blockchain
Commons builds three envelopes, **each holding the encrypted payload plus one
share** of the key. This framework keeps the payload apart from the shares
entirely.

The consequence is the whole trade. Under their arrangement, threshold-many
envelopes are sufficient: gather two of three and you are done, because each
one already carried the ciphertext. Under this one, threshold-many shares are
*not* sufficient, because the payload is a separate artifact you also have to
hold ([§4](README.md#4-inventory-the-secrets-you-actually-hold)).

Theirs is simpler to recover and has one fewer thing to lose, which is the more
common failure. This one resists a group of share-holders combining against you
and survives a stranger finding every share, and pays for that with a second
artifact that must also survive
([§10](README.md#10-failure-mode-matrix-what-saves-you) lists losing it as
unrecoverable). Neither is the strict improvement, and anyone claiming the
two-layer idea as novel should be pointed at SSKR.

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

The largest category, and the closest comparisons to this document. They differ
in a way worth noticing before you pick one: a **protocol** tells you what to do
in order and expects to be followed, while a **guide** explains a topic and
expects you to decide. Reading a protocol as a guide is how people end up with
half a protocol, which is usually worse than either.

### Step-by-step protocols

| Protocol | Where | What it is |
| --- | --- | --- |
| **Glacier Protocol** | [glacierprotocol.org](https://glacierprotocol.org/) | The most rigorous published cold-storage protocol, at 93 pages: multisig, keys on paper, and eternally quarantined factory-new hardware that never goes online again. It is also the reason [§12](README.md#12-what-this-framework-deliberately-does-not-do) treats complexity as its own risk axis, since its own community has noted that most people attempting it are more likely to lose funds than gain security. Largely unmaintained |
| **CryptoGlacier** | [vogelito.github.io/cryptoglacierdocs](https://vogelito.github.io/cryptoglacierdocs/docs/overview/) | A continuation of Glacier's approach by a different author, for readers who want that protocol with more recent maintenance |
| **Yeti** | [yeticold.com](https://yeticold.com/), [github.com/JWWeatherman/yeticold](https://github.com/JWWeatherman/yeticold) | A script that installs Bitcoin Core and walks you through a multisig cold-storage setup, explicitly preferring safety over ease of use. Notable for a decision this framework shares: recovery instructions are stored **with every copy of the keys**, so the plan cannot be separated from the material it explains |
| **10x Security Bitcoin Guide** | [btcguide.github.io](https://btcguide.github.io/) | Michael Flaxman's multisig guide, built on the argument that a fault-tolerant setup lets you survive one or more catastrophic mistakes. Where this framework protects the backup of a key, that one removes the single key |
| **SmartCustody** | [smartcustody.com](https://www.smartcustody.com/) | Blockchain Commons, and the odd one out here because it is all three kinds at once. A **method**: itemise your assets, name your adversaries, resolve each, across a 186-page book and a 14-step cold-storage scenario, and the source of the adversary list in [§13](README.md#13-what-we-read-and-what-each-source-changed). **Specifications**: SSKR, Gordian Envelope, multisig and timelock patterns. **Software**: [Gordian Seed Tool](https://github.com/BlockchainCommons/GordianSeedTool-iOS) for iOS, plus command-line tools including seedtool, which converts a seed between BIP-39, SSKR, hex and Bytewords. Deliberately not prescriptive: it analyses wallets such as Sparrow and Passport as case studies rather than telling you which to buy. The complement to this document rather than a competitor, and the better place to start if you want to derive your own answer instead of adopting one |

### What SmartCustody actually prescribes

Worth setting out concretely, because it is the nearest methodological relative
and it reaches different answers from this document on both halves of the job.

**Generating the seed: they trust the device, and this framework does not.**
Their Simple Self-Custody Cold Storage Scenario has the seed generated by a
hardware wallet's own random number generator, on the principle that the
recovery phrase "is generated on trusted hardware certified for key creation".
[§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting) is built
on the opposite premise, and on a specific event: a hardware wallet certified for
exactly that purpose shipped a broken generator for five years, and no owner
could detect it by examining their words. Note the dates before treating this as
a disagreement, since that scenario was published in 2019 and the defect was
disclosed in 2026.

Their own tooling has since moved: Gordian Seed Tool accepts coin flips, die
rolls and playing cards, and their material calls dice the quickest of the
three. So the two documents give different answers, and the newer one agrees
with this guide.

**Storing it: their default is whole copies, not shards.** The cold storage
scenario keeps a metal 24-word seed, a paper 24-word seed and a second hardware
wallet in a safety deposit box, with the first device in a home safe. That is
several complete backups in guarded places, which
[§4](README.md#4-inventory-the-secrets-you-actually-hold) declines on the
grounds that every complete copy is another place the whole secret can be taken
from. Their answer is that the places are guarded. Both positions are defensible
and they rest on different estimates of how good your locations are.

They do offer an optional split of the 24 words across three metal tiles, any
two of which recover. Read that carefully before using it: splitting a phrase
into overlapping groups of words is not Shamir, and a single piece reveals most
of the words rather than nothing at all.

**Their sharding guidance, where they do shard,** lands close to this framework:
2-of-3 across home, work and a bank deposit box, with 3-of-5 and 4-of-9 for
people who have more locations or want to involve others, and group-of-groups
configurations beyond that.

**And their warning, which is aimed squarely at designs like this one.** Their
SSKR-Dangers document says that "reconstructing a seed using a secret-sharing
scheme should always be considered a danger, at least in the case of a
single-sig situation where the secret is all that's needed to access assets",
and names three risks at reconstruction time: shard holders being talked into
handing shards over, the transfer being eavesdropped, and the machine used for
reconstruction being compromised. Their preferred alternative is to shard one
key of a multisig rather than the only key of a single-sig wallet.

That criticism deserves a direct answer rather than a mention:

- **Talking holders into handing shards over** does not apply to the solo
  framework, where nobody holds anything, and becomes live the moment you take
  the [§11](README.md#11-involving-others-later-the-upgrade-path) upgrade. It is
  a good argument for the rule that a share-holder must never also be able to
  reach the payload.
- **Eavesdropping the transfer** does not apply either, because the cards are
  collected by you, in person, and never transmitted.
- **A compromised reconstruction machine** is the real one, and rule 8 exists
  for it: recovery happens only in the offline leave-no-trace environment, never
  on a daily-use machine. The framework already credits the published criticism
  of share-based backups for that rule
  ([§13](README.md#13-what-we-read-and-what-each-source-changed)).
- **The single-sig point stands.** At the final moment of recovery the seed does
  exist in one place, and no arrangement of shares changes that. Their remedy,
  multisig, is what [§11](README.md#11-involving-others-later-the-upgrade-path)
  recommends for large holdings, and the two compose: multisig protects the use
  of keys, this framework protects the backup of each one.

### Reference libraries and topic guides

| Resource | Where | What it is |
| --- | --- | --- |
| **Lopp's Bitcoin security resources** | [lopp.net/bitcoin-information/security.html](https://www.lopp.net/bitcoin-information/security.html) | Jameson Lopp's curated index. The place to start if you want breadth rather than one opinion |
| **Metal seed storage stress tests** | [jlopp.github.io/metal-bitcoin-storage-reviews](https://jlopp.github.io/metal-bitcoin-storage-reviews/) | The same author's destructive testing of metal backup products, now into its sixth round and dozens of devices. The reference for [§8](README.md#8-storing-the-shares-the-object-and-where-it-goes)'s durability claims, and the source of the figure that a house fire peaks around 1,300°F |
| **Athena Alpha** | [athena-alpha.com](https://www.athena-alpha.com/expert-bitcoin-security/) | Security and privacy guides written in three tiers, beginner through expert, so you can find the level you are actually at instead of the level a document assumes |
| **Multisig.Guide** | [bitcoiner.guide/multisig](https://bitcoiner.guide/multisig/) | Focused on the part most multisig material skips, which is recovering one rather than creating one |
| **Wizardsardine's self-custody guide** | [wizardsardine.com/blog/self-custody-guide](https://wizardsardine.com/blog/self-custody-guide/) | A current step-by-step for someone starting from nothing, from the team behind Liana |
| **Bitcoin Core's multisig tutorial** | [github.com/bitcoin/bitcoin](https://github.com/bitcoin/bitcoin/blob/master/doc/multisig-tutorial.md) | Multisig at the level of the reference implementation, with no product attached |

### Taught rather than read

Worth listing separately, because for a procedure that must be executed
correctly once, watching somebody do it is a different kind of help.

| Resource | Where | What it is |
| --- | --- | --- |
| **Ministry of Nodes** | [ministryofnodes.com.au](https://www.ministryofnodes.com.au/) | Video walkthroughs of wallet and node setup, including Sparrow |
| **BTC Sessions** | [btcsessions.ca](https://www.btcsessions.ca/) | Long-running video tutorials covering most hardware and wallet combinations |
| **Coldcard's own videos** | [coldcard.com/docs/how-to-videos](https://coldcard.com/docs/how-to-videos/) | Vendor material, which is the right source for device-specific steps and the wrong one for whether to use that device |
| **Bitcoiner.Guide** | [bitcoiner.guide](https://bitcoiner.guide/) | Now primarily paid one-to-one mentorship covering self-custody, multisig and inheritance, alongside the guides its author has written. Listed because for some people the missing ingredient is a person rather than a page |

### Books

| Book | What it is |
| --- | --- |
| **Cryptoasset Inheritance Planning**, Pamela Morgan | The standard work on the part this framework deliberately leaves out ([§12](README.md#12-what-this-framework-deliberately-does-not-do)) |
| **#SmartCustody**, Blockchain Commons | The book form of the risk-modelling material above, [free to read](https://github.com/BlockchainCommons/SmartCustodyBook) |

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
