# How the numbers work

Every number in this guide comes from somewhere, and none of them are
conventions you have to take on trust. This page derives them: why a die roll is
worth 2.585 bits, why 99 rolls is not quite enough, why 24 words rather than 23,
and why a hex character is exactly half a byte.

You do not need this page to follow the instructions. It is here so that the
rest of the guide can say "32 bytes" without stopping to explain itself, and so
that when a tool shows you a number you can check whether it is the number it
should be.

---

## A bit is one halving

A **bit** is one yes-or-no answer. One bit distinguishes two things, two bits
distinguish four, three distinguish eight. Each bit you add doubles the number
of possibilities, so **n bits distinguish 2ⁿ things**.

Running that backwards: if something has N equally likely outcomes, it is worth
**log₂(N) bits**, which is the number of halvings it takes to get from N down to
one. This is the only piece of arithmetic on this page that matters, and
everything below is an application of it.

When people say a seed has "128 bits of entropy", they mean it was drawn from a
pool of 2¹²⁸ equally likely possibilities. An attacker who knows everything
except which one you got has that many to search.

## Why one die roll is 2.585 bits

A fair six-sided die has six equally likely outcomes, so one roll is worth:

```
log₂(6) = 2.5849625…  bits
```

The fraction is the whole story. Six is not a power of two, so a roll does not
fit neatly into a whole number of bits. Two bits would be four outcomes and
three bits would be eight, and six sits between them. You cannot round up: a
roll is not worth 3 bits, and treating it as though it were is how a count of
rolls ends up short.

Rolls are independent, so their bits add:

```
50 rolls  ×  2.585  =  129.2 bits
60 rolls  ×  2.585  =  155.1 bits
99 rolls  ×  2.585  =  255.9 bits
111 rolls ×  2.585  =  286.9 bits
```

## Why 99 rolls is not 256 bits

Look at the third line. **Ninety-nine rolls of a perfect die produce 255.9 bits,
not 256.** It misses by about a tenth of a bit, and no die is perfect, so the
real figure is lower still.

Ninety-nine is the number most vendors ask for, and it is a rounding rather
than a proof of sufficiency: 256 ÷ 2.585 = 99.03, rounded down. The shortfall
is small and it is real, and it is in the roll count rather than in the dice.
The fix is also small: roll past the minimum. Sixty rolls instead of fifty, and
111 instead of 99, put you clear of the target with room for a die that is not
quite fair.

