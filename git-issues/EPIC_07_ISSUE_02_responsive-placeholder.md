## Role

You are a Wear OS Compose engineer making layouts responsive across round,
square, and small-screen watches.

## Goal

Reproduce the original's percentage-of-screen sizing via `BoxWithConstraints`
(DRAW button + title), enforce the 11:19 card aspect, and render the `CardImage`
gradient placeholder when a drawable can't resolve — across round/square/small
targets.

## Context

- **Parent epic:** #7
- **Predecessor issue(s):** #34 (theme tokens for the placeholder gradient).
- **SPEC section:** `plans/SPEC.md` §11 responsive + placeholder (lines 499–505), §6.1 button sizing (lines 223–227), §15 round/square + memory (lines 581–589).
- **Files involved:**
  - `ui/draw/DrawCardScreen.kt` / `ui/components/DrawButton.kt` — `BoxWithConstraints`: button ~70% width (clamp 120–160dp, ≤~60% height), title ~12% height; account for `TimeText`/inset
  - `ui/components/CardImage.kt` — `aspectRatio(11f/19f)`; purple/blue gradient placeholder (icon + card name) on unresolved drawable
  - UI tests across device configs where practical
- **Prior decisions:** `BoxWithConstraints` for percentage sizing; placeholder mirrors the original `CardImageView` fallback.
- **State of the world:** themed screens exist (ISSUE_01); sizing is not yet responsive; `CardImage` lacks the gradient fallback.

## Output Format

A single PR containing:

- [ ] Responsive DRAW button + title sizing via `BoxWithConstraints`
- [ ] `CardImage` enforces 11:19 and renders the gradient placeholder on miss
- [ ] UI tests / previews for round + square + small configs
- [ ] No new features

## Examples

**Test that should pass:**
```kotlin
@Test fun card_image_shows_placeholder_when_unresolved() {
    composeRule.setContent { CardImage(imageName = "does_not_exist", cardName = "The Fool") }
    composeRule.onNodeWithTag("cardImagePlaceholder").assertIsDisplayed()
    composeRule.onNodeWithText("The Fool").assertExists()
}
```

## Constraints

**Scope fence:** No a11y semantics pass (ISSUE_03). No behavior changes beyond
layout/placeholder.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Layouts adapt across watch shapes without breaking any
screen.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Components ≥60% (§5); placeholder + aspect tested.
- [ ] KDoc on `CardImage` placeholder behavior.
- [ ] PR includes `Refs #7` and `Closes #35`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `theming`
