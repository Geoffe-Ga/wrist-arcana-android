## Role

You are a Wear OS Compose engineer building modal-layered result screens with
full-bleed card art.

## Goal

Build `CardPreviewScreen` (full-bleed art on near-black) and `CardDisplayScreen`
(image 11:19 + name + upright meaning + note-section placeholder), with
preview→detail navigation after a successful draw.

## Context

- **Parent epic:** #3
- **Predecessor issue(s):** #21 (a successful draw now yields `currentCard`/`currentCardPull`).
- **SPEC section:** `plans/SPEC.md` §6.1 CardPreview/CardDisplay (lines 241–252), §11 aspect/placeholder (lines 499–505). Original: `CardPreviewView.swift`, `CardDisplayView.swift`.
- **Files involved:**
  - `ui/draw/CardPreviewScreen.kt` — black ~90% bg, centered card at 11:19, tappable → detail; Done + info actions
  - `ui/draw/CardDisplayScreen.kt` — image (11:19), name (serif ~20sp), upright meaning; **note section placeholder** ("Add Note" button that is wired in Epic 5); Done dismisses
  - `ui/components/CardImage.kt` — renders by `imageName` via the resId map (basic; gradient placeholder polish is Epic 7)
  - Compose UI tests for the navigation
- **Prior decisions:** show preview on success, then optional detail. Note persistence is Epic 5 — leave a non-functional "Add Note" affordance here.
- **State of the world:** draw saves a pull (ISSUE_03); no result UI yet.

## Output Format

A single PR containing:

- [ ] `CardPreviewScreen` + `CardDisplayScreen` + `CardImage`
- [ ] Wiring: successful draw → preview; preview tap/info → detail; Done dismisses (`dismissCard()`)
- [ ] Compose UI tests: draw → preview shows art; preview → detail shows name + upright
- [ ] Note section is a visible placeholder only (no persistence)

## Examples

**UI test that should pass:**
```kotlin
@Test fun draw_shows_preview_then_detail() {
    composeRule.onNodeWithContentDescription("Draw a tarot card").performClick()
    composeRule.waitUntil { composeRule.onAllNodesWithTag("cardPreview").fetchSemanticsNodes().isNotEmpty() }
    composeRule.onNodeWithTag("cardPreview").performClick()
    composeRule.onNodeWithTag("uprightMeaning").assertIsDisplayed()
}
```

## Constraints

**Scope fence:** No note save/edit (Epic 5). No full theming/placeholder polish
(Epic 7) — minimal `CardImage` is enough. No storage dialog (ISSUE_05).

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** The full draw→preview→detail loop is demoable.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Compose UI tests cover preview + detail navigation; component coverage ≥60% (§5).
- [ ] KDoc on the new composables' public params.
- [ ] PR includes `Refs #3` and `Closes #22`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `draw`, `ui`
