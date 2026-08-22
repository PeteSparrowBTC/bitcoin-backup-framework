# How the cryptography works

This framework names several cryptographic primitives without stopping to
explain them: SHA-256, BIP-39, BIP-32, SLIP-39, age, OpenPGP. For each one,
this page states what goes in, what comes out, what makes it hard to
reverse, what it guarantees, what it does not, and why this framework relies
on it.

Not how it works inside. No compression functions, no round structure, no
field arithmetic: those belong to a cryptography course, and
[§12](README.md#12-what-this-framework-deliberately-does-not-do) already
treats complexity itself as a risk. Knowing what a lock does and does not do
is enough to use it correctly; opening the lock is a different skill. The
arithmetic behind the counts below (bits, iterations, word counts) lives on
[the numbers page](NUMBERS.md); this page cross-links it rather than
repeating it.

You do not need this page to follow the framework's instructions. It exists
so the framework's own sections can use "SHA-256" or "threshold" and move
straight on, rather than pausing to define them each time.

<!-- revision:start -->
**Revised 2026-08-22.** The primitives described here are fixed by published
standards and do not move. What can move is which of them the tools use, so
the date says when a person last checked this page against those tools.
<!-- revision:end -->

---

## One-way functions, and SHA-256

A **one-way function** takes an input and produces an output that is easy to
compute forward and infeasible to compute backward: given the output alone,
there is no shortcut to finding an input that produces it, short of trying
inputs one at a time against a space too large to search.

**SHA-256** is the one-way function this framework uses. Input: any string of
bytes, of any length. Output: exactly 256 bits, always, however long or short
the input was. The same input always produces the same output, which is what
makes it useful here rather than just being a curiosity: anyone who has the
same roll digits, in the same order, gets the same 256 bits back, and can
check that against what a device or an app claims to have derived.

What it guarantees: given the digits, anyone reproduces the output; without
the digits, the output alone gives no way to find them. What it does not do
is create unpredictability. If the digits fed in carry 255.9 bits of
uncertainty ([why 99 rolls is not 256 bits](NUMBERS.md#why-99-rolls-is-not-256-bits)),
the 256-bit output is still only 255.9 bits uncertain. Hashing compresses and
fixes the length; it does not add randomness that was not already there.

SHA-256 shows up in several places in this framework's own tools, including
inside the BIP-39 checksum and inside the release checksum files described
below. The place this page is about is the dice: one roll log's digits
become a cosigner seed's entropy, and a different roll log's digits become
the 32-byte backup key `k`, computed as
`SHA-256(the roll digits, joined by nothing)`, which is why the key is
reproducible with one shell command: `printf '%s' "$ROLLS" | sha256sum`. Feed
the same function the same log for both and you get the seed and the key
from one root, which is exactly the collapse
[rule 0](README.md#3-the-rules) forbids: the key protecting the backup
becomes derivable from the wallet it protects
([the arithmetic](NUMBERS.md#what-the-hash-does-and-the-one-thing-it-cannot-do)).

## BIP-39: words from entropy, and a seed from words

BIP-39 does two conversions, not one.

**Entropy to words.** Input: entropy in one of five sizes the standard
allows, 128 to 256 bits; this framework only ever uses the two ends of that
range, for a 12-word or a 24-word seed. A checksum derived from the entropy
travels with it. Output: 12 or 24 words from a fixed list of 2,048, chosen so
each word carries a whole number of bits
([the arithmetic](NUMBERS.md#from-256-bits-to-24-words)). The checksum is
what lets a wallet tell you that a word was mistyped rather than silently
deriving a different, wrong wallet. This step is deterministic and reversible
in both directions: the words carry exactly the entropy, no more, no less.

**Words to seed.** Input: the words, plus an optional passphrase you supply.
Output: a 512-bit seed, produced by PBKDF2-HMAC-SHA512 run for 2,048
iterations ([why that count is small](NUMBERS.md#where-every-number-in-this-guide-comes-from)).
The salt is not the passphrase alone: it is the fixed string `mnemonic` with
the passphrase appended, which is why the derivation is salted at all even
when no passphrase is set. Running the words through this step many times,
rather than once, is what makes guessing passphrases against known words at
least somewhat costly, though 2,048 iterations is a low cost by modern
standards, which is why the passphrase itself has to be strong.

What this guarantees: the same words and the same passphrase always produce
the same seed, on any correct implementation, which is why a seed phrase
recovers in software you have never used. What it does not guarantee is any
signal on a wrong passphrase. Every passphrase, including a mistyped one,
produces a valid seed and a valid, empty wallet. There is no error to catch a
typo; the framework's own instruction to test with a small spend before
funding further exists because this step cannot warn you.

## BIP-32: one seed, many keys

Input: the 512-bit seed from BIP-39. Output: as many keys as a wallet needs,
derived by a fixed, deterministic procedure, organised as a tree so that
different branches can be handed to different purposes without exposing the
whole tree.

What it guarantees: the same seed, run through the same derivation path,
always yields the same keys, in any software that implements the standard
correctly. That determinism is what lets a wallet be rebuilt from words
alone, in different software, years apart.

What it does not guarantee is that words alone are enough. The **descriptor**
(the text describing which derivation path and script type a wallet uses) and
the wallet's **fingerprint** are what tell software how to walk that tree
correctly; without them, correct words can still derive the wrong addresses
in unfamiliar software, which is why both are treated as recovery-critical
rather than as optional metadata
([§4](README.md#4-inventory-the-secrets-you-actually-hold)). An **extended
public key** (xpub) sits at the other end of that guarantee: it lets whoever
holds it compute every address the wallet will ever use, which is a privacy
leak, but it carries no private key material, so it is not by itself a
spending risk.

## SLIP-39: splitting the backup key

Input: one short secret, 16 or 32 bytes in every interoperable
implementation. In this framework, that secret is the 32-byte backup key
`k`, never the seed itself
([why not the seed](README.md#4-inventory-the-secrets-you-actually-hold)).
Output: a set of word-list shares, built so that any threshold-many of them
reconstruct the secret exactly, and the framework's recommendation is
2-of-3 cards rather than the tool's own default of 3-of-5 cards.

SLIP-39 implements **Shamir's secret sharing**, named for its designer. Each
share by itself is consistent with every value the secret could possibly be,
not with a narrowed set of candidates, and only combining threshold-many
shares picks out the one true value. That is what it guarantees: fewer than
threshold shares reveal nothing at all, and threshold-many reconstruct the
secret exactly. What it does not guarantee is anything once threshold-many
shares are actually together: at that point the secret is fully
reconstructed, so shares held together are exactly as sensitive as the
secret they protect.

This framework relies on the below-threshold guarantee to make one location
holding one card useless on its own. It does not ask SLIP-39 to protect the
seed directly, and it does not use SLIP-39's own passphrase either. The
standard defines one: SLIP-0039 encrypts the master secret with a passphrase
before splitting it. This tool passes an empty string for that passphrase,
so there is no SLIP-39 passphrase for the reader to remember, a choice the
tool makes rather than a concept the standard lacks. What the standard has
no place for regardless is a BIP-39 passphrase, a wallet descriptor, or
notes: it splits one short secret and nothing else, which is why the
two-layer design here exists, to give those a home.

## age with scrypt: locking the payload

Input: the wallet payload (seed, passphrase, descriptor, notes), plus the
backup key `k`, used as a passphrase in age's passphrase mode. The
implementation wraps `AgeSharp`'s `ScryptRecipient`, handing it `k` as a hex
string. Output: an encrypted file.

Turning the passphrase into an encryption key goes through **scrypt**, whose
purpose is to make that step deliberately slow to compute, so that trying
many candidate passphrases is expensive. That work factor matters most when
the passphrase is something a person chose and might be guessed; here `k` is
the full 256-bit output of a hash, not a chosen phrase, so brute-forcing it
directly is infeasible regardless, and scrypt's slowness is a second margin
rather than the only one.

The payload itself is encrypted with **ChaCha20-Poly1305**, an authenticated
cipher. What it guarantees: without `k`, the ciphertext reveals nothing about
the payload, and any tampering with the ciphertext is detected on decryption,
because the authentication check fails, rather than silently producing
corrupted or misleading plaintext. What it does not guarantee is anything
about who encrypted the file or when; age proves confidentiality and
tamper-evidence, not authorship.

## OpenPGP and ASCII armor: the second lock

Input: the age ciphertext from the step above. Output: that ciphertext,
encrypted again with AES-256, then ASCII-armored into printable text. Both
layers take the same key, `k`, the tool's armor header says so in plain
words, and that reuse is a deliberate choice: an independent key for the
outer layer would close a theoretical gap below at the cost of turning
recovery from typing one secret twice into a derivation step no ordinary
tool performs.

Nesting the two locks also buys a concrete margin against a future quantum
computer. age's own file key is 128 bits, and Grover's algorithm, the best
known quantum attack against a key of that kind, would cut the effective
search down to 64 bits. AES-256 in the layer wrapped around it restores
that headroom back to 128 bits, which is the structural reason for this
particular pairing rather than only for having two locks in general.

That shared key is what fixes what the second lock actually buys, and it is
narrower than "an attacker needs to break two things." A break in either
layer's cipher or file format leaves the cascade standing: breaking age's
internals does not hand over `k`, because `k` enters age only through
scrypt, which is one-way, so an attacker who somehow broke age's cipher
would still face OpenPGP's AES-256 guarding the same key from the other
side. What does collapse the cascade is recovering `k` itself, by inverting
scrypt or by inverting OpenPGP's passphrase-to-key derivation: either one
opens both layers, since both were locked with the same key. So the two
locks are independent against a break in the cipher, not against a break
that recovers the shared key.

ASCII armor is a separate property from either encryption layer: it
re-encodes the ciphertext as text, which is why `payload.age.gpg.asc` can
live inside a password manager note, an email, or a printed page rather than
needing to be handled as a binary file. Armor also carries a **CRC-24**
checksum over that text, which catches accidental corruption such as a bad
paste. A 24-bit checksum makes an accidental change unlikely to produce a
matching checksum by chance, but it does not catch a deliberate change made
by someone who recomputes the checksum after editing the text, so it is a
transcription check rather than a security one. Deliberate tampering with
the ciphertext itself is caught by the layers underneath instead: OpenPGP is
written with its own integrity packet and checks it on decryption, and
ChaCha20-Poly1305 does the same inside age, so an alteration to either layer
is detected there rather than producing a wrong but plausible result.

## Checksums and signatures: what each one proves

Both tools this framework uses publish a **SHA-256 checksum file** beside
each release. Recomputing that hash over the file you downloaded and
comparing it against the published value proves the file is bit-identical to
the one the checksum describes. It does not prove who published it: the
checksum travels with the file, so a substituted file and a substituted
checksum arrive together and agree with each other.

**Tails** instead publishes a real **signature**, verified against a key
obtained independently of the download itself. A signature proves the file
was produced by whoever holds that specific private key, which is a stronger
claim than a checksum makes, and is why Tails is verified that way while the
tools are verified by checksum. Intact and genuine are different claims.

What neither one can do is see what happened in front of you. A checksum and
a signature both compare digital records against each other; neither has any
view of the dice. Press 4 where the die showed 5 and every check above still
agrees perfectly, because the tools converted what was typed, correctly. The
printed roll sheet exists for exactly this gap: it is the one record made
from the dice rather than from a keyboard, and comparing it against the
screen before deriving is the only check in the system that can catch a
mis-press.

## What none of this protects

Every primitive on this page protects something specific, and none of them
protect the following.

- **Weak entropy at the root.** SHA-256 compresses what it is given,
  BIP-39 and BIP-32 derive from it, SLIP-39 splits it, and age and OpenPGP
  lock it away; none of them manufactures randomness. A seed built from a
  defective generator produces a cryptographically well-formed backup of a
  weak secret
  ([§2](README.md#2-before-you-back-it-up-is-the-secret-worth-protecting)).
- **Trust in a random number generator, even after rolling your own key.**
  Dice give `k` an origin the reader can recompute, but `k` never touches
  the payload directly. age generates its own random file key on the
  machine running the tool, using that machine's random number generator,
  encrypts the payload under that file key, and only then locks the file
  key itself with `k` through scrypt. Rolling `k` from dice does not remove
  the machine's random number generator from the design; it makes the
  wrapper around that generator's output accountable, not the generator
  ([the same point in the failure matrix](README.md#10-failure-mode-matrix-what-saves-you)).
- **A filled roll sheet left in a drawer.** A sheet with the dice results
  written on it is a seed or a key in plain text. No cryptography on this
  page defends paper; destroying the sheet once the backup is proven is what
  does.
- **Threshold-many cards sitting in the same place as the payload.** Below
  threshold, SLIP-39 reveals nothing; without `k`, age and OpenPGP reveal
  nothing. Both guarantees assume the shares and the payload are apart. Put
  threshold-many cards next to the file they unlock and the whole secret is
  assembled in one place.

---

*Collaboration by Claude*
