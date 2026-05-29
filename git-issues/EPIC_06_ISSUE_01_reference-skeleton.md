## Role

You are a Wear OS Compose + MVVM engineer scaffolding a reference browser entry
screen.

## Goal

Create `CardReferenceViewModel` + `CardReferenceScreen` listing the 5 suits in
fixed order (icon + name + card count), replacing the Reference placeholder page,
with navigation stubs to a card list.

## Context

- **Parent epic:** #6
- **Predecessor issue(s):** none — skeleton issue for Epic 6. (Epic 2 must be merged: `CardRepository`.)
- **SPEC section:** `plans/SPEC.md` §6.3 CardReferenceScreen (lines 279–282), §10.3 `CardReferenceViewModel` (lines 467–470), §7.1 `Suit` metadata (lines 304–307).
- **Files involved:**
  - `viewmodel/CardReferenceViewModel.kt` — state (`suits`, `selectedSuit`, `cardsInSuit`, `selectedCard`); `loadSuits()`, `cardCount(suit)`
  - `ui/reference/CardReferenceScreen.kt` — 5 suits fixed order: Major (22 ⭐), Swords (14 ⚔️), Wands (14 🪄), Pentacles (14 🪙), Cups (14 🏆)
  - VM + Compose smoke tests
- **Prior decisions:** fixed suit order by `sortOrder`; counts from `CardRepository`/`Suit`.
- **State of the world:** `CardRepository` exists (Epic 2); Reference page is a placeholder.

## Output Format

A single PR containing:

- [ ] `CardReferenceViewModel` with `loadSuits`/`cardCount`
- [ ] `CardReferenceScreen` listing 5 suits with icon + name + count, replacing the placeholder
- [ ] Nav stub to a (not-yet-built) card list
- [ ] VM test (5 suits, correct counts/order) + Compose smoke test
- [ ] No card list/detail (ISSUE_02/03)

## Examples

**VM test that should pass:**
```kotlin
@Test fun loads_five_suits_in_order_with_counts() {
    vm.loadSuits()
    val suits = vm.uiState.value.suits
    assertEquals(listOf("Major Arcana","Swords","Wands","Pentacles","Cups"), suits.map { it.displayName })
    assertEquals(22, vm.cardCount(Suit.MAJOR_ARCANA))
}
```

## Constraints

**Scope fence:** No `CardListScreen` (ISSUE_02) or detail (ISSUE_03). No theming
polish (Epic 7).

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** The Reference page lists real suits backed by a real VM.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM 95–100% (§5); suit list + counts tested.
- [ ] KDoc on `CardReferenceViewModel`.
- [ ] PR includes `Refs #6` and `Closes #31`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `skeleton`, `reference`
