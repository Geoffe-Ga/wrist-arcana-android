## Role

You are a Kotlin/Compose engineer building a feature behind a disabled flag so it
ships code-complete but invisible.

## Goal

Implement `DeckSelectionViewModel` (`loadDecks`/`selectDeck`) and a
`DeckSelectionScreen` that is reachable **only** when
`FeatureFlags.MULTI_DECK_ENABLED == true` (default **false**).

## Context

- **Parent epic:** #9
- **Predecessor issue(s):** none for this epic; Epic 2 (multi-deck-capable repos/models) must be merged. Skeleton issue for Epic 9.
- **SPEC section:** `plans/SPEC.md` §10.4 (lines 472–475), §12 `MULTI_DECK_ENABLED` (line 523), §2 non-goals (lines 65–71), §16.9 (lines 624–625).
- **Files involved:**
  - `viewmodel/DeckSelectionViewModel.kt` — state (`availableDecks`, `selectedDeckId`, `errorMessage`); `loadDecks()`, `selectDeck(id)`
  - `ui/.../DeckSelectionScreen.kt` — surfaced only behind the flag
  - `config/FeatureFlags.kt` — `MULTI_DECK_ENABLED = false`
  - VM tests + a test proving no entry point exists with the flag off
- **Prior decisions:** flag default false; the v1.0 build never surfaces this (product invariant). `future-work` label keeps the Ralph picker off this issue.
- **State of the world:** single-deck app complete; flag not yet exercised.

## Output Format

A single PR containing:

- [ ] `DeckSelectionViewModel` + `DeckSelectionScreen` gated by `MULTI_DECK_ENABLED`
- [ ] VM tests (`loadDecks`, `selectDeck`) + a test asserting no reachable UI with the flag off
- [ ] No wiring into draw/reference yet (ISSUE_02)

## Examples

**Test that should pass:**
```kotlin
@Test fun deck_selection_hidden_when_flag_off() {
    assertFalse(FeatureFlags.MULTI_DECK_ENABLED)
    // navigation graph exposes no route to DeckSelectionScreen with the flag off
    assertTrue(reachableRoutes(flagEnabled = false).none { it.contains("deckSelection") })
}
```

## Constraints

**Scope fence:** Do not wire deck switching into draw/reference (ISSUE_02). Do not
flip the flag default to true. No IAP/purchase flow, no new deck content.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** With the flag off (default), the app is unchanged; the
new code is dormant and tested.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM 95–100% (§5); flag-off invisibility tested.
- [ ] KDoc on `DeckSelectionViewModel` + the flag.
- [ ] PR includes `Refs #9` and `Closes #40`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `skeleton`, `future-work`, `multi-deck`
