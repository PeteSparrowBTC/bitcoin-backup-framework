# Generate, back up, or both

This framework covers two separate actions: generating seeds and backing
seeds up. Either is useful on its own. Generating gives you keys with an
origin you can vouch for, whether or not you back them up today. Backing up
takes the seeds you hold, whatever their origin, and turns them into a
recoverable, encrypted payload and a set of cards. This page says what each
action produces, which one you need, and how much of [the framework](README.md)
each combination reads.

<!-- revision:start -->
**Revised 2026-08-22.** This page is new. It exists because the framework now
supports three distinct starting points, and a reader arriving at any of them
needs to know which parts apply before opening the framework itself.
<!-- revision:end -->

---

## Generating seeds

Generating produces one seed per cosigner key, rolled from dice, with an
origin you can recompute from the roll log while it still exists. It does not
touch a passphrase choice, a wallet descriptor, or the backup: those belong to
the action below.

Generating is optional. If you already hold two cosigner seeds you trust,
because you rolled them yourself before, or you audited how they were made
and are satisfied, there is nothing to generate. Go straight to backing up.

Stopping after generating is supported. You end the sitting holding two
seeds on paper and no backup of either, which is a real position with a real
cost stated plainly: do not fund the wallet beyond pocket change until the
backup exists, and the machine that has held the seeds never goes back online.
[The exit for this journey](README.md#if-you-are-stopping-after-generating)
is in the framework's setup checklist.

This page does not survey the other ways to generate a seed: coins, cards,
device generators, or verifying an existing one. That survey lives at
[seed-generation](https://github.com/PeteSparrowBTC/seed-generation), which
is deliberately neutral about vendors and methods. This framework is not: it
recommends dice, two named tools, and two vendors, and says so once rather
than surveying the alternatives.

## Backing seeds up

Backing up takes the seeds you hold, subject to rule 0 auditing how each one
was made ([§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting)),
and produces three things: three share cards, the encrypted payload file, and
the written recovery instructions that travel with each card. It does not
care whether the seeds came from this sitting's dice rolls, an earlier
generation, or a wallet you already run. What it needs is the seeds
themselves, an optional passphrase per cosigner, and the wallet descriptor.

## Which parts you need

Three journeys arrive at this document, and each needs a different slice of
the framework and a different number of dice sheets. A sheet is one printed
roll log; the recommended shape takes up to three, one per cosigner seed and
one for the backup key, and no two are ever the same sheet
([why](NUMBERS.md#why-99-rolls-is-not-256-bits)).

| Journey | What it is | Framework sections | Sheets |
| --- | --- | --- | --- |
| Both actions, one sitting | No wallet yet | [§1](README.md#1-what-you-are-protecting-and-the-two-ways-you-lose) through [§11](README.md#11-involving-others-later-the-upgrade-path), in order; [§6](README.md#6-setup-from-zero-the-ordered-checklist) is the checklist itself | Three |
| Backing up only | Arrives holding two cosigner seeds already trusted | [§1](README.md#1-what-you-are-protecting-and-the-two-ways-you-lose), [§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting) to decide whether the seeds you hold are worth backing up, [§3](README.md#3-the-rules), [§4](README.md#4-inventory-the-secrets-you-actually-hold), [§5](README.md#5-the-architecture-three-layers), [§6](README.md#6-setup-from-zero-the-ordered-checklist) from Phase B onward, [§7](README.md#7-known-traps-each-has-bitten-real-people) through [§11](README.md#11-involving-others-later-the-upgrade-path) | One, for the key |
| Generating only | Wants keys it can vouch for, not ready to build the backup | [§1](README.md#1-what-you-are-protecting-and-the-two-ways-you-lose), [§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting), [§3](README.md#3-the-rules) for rule 0, [§6](README.md#6-setup-from-zero-the-ordered-checklist) as far as [the generation exit](README.md#if-you-are-stopping-after-generating) | Two, one per cosigner seed |

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
