## Role

You are a Wear OS Compose + MVVM engineer scaffolding a scrollable history list
with an empty state.

## Goal

Create `HistoryViewModel` with its full UI-state shape and `HistoryScreen`
rendering a `ScalingLazyColumn` of placeholder `HistoryRow`s plus the empty state
("No Readings Yet" + sparkles), replacing the History placeholder page.

## Context

- **Parent epic:** #4
- **Predecessor issue(s):** none — skeleton issue for Epic 4. (Epic 2 must be merged: `CardPull` DAO.)
- **SPEC section:** `plans/SPEC.md` §6.2 HistoryScreen (lines 255–266), §10.2 `HistoryViewModel` (lines 457–465).
- **Files involved:**
  - `viewmodel/HistoryViewModel.kt` — state (`pulls`, `selectedPull`, `isInEditMode`, `selectedPullIds`, `showsPruningAlert`, `showsNoteEditor`, `editingNote`, …) as `StateFlow`; `loadHistory()` stub returning empty/seed
  - `ui/history/HistoryScreen.kt` — `ScalingLazyColumn` + empty state
  - `ui/components/HistoryRow.kt` — placeholder row (thumbnail + name + date)
  - VM + Compose smoke tests
- **Prior decisions:** `maxPullsToDisplay = 100`; most-recent-first. Note/edit-mode fields exist in state now but their behavior lands in later issues.
- **State of the world:** DAO exists (Epic 2); History page is a placeholder.

## Output Format

A single PR containing:

- [ ] `HistoryViewModel` with full state shape + stubbed `loadHistory()`
- [ ] `HistoryScreen` list + empty state; placeholder `HistoryRow`
- [ ] Tests: empty state renders with no pulls; list renders with seeded pulls
- [ ] No real DAO query, prune, multi-select, or detail (later issues)

## Examples

**UI test that should pass:**
```kotlin
@Test fun empty_state_when_no_pulls() {
    composeRule.setContent { HistoryScreen(state = HistoryUiState(pulls = emptyList())) }
    composeRule.onNodeWithText("No Readings Yet").assertIsDisplayed()
}
```

## Constraints

**Scope fence:** No real `loadHistory` query (ISSUE_02), no storage/prune
(ISSUE_03), no multi-select/clear-all (ISSUE_04), no note CRUD (Epic 5).

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** The History page renders a real (if empty) list backed
by a real VM.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM coverage 95–100% for present logic (§5); empty + populated states tested.
- [ ] KDoc on `HistoryViewModel`.
- [ ] PR includes `Refs #4` and `Closes #24`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `skeleton`, `history`