Each of those counts is per sheet. This framework rolls sixty for each of its
three secrets, the two cosigner seeds and the backup key, so three sheets,
each rolled and hashed on its own
([why sixty everywhere](#one-sheet-for-every-secret-and-why-sixty-rolls-is-enough)).

## Two kinds of entropy, and why the tables have three columns

The 2.585 figure is the **average** surprise per roll, called Shannon entropy.
It is the right measure when outcomes are equally likely and the wrong one when
they are not, because an attacker does not guess averagely. They start with the
most likely outcome.

The measure that matches an attacker is **min-entropy**: the surprise of the
single most likely outcome, which is the worst case rather than the average
one. For a fair die the two are identical. For a biased die, min-entropy is
lower, and it is the number to plan against.

This is why the roll-count table in
[dice-to-seed](https://github.com/PeteSparrowBTC/dice-to-seed#what-you-need)
has three columns: a fair die, a real die as actually measured, and a
deliberately pessimistic case.

How biased is a real die? The largest published count is Weldon's, from 1894:
315,672 rolls of ordinary dice, in which a 5 or 6 came up 33.77% of the time
against the 33.33% expected. Ordinary dice have recessed pips filled with
lighter paint, so the 6 face is fractionally lighter and lands upward slightly
more often. Across a 60-roll log that costs about 0.004 bits on the average
measure and about 1.1 bits on the min-entropy floor. It is a real effect and it
is much smaller than the margin you get from rolling eleven extra times.

## Why this guide says one die

Throwing several dice at once and reading them in one go is faster, and the
count does not matter: three, four, five or six all work. n dice are n
independent rolls worth n × 2.585 bits, **provided the order you read them in
does not depend on what they show.** Fix it before you throw, left to right
where they land or by colour in an order you wrote down, and nothing is lost.

The reason this guide says one die anyway is what happens when that condition
fails. The natural accident is to read the dice sorted by value, which records
only which faces appeared and how many times. There are far fewer of those than
there are ordered outcomes, and the gap widens with every die you add:

| dice | ordered outcomes | if read sorted | worth ordered | worth sorted | lost |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | 6 | 2.58 bits | 2.58 bits | 0 |
| 2 | 36 | 21 | 5.17 | 4.39 | 0.8 bits |
| 3 | 216 | 56 | 7.75 | 5.81 | 1.9 |
| 4 | 1,296 | 126 | 10.34 | 6.98 | 3.4 |
| 5 | 7,776 | 252 | 12.92 | 7.98 | **4.9** |
| 6 | 46,656 | 462 | 15.51 | 8.85 | **6.7** |

So the more dice you add, the more the mistake costs, and the mistake leaves no
trace. A seed built from sorted throws looks exactly like a seed built
correctly, imports fine everywhere, and derives valid addresses. Nothing tells
you, which is the same property that made the 2026 Coldcard defect so expensive.

One die removes the rule instead of asking you to keep it at roll eighty. It
costs about a quarter of an hour per log. If you do use several, the count is
yours to choose and the condition is the same at any count.

## The same die for every sheet

Use one die for every sheet: a cosigner seed's sheet and the key's sheet
alike. A die has no memory, so each sheet is its own independent set of
rolls, and a second die adds nothing except another object whose fairness
you have not considered.

A bias does not couple them either. If your die favours 6, every sheet is
weakened in the same way and remains independent of the others: an attacker
who exploits the bias still has to search each secret separately, and knowing
one tells them nothing about another. What must not be shared is the **roll
log**, and that is a different failure, described next.

## What the hash does, and the one thing it cannot do

Your roll log is a string of digits. The tools turn it into a key by hashing
it ([what a one-way function is](CRYPTOGRAPHY.md#one-way-functions-and-sha-256)):

```
k = SHA-256(the roll digits, joined by nothing)
```

SHA-256 always produces exactly 256 bits, whatever you feed it. That is what
makes it useful here: sixty rolls carry 155.1 bits, and the hash turns however
many bits you rolled into a value of exactly the width the tools take, in a way
anyone can reproduce and check.

**What it cannot do is create randomness.** If you feed it 255.9 bits of
unpredictability, the output is 256 bits long and still only 255.9 bits
unpredictable. An attacker attacks your roll log, not the hash's output size.
This is the reason roll counts matter at all, and the reason a short log cannot
be rescued by hashing it into a longer key.

It is also why the design is checkable. Because the key is the hash of the rolls
and nothing else, one command reproduces it:

```
printf '%s' "$ROLLS" | sha256sum
```

A tool that mixed in its own randomness would produce a key nobody, including
you, could ever recompute.

**And it is why a seed's roll log and the key's roll log must never be the
same one.** On a 24-word seed the BIP-39 entropy is SHA-256 of your rolls, and
the backup key is SHA-256 of your rolls. Same function, same input, same
output: reuse one log for both and the key protecting your backup *is* the
wallet it protects, so the shares stop protecting anything. On a 12-word seed
it is the first half of the same hash, which is no better. Both tools enforce
this rather than only warning about it:
`dice-to-seed` clears your rolls when you change mode, and `slip39-backup`
recovers the entropy of every seed in the form, compares it against the key, and
refuses if they match.

## From 256 bits to 24 words

BIP-39, the standard behind seed phrases, turns those bits into words with a
word list of exactly **2,048** entries
([what BIP-39 does with them](CRYPTOGRAPHY.md#bip-39-words-from-entropy-and-a-seed-from-words)).
That number is chosen so each word carries a whole number of bits:

```
2,048 = 2¹¹     so one word = 11 bits
```

The phrase also carries a checksum, which is what lets a wallet tell you that
you mistyped a word rather than silently deriving the wrong account. The
checksum is one bit for every 32 bits of entropy:

| entropy | checksum | total | ÷ 11 | words |
| --- | --- | --- | --- | --- |
| 128 bits | 4 bits | 132 | 132 ÷ 11 | **12** |
| 256 bits | 8 bits | 264 | 264 ÷ 11 | **24** |

So 24 words is not a style choice. It is the only whole number of words that
256 bits plus its checksum divides into.

**SLIP-39, which splits the backup key, uses a different list**: 1,024 words, so
each word is 10 bits. A share of a 256-bit secret is 33 words, or 330 bits: the
share value, the identifiers and threshold that say which share this is and how
many are needed, and a 30-bit checksum. A 128-bit secret gives 20-word shares.
The two lists are different, so a SLIP-39 share is not a seed phrase and cannot
be typed into a wallet as one.

## One sheet for every secret, and why sixty rolls is enough

This framework rolls three secrets: two cosigner seeds of twelve words each,
and the backup key `k`. All three take sixty rolls, so all three take the same
printed sheet, ticked at the top for what it is.

**Twelve words is 128 bits, and 128 bits is where the ceiling already sits.** A
bitcoin private key is a point on the secp256k1 curve, and the fastest known
attack on a curve that size is Pollard's rho, which costs about the square root
of the number of points:

```
sqrt(2^256)  =  2^128  operations
```

So a twenty-four-word seed does not make an attacker do 2²⁵⁶ work. It makes
them do 2¹²⁸, the same as a twelve-word seed, because the cheapest way in is
the key itself and not the phrase that produced it. The extra 128 bits sit
above a ceiling the curve has already set, and they charge for the privilege.
Nothing in this procedure is copied onto paper by hand, but the words are still
keyed in three times before they are done: once into each cosigner's device to
build the wallet, and once more into whatever wallet a recovery happens in,
years later, in conditions nobody gets to choose. Twenty-four words doubles
every one of those, and keying mistakes are what most of the checks in this
guide exist to catch.

**`k` is 128 bits for the same reason, one step further along.** The key is
32 bytes whatever you roll, because it is a SHA-256 output and `slip39-backup`
accepts nothing else. Sixty rolls change the entropy behind those 32 bytes and
not their width, so the shares stay 33 words and nothing downstream notices.
And 128 bits is not the weak link: someone who wants the coins without going
near the payload faces the same 2¹²⁸ at the curve, so raising `k` to 256 bits
lifts a ceiling that was never the binding one. `dice-to-seed` offers the
128-bit strength in its backup-key mode, and the sheet carries a backup-key
tick beside its sixty boxes.

A quantum attacker does not change this either. Grover's algorithm would halve
a symmetric key's strength, which is the usual argument for 256 bits, but
Shor's algorithm breaks the curve outright, so the wallet is gone long before
the payload's key matters
([what `k` protects](CRYPTOGRAPHY.md#slip-39-splitting-the-backup-key)).

## Bytes, and why a hex character is half a byte

A **byte** is 8 bits, so it has 2⁸ = 256 possible values. Keys are quoted in
bytes out of habit rather than necessity: 32 bytes is 32 × 8 = **256 bits**, the
same number as above and not a coincidence, because the key is a hash output.

**Hexadecimal** writes numbers with sixteen digits instead of ten: `0` to `9`,
then `a` to `f`. Sixteen is a power of two:

```
16 = 2⁴     so one hex character = exactly 4 bits
```

A byte is 8 bits, and 8 ÷ 4 = 2, so **two hex characters make one byte and a
single hex character is exactly half of one.** That exactness is the entire
reason hex is used. Decimal digits carry log₂(10) = 3.32 bits, which is not a
whole number, so a decimal digit never lines up with a byte boundary and you
cannot read a key off in fixed-size pieces.

Putting it together, for the backup key `k`:

```
32 bytes  =  256 bits  =  64 hex characters
```

which is why the tool displays 64 characters and why they are grouped in fours:
each group of four hex characters is 16 bits, and counting groups is easier than
counting characters when you are copying by hand and lose your place.

## The four-character check code

The check code beside the key is 4 hex characters, so:

```
4 × 4 bits = 16 bits = 65,536 possible values
```

If you mistype the key while copying it, the odds that your wrong key produces
the same check code are 1 in 65,536. That is a good typo detector and it is
nothing else. Sixteen bits is trivial for anyone who can change the key on
purpose, and the code is not treated as though it were security.

## Where every number in this guide comes from

| Number | Why |
| --- | --- |
| 2.585 bits per roll | log₂(6); six is not a power of two |
| 50 rolls | 128 ÷ 2.585 = 49.5, rounded up. The vendor minimum |
| **60 rolls** | Every secret this framework rolls. Clears 128 bits on the pessimistic measure as well as the average |
| 99 rolls | 256 ÷ 2.585 = 99.03, rounded down. Reaches 255.9, not 256 |
| 111 rolls | Clears 256 bits with margin for a real die. What a twenty-four-word seed takes |
| 2,048-word list | 2¹¹, so one BIP-39 word is 11 bits |
| 12 words | (128 + 4) ÷ 11. One cosigner seed |
| 32-byte `k` from 60 rolls | SHA-256 is 32 bytes whatever it is fed; the rolls set the entropy, not the width |
| 24 words | (256 + 8) ÷ 11 |
| 1,024-word list | 2¹⁰, so one SLIP-39 word is 10 bits |
| 33-word share | 256-bit share value plus metadata and a 30-bit checksum |
| 32-byte key | 32 × 8 = 256 bits, the width of a SHA-256 output |
| 64 hex characters | 256 ÷ 4; one hex character is 4 bits |
| 4-character check code | 16 bits, 1 in 65,536 of missing a typo |
| 2,048 PBKDF2 iterations | BIP-39's fixed work factor for the passphrase, and the reason a passphrase must be strong on its own |

---

*Collaboration by Claude*

<!-- revision:start -->
**Revised 2026-08-28.**
<!-- revision:end -->
