## Role

You are a Wear OS Compose + MVVM engineer wiring a filtered, sorted list screen.

## Goal

Implement `selectSuit(s)` → `CardListScreen` showing the chosen suit's cards
sorted by number (thumbnail + full display name), navigating to a card detail.

## Context

- **Parent epic:** #6
- **Predecessor issue(s):** #31 (reference VM + suit screen).
- **SPEC section:** `plans/SPEC.md` §6.3 CardListScreen (lines 284–286), §10.3 `selectSuit` (lines 468–470), §7.1 `fullDisplayName` (lines 309–311).
- **Files involved:**
  - `viewmodel/CardReferenceViewModel.kt` — `selectSuit(s)` (filter + sort by number), `selectCard`, `deselectCard`
  - `ui/reference/CardListScreen.kt` — thumbnail (resId map) + `fullDisplayName`, sorted by number; tap → detail
  - VM + Compose UI tests
- **Prior decisions:** sort within suit by `number`; reuse `CardRepository.getCards(suit)`.
- **State of the world:** suit screen + VM skeleton exist (ISSUE_01).

## Output Format

A single PR containing:

- [ ] `selectSuit`/`selectCard` in the VM; `CardListScreen`
- [ ] Navigation suit → list; list row → detail (detail content lands in ISSUE_03)
- [ ] VM test (cards filtered + sorted by number) + UI test (suit tap → list shows N cards in order)

## Examples

**VM test that should pass:**
```kotlin
@Test fun selectSuit_filters_and_sorts_by_number() {
    vm.loadSuits(); vm.selectSuit(Suit.SWORDS)
    val cards = vm.uiState.value.cardsInSuit
    assertEquals(14, cards.size)
    assertTrue(cards.zipWithNext().all { (a, b) -> a.number <= b.number })
}
```

## Constraints

**Scope fence:** No reference detail content (ISSUE_03). No theming polish (Epic 7).

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Suit → list navigation works end-to-end; detail is the
next slice.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM 95–100%, components ≥60% (§5); filter/sort + navigation tested.
- [ ] KDoc on `selectSuit`.
- [ ] PR includes `Refs #6` and `Closes #32`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `reference`
