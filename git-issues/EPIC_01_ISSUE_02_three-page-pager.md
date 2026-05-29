## Role

You are a Wear OS Compose engineer wiring app navigation. You know
`androidx.wear.compose` `HorizontalPager`, swipe-to-dismiss interactions, and
`TimeText`.

## Goal

Replace the blank activity with a 3-page horizontal pager (Reference / Draw /
History) whose **default/initial page is Draw (index 1)**, each page showing
placeholder content, that swipes cleanly on a Wear emulator.

## Context

- **Parent epic:** #1
- **Predecessor issue(s):** #10 (Gradle module — must be merged first).
- **SPEC section:** `plans/SPEC.md` §6 navigation (lines 213–219), §15 pager-vs-swipe risk (lines 587–589), Appendix B nav choice (lines 685–686).
- **Files involved:**
  - `app/src/main/kotlin/com/wristarcana/ui/WristArcanaRoot.kt` — the pager host
  - `MainActivity.kt` — `setContent { WristArcanaRoot() }`
  - placeholder composables for the three pages (inline or tiny stubs under `ui/`)
- **Prior decisions:** default nav primitive is Wear Compose `HorizontalPager` (Appendix B). If swipe-to-dismiss conflicts with the pager, document the resolution in the PR.
- **State of the world:** module builds and launches a blank activity (ISSUE_01).

## Output Format

A single PR containing:

- [ ] `WristArcanaRoot.kt` with a 3-page `HorizontalPager`, `initialPage = 1`
- [ ] Three placeholder pages labeled "Reference" / "Draw" / "History"
- [ ] A Compose UI test asserting the default page is Draw and swiping reaches the other two
- [ ] `MainActivity` calls `WristArcanaRoot()`

## Examples

**Test that should pass after this issue lands:**
```kotlin
@Test fun pager_starts_on_draw_and_swipes_to_neighbors() {
    composeRule.setContent { WristArcanaRoot() }
    composeRule.onNodeWithText("Draw").assertIsDisplayed()      // index 1 default
    composeRule.onNodeWithText("Reference").performTouchInput { swipeRight() }
    composeRule.onNodeWithText("History").performTouchInput { swipeLeft() }
}
```

## Constraints

**Scope fence:** Placeholders only — no draw logic, history list, or reference
data (Epics 3/4/6). No theme palette work (Epic 7). Do not change build config
beyond adding the Wear Compose pager dependency if missing.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)` to silence detekt/lint, no `// ktlint-disable`, no `!!`, no
> `@Suppress("UNCHECKED_CAST")`, no empty/`runCatching {}` catches that swallow
> errors, no `@Ignore`d tests without an issue reference, no lowering thresholds.
> Fix the root cause. The only exception is the documented 4-line escape hatch
> (third-party-SDK bug / OS-version compat / benchmarked-perf / generated code)
> with reason, reference URL, alternative considered, and review date.

**Tracer-code invariant:** The app stays demoable — three swipeable pages. Later
epics swap each placeholder for a real screen without touching the pager host.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Compose UI test for default page + swipe passes.
- [ ] KDoc on `WristArcanaRoot`.
- [ ] PR includes `Refs #1` and `Closes #11`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `ui`
