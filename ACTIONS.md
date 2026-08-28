# Which parts you need

This framework backs seeds up. It has one procedure, and two places to join
it: with seeds you already hold, or by rolling them here first and carrying
straight on. This page says which sections each route reads and how many roll
sheets it prints.

**Generating a seed is not a destination here.** If that is all you came for,
[dice-to-seed](https://github.com/PeteSparrowBTC/dice-to-seed) is the tool and
its own instructions are the guide, and
[seed-generation](https://github.com/PeteSparrowBTC/seed-generation) surveys
the other ways to do it, neutrally about vendors and methods. This framework is
not neutral: it recommends dice, two named tools and two vendors, and says so
once rather than surveying the alternatives.

---

## Rolling the seeds here

Rolling produces one seed per cosigner key, from your own dice, with an origin
you can recompute from the roll sheet while it still exists. It does not settle
a passphrase, a wallet descriptor or anything about the backup: those belong to
the procedure below, which you carry straight on into.

Skip it if you already hold two cosigner seeds you trust, because you rolled
them yourself before or you audited how they were made and are satisfied. If
you hold one and want the second from dice, roll that one and bring the other.

The wallet itself gets built between the rolling and the backup, because the
backup wants its descriptor and the descriptor wants both keys
([why the wallet comes first](README.md#why-the-wallet-comes-before-the-backup), and
[which path and why](CRYPTOGRAPHY.md#the-derivation-path-this-framework-picks-and-why)).

## Backing seeds up

Backing up takes the seeds you hold, subject to rule 0 auditing how each one
was made ([§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting)),
and produces three things: three share cards, the encrypted payload file, and
the written recovery instructions that travel with each card
([what the cards hold, and what locks the payload](CRYPTOGRAPHY.md#slip-39-splitting-the-backup-key)).
It does not care whether the seeds came from this sitting's dice rolls, an earlier
generation, or a wallet you already run. What it needs is the seeds
themselves, an optional passphrase per cosigner, and the wallet descriptor.

## The routes, and what each one prints

Three routes arrive at this document, and each needs a different slice of
the framework and a different number of dice sheets. A sheet is one printed
roll log; this framework takes three, one per cosigner seed and one
for the backup key, and no two are ever the same sheet
([why](NUMBERS.md#why-99-rolls-is-not-256-bits)). One sheet covers all three:
sixty rolls, with a tick at the top saying whether this one is a seed or the
key ([why sixty](NUMBERS.md#one-sheet-for-every-secret-and-why-sixty-rolls-is-enough)).
Print a spare sheet and hold back a spare card on top of whatever your
row says. Printing happens on a networked machine before the offline session,
so a sheet spoiled at the table cannot be replaced from there.

| Route | What it is | Framework sections | Sheets |
| --- | --- | --- | --- |
| Rolling both seeds here | No wallet yet | [§1](README.md#1-what-you-are-protecting-and-the-two-ways-you-lose) through [§11](README.md#11-involving-others-later-the-upgrade-path), in order; [§6](README.md#6-setup-from-zero-the-ordered-checklist) is the checklist itself | Three, plus the spare |
| Rolling one, bringing one | Holds one seed already trusted and wants the second from dice | [§1](README.md#1-what-you-are-protecting-and-the-two-ways-you-lose) through [§11](README.md#11-involving-others-later-the-upgrade-path), in order, as the row above; inside [§6](README.md#6-setup-from-zero-the-ordered-checklist) roll for the seed you are generating and skip the bullet for the seed you brought | Two, the seed you generate and the key, plus the spare |
| Bringing both seeds | Arrives holding two cosigner seeds already trusted | [§1](README.md#1-what-you-are-protecting-and-the-two-ways-you-lose), [§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting) to decide whether the seeds you hold are worth backing up, [§3](README.md#3-the-rules), [§4](README.md#4-inventory-the-secrets-you-actually-hold), [§5](README.md#5-the-architecture-three-layers), all of [§6](README.md#6-setup-from-zero-the-ordered-checklist) starting at Phase A, which builds both the password manager the payload lives in and the Recovery Sheet its storage depends on, [§7](README.md#7-known-traps-each-has-bitten-real-people) through [§11](README.md#11-involving-others-later-the-upgrade-path) | One, for the key, plus the spare |

**One owner, two vendors.** The wallet is 2-of-2 keys, both cosigner keys
held by one owner, each on hardware from a different vendor. Two seeds is the
requirement. Twelve words each is what this framework rolls, because that is
128 bits and the curve behind a bitcoin key leaves an attacker 128 bits
whatever the seed length ([the arithmetic](NUMBERS.md#one-sheet-for-every-secret-and-why-sixty-rolls-is-enough)).

**A cosigner key held by someone else is that person's own document.** If
another person holds a cosigner key, they run this framework themselves, for
their own key, and the two backups never touch: no payload of yours holds
their seed, no payload of theirs holds yours, and neither of you holds the
other's cards.

**Other quorum shapes are not covered here.** 2-of-2 keys is what this
framework walks you through. Other shapes, 2-of-3 keys, 3-of-5 keys, anything
else, work in the tools and are a different document to write.

---

*Collaboration by Claude*

<!-- revision:start -->
**Revised 2026-08-28.**
<!-- revision:end -->
