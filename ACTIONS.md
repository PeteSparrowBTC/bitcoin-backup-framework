# Generate, back up, or both

This framework covers two separate actions: generating seeds and backing
seeds up. Either is useful on its own. Generating gives you keys rolled from
your own dice, whether or not you back them up today. Backing up takes the
seeds you hold, whatever their origin, and turns them into a recoverable,
encrypted payload and a set of cards. This page says what each action
produces, which one you need, and how much of [the framework](README.md) each
combination reads.

---

## Generating seeds

Generating produces one seed per cosigner key, rolled from dice, with an
origin you can recompute from the roll log while it still exists. It does not
touch a passphrase choice, a wallet descriptor, or the backup: those belong to
the action below.

Generating is optional. If you already hold two cosigner seeds you trust,
because you rolled them yourself before, or you audited how they were made
and are satisfied, there is nothing to generate. Go straight to backing up.
If you hold one seed you trust and want the second from dice, generate that
one and bring the other.

Most readers stop after generating, because a two-vendor build usually has to:
the backup needs a wallet descriptor, and that gets built on another machine
between the two sittings
([what to do before you leave the table](README.md#the-pause-between-generating-and-backing-up)).

This page does not survey the other ways to generate a seed. That survey
lives at [seed-generation](https://github.com/PeteSparrowBTC/seed-generation),
which is deliberately neutral about vendors and methods. This framework is
not: it recommends dice, two named tools, and two vendors, and says so once
rather than surveying the alternatives.

## Backing seeds up

Backing up takes the seeds you hold, subject to rule 0 auditing how each one
was made ([§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting)),
and produces three things: three share cards, the encrypted payload file, and
the written recovery instructions that travel with each card
([what the cards hold, and what locks the payload](CRYPTOGRAPHY.md#slip-39-splitting-the-backup-key)).
It does not care whether the seeds came from this sitting's dice rolls, an earlier
generation, or a wallet you already run. What it needs is the seeds
themselves, an optional passphrase per cosigner, and the wallet descriptor.

## Which parts you need

Four journeys arrive at this document, and each needs a different slice of
the framework and a different number of dice sheets. A sheet is one printed
roll log; the recommended shape takes three, one per cosigner seed and one
for the backup key, and no two are ever the same sheet
([why](NUMBERS.md#why-99-rolls-is-not-256-bits)). Print a spare sheet and
hold back a spare card on top of whatever your row says. Printing happens on
a networked machine before the offline session, so a sheet spoiled at the
table cannot be replaced from there, and the spare is also what the key gets
rolled on by a reader who generates today and builds the backup weeks
later.

| Journey | What it is | Framework sections | Sheets |
| --- | --- | --- | --- |
| Both actions, one sitting | No wallet yet | [§1](README.md#1-what-you-are-protecting-and-the-two-ways-you-lose) through [§11](README.md#11-involving-others-later-the-upgrade-path), in order; [§6](README.md#6-setup-from-zero-the-ordered-checklist) is the checklist itself | Three, plus the spare |
| Both actions, arriving with one cosigner seed | Holds one seed already trusted and wants the second from dice | [§1](README.md#1-what-you-are-protecting-and-the-two-ways-you-lose) through [§11](README.md#11-involving-others-later-the-upgrade-path), in order, as the row above; inside [§6](README.md#6-setup-from-zero-the-ordered-checklist) roll for the seed you are generating and skip the bullet for the seed you brought | Two, the seed you generate and the key, plus the spare |
| Backing up only | Arrives holding two cosigner seeds already trusted | [§1](README.md#1-what-you-are-protecting-and-the-two-ways-you-lose), [§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting) to decide whether the seeds you hold are worth backing up, [§3](README.md#3-the-rules), [§4](README.md#4-inventory-the-secrets-you-actually-hold), [§5](README.md#5-the-architecture-three-layers), all of [§6](README.md#6-setup-from-zero-the-ordered-checklist) starting at Phase A, which builds both the password manager the payload lives in and the Recovery Sheet its storage depends on, [§7](README.md#7-known-traps-each-has-bitten-real-people) through [§11](README.md#11-involving-others-later-the-upgrade-path) | One, for the key, plus the spare |
| Generating only | Wants keys rolled from dice, not ready to build the backup | [§1](README.md#1-what-you-are-protecting-and-the-two-ways-you-lose), [§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting), [§3](README.md#3-the-rules) for rule 0, [§6](README.md#6-setup-from-zero-the-ordered-checklist) as far as [the generation exit](README.md#the-pause-between-generating-and-backing-up) | Two, one per cosigner seed, plus the spare the key is rolled on when you come back |

**One owner, two vendors.** The recommended wallet is 2-of-2 keys, both
cosigner keys held by one owner, each on hardware from a different vendor.

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
**Revised 2026-08-22.**
<!-- revision:end -->
