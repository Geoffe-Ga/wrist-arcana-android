## Role

You are a Wear OS Compose engineer building a detail screen with a wrapping
chip layout.

## Goal

Build `CardReferenceDetailScreen` (image, name + suit + display number, Upright
and Reversed sections, keyword chips) and the `FlowRow` component for wrapping
keyword chips.

## Context

- **Parent epic:** #6
- **Predecessor issue(s):** #32 (card list + `selectCard`).
- **SPEC section:** `plans/SPEC.md` §6.3 CardReferenceDetailScreen (lines 288–292), §7.1 `displayNumber` (lines 308–311), Appendix A `FlowLayout` → `FlowRow` (line 674).
- **Files involved:**
  - `ui/reference/CardReferenceDetailScreen.kt` — image (11:19), name + suit + display number (e.g. "⭐ Major Arcana • I"), Upright (up-arrow, green accent), Reversed (down-arrow, orange accent), Keywords via `FlowRow`
  - `ui/components/FlowRow.kt` — wrapping chips (blue-tinted, ~12dp radius); use Compose `FlowRow`
  - Compose UI tests
- **Prior decisions:** keyword chips via Compose `FlowRow`; accent colors per SPEC (green upright / orange reversed). Full palette polish is Epic 7 — use sensible accents now.
- **State of the world:** suit → list navigation exists (ISSUE_02); detail is a stub.

## Output Format

A single PR containing:

- [ ] `CardReferenceDetailScreen` with all sections; `FlowRow` chips
- [ ] Navigation list → detail renders the selected card
- [ ] UI tests: detail shows name + upright + reversed; chips render for each keyword

## Examples

**UI test that should pass:**
```kotlin
@Test fun detail_shows_sections_and_keyword_chips() {
    composeRule.setContent { CardReferenceDetailScreen(card = magician) }
    composeRule.onNodeWithTag("uprightSection").assertIsDisplayed()
    composeRule.onNodeWithTag("reversedSection").assertIsDisplayed()
    magician.keywords.forEach { composeRule.onNodeWithText(it).assertExists() }
}
```

## Constraints

**Scope fence:** This closes Epic 6 — no drawing, no new data. Full theming/a11y
polish is Epic 7.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Full reference browse (suit → list → detail) is
demoable and offline.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Components ≥60% (§5); detail sections + chips tested.
- [ ] KDoc on `FlowRow` + detail composable.
- [ ] PR includes `Refs #6` and `Closes #33`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `reference`, `ui`
