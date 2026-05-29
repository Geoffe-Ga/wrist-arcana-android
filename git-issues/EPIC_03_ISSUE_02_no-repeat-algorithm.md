## Role

You are a Kotlin engineer porting a cryptographically-fair, no-repeat card
selection algorithm and proving its invariants with statistical tests.

## Goal

Implement the no-repeat CSPRNG selection (SPEC §8.1) in `CardDrawViewModel` so
that across a full deck every card appears exactly once before any repeat, then
the session set resets.

## Context

- **Parent epic:** #3
- **Predecessor issue(s):** #19 (RNG interface + VM skeleton + `drawnThisSession`).
- **SPEC section:** `plans/SPEC.md` §8.1 algorithm (lines 393–407), §1 no-repeat invariant (lines 44–45).
- **Files involved:**
  - `viewmodel/CardDrawViewModel.kt` — replace the stub selection with `selectRandomCard(deck)`
  - optionally `data/repo/DeckRepository.getRandomCard` if the SPEC's seam fits better there (keep one source of truth)
  - VM tests using `FakeRandomGenerator`
- **Prior decisions:** algorithm verbatim from §8.1 — clear `drawnThisSession` when it covers the deck; `available = cards.filterNot { it.id in drawnThisSession }`; pick via `secureRandom.nextInt(size)`; add the picked id to the set.
- **State of the world:** VM skeleton + RNG exist (ISSUE_01); selection is still stubbed.

## Output Format

A single PR containing:

- [ ] Real `selectRandomCard` honoring the no-repeat-until-exhausted rule
- [ ] VM tests: across 78 draws each card id appears exactly once; the 79th draw resets and re-draws; distribution sanity with the real `SecureRandom`
- [ ] No suspense/haptic/save yet (ISSUE_03)

## Examples

**Invariant test:**
```kotlin
@Test fun no_repeat_until_deck_exhausted() {
    val seen = mutableListOf<String>()
    repeat(78) { seen += vm.selectRandomCard(deck)!!.id }
    assertEquals(78, seen.toSet().size)   // all unique
    val next = vm.selectRandomCard(deck)!!.id
    assertTrue(next in seen)              // 79th may repeat (set reset)
}
```

## Constraints

**Scope fence:** No persistence of the pull (ISSUE_03), no UI beyond what
ISSUE_01 built. Do not introduce a seeded PRNG — CSPRNG only.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Drawing now returns a real, fair, non-repeating card;
the screen still works end-to-end.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM coverage 95–100% (§5); no-repeat invariant + reset + distribution tested.
- [ ] KDoc on the selection method.
- [ ] PR includes `Refs #3` and `Closes #20`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `draw`
