## Role

You are a Kotlin data engineer building the read-only reference data source that
the browser screens will consume.

## Goal

Implement `CardRepository` to load cards once and expose them sorted and
filtered: `getAllCards()` (by `suit.sortOrder` then `number`), `getCards(suit)`,
`getCard(id)`, `getSuits()` (5, sorted), with a single-Fool fallback on load
failure.

## Context

- **Parent epic:** #2
- **Predecessor issue(s):** #15 (JSON + `DeckRepository` decode it reuses).
- **SPEC section:** `plans/SPEC.md` §7.5 `CardRepository` (lines 380–387), §6.3 reference data needs (lines 277–293).
- **Files involved:**
  - `data/repo/CardRepository.kt` — implements `CardRepositoryProtocol`
  - tests for sort order, suit filtering, id lookup, fallback
- **Prior decisions:** load once and cache; fall back to the single "Fool" card on failure. Reuse the validated deck from `DeckRepository`/JSON.
- **State of the world:** models + `DeckRepository` + JSON exist (ISSUE_01/02).

## Output Format

A single PR containing:

- [ ] `CardRepository` with `getAllCards`/`getCards(suit)`/`getCard(id)`/`getSuits`
- [ ] Tests: 78 cards sorted by `suit.sortOrder` then `number`; per-suit counts (Major 22, others 14); id lookup hit/miss; fallback on load failure
- [ ] No images/Room/UI

## Examples

**Test that should pass:**
```kotlin
@Test fun all_cards_sorted_by_suit_then_number() {
    val cards = repo.getAllCards()
    assertEquals(78, cards.size)
    assertTrue(cards.zipWithNext().all { (a, b) ->
        a.suit.sortOrder < b.suit.sortOrder ||
        (a.suit == b.suit && a.number <= b.number)
    })
}
@Test fun cups_has_14() { assertEquals(14, repo.getCards(Suit.CUPS).size) }
```

## Constraints

**Scope fence:** Images/resId map (ISSUE_04) and Room (ISSUE_05) are out of scope.
No reference UI (Epic 6).

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Reference data is now queryable; Epic 6 can build on it
without further data work.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Repository coverage 90–100% (§5); sort/filter/lookup/fallback tested.
- [ ] KDoc on `CardRepository` public methods.
- [ ] PR includes `Refs #2` and `Closes #16`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `data`
