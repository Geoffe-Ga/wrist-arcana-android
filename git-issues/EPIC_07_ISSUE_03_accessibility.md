## Role

You are a Wear OS accessibility engineer making an app fully usable with
TalkBack.

## Goal

Add `contentDescription`/semantics to every interactive element, merge history
rows into single semantic nodes, and verify the app reads coherently under
TalkBack.

## Context

- **Parent epic:** #7
- **Predecessor issue(s):** #35 (final layouts). This closes Epic 7.
- **SPEC section:** `plans/SPEC.md` §11 accessibility (lines 506–509).
- **Files involved:**
  - all interactive composables under `ui/**` — semantics labels (DRAW = "Draw a tarot card", card image = "Tarot card: <name>", etc.)
  - `ui/components/HistoryRow.kt` — merge descendant semantics into one node
  - Compose semantics tests (assert merged nodes + labels)
- **Prior decisions:** parity work, not optional; labels mirror the original's intent. Verify with TalkBack.
- **State of the world:** themed, responsive screens exist (ISSUE_01/02).

## Output Format

A single PR containing:

- [ ] Semantics labels on every interactive element
- [ ] History rows merged into single semantic nodes
- [ ] Compose semantics tests asserting labels + merging
- [ ] A short PR note on the manual TalkBack pass performed
- [ ] No behavior changes

## Examples

**Test that should pass:**
```kotlin
@Test fun draw_button_has_semantics_label() {
    composeRule.onNodeWithContentDescription("Draw a tarot card").assertHasClickAction()
}
@Test fun history_row_is_single_merged_node() {
    composeRule.onNodeWithTag("historyRow", useUnmergedTree = false).assert(hasContentDescription())
}
```

## Constraints

**Scope fence:** No theming/layout changes (ISSUE_01/02) beyond adding semantics.
No new features. This is the final polish issue for Epic 7.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** The whole app remains functional and is now
screen-reader navigable.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Semantics tests pass; manual TalkBack pass noted in the PR.
- [ ] No coverage regression.
- [ ] PR includes `Refs #7` and `Closes #36`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `polish`, `accessibility`
