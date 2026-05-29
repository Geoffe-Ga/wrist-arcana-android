## Role

You are a Kotlin/Compose engineer integrating a flag-gated feature into existing
flows without affecting the default build.

## Goal

Wire deck selection into the draw and reference paths so that, **when the flag is
on**, switching decks changes the active deck everywhere — while the flag-off
default remains exactly the single-deck v1.0 experience.

## Context

- **Parent epic:** #9
- **Predecessor issue(s):** #40 (DeckSelection VM + screen). Closes Epic 9.
- **SPEC section:** `plans/SPEC.md` §10.4 (lines 472–475), §16.9 (lines 624–625), §2 non-goals (lines 65–71).
- **Files involved:**
  - draw + reference VMs/screens — consult the selected deck id when the flag is on
  - `viewmodel/DeckSelectionViewModel.kt` — expose the active selection to those flows
  - flag-on integration tests + flag-off regression tests
- **Prior decisions:** flag stays false in v1.0; this path is exercised only in tests with the flag on. `future-work` label keeps the Ralph picker off this.
- **State of the world:** DeckSelection exists but is not wired into draw/reference (ISSUE_01).

## Output Format

A single PR containing:

- [ ] Draw + reference consume the selected deck when `MULTI_DECK_ENABLED` is on
- [ ] Flag-on integration tests (switching decks changes draws + reference content)
- [ ] Flag-off regression tests (behavior identical to single-deck v1.0)
- [ ] Flag default remains false

## Examples

**Test that should pass:**
```kotlin
@Test fun flag_on_switching_deck_changes_active_deck() = runTest {
    withFlag(MULTI_DECK_ENABLED = true) {
        deckSelectionVm.selectDeck("some-other-deck")
        assertEquals("some-other-deck", drawVm.activeDeckId)
    }
}
@Test fun flag_off_uses_default_deck() {
    assertEquals(AppConstants.DEFAULT_DECK_ID, drawVm.activeDeckId)
}
```

## Constraints

**Scope fence:** Do not surface deck selection by default; do not flip the flag.
No IAP, no new deck content/art (separate future SPEC).

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Flag-off default is byte-for-byte the shipped v1.0
behavior; the multi-deck path is complete behind the flag.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Coverage meets §5; both flag-on and flag-off paths tested.
- [ ] KDoc on the deck-switching seam.
- [ ] PR includes `Refs #9` and `Closes #41`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `future-work`, `multi-deck`
