## Role

You are a Wear OS Compose + MVVM engineer implementing multi-select editing and
destructive bulk actions with confirmation.

## Goal

Add edit-mode multi-select (toggle rows, batch delete) and a "Clear All" action
with a destructive confirmation dialog to History.

## Context

- **Parent epic:** #4
- **Predecessor issue(s):** #26 (storage/prune) — file last in Epic 4.
- **SPEC section:** `plans/SPEC.md` §6.2 management/edit-mode (lines 261–263), §10.2 multi-select methods (lines 462–465).
- **Files involved:**
  - `viewmodel/HistoryViewModel.kt` — `enterEditMode`/`exitEditMode`, `toggleSelection`, `isSelected`, `deleteMultiplePulls(ids)`, `clearAllHistory()`, `deletePull(p)`
  - `ui/history/HistoryScreen.kt` — Select action, per-row checkbox in edit mode, "Delete N items" bottom action, "Clear All" + destructive confirm dialog, Done exits edit mode
  - `ui/components/HistoryRow.kt` — checkbox affordance in edit mode
  - VM + Compose UI tests
- **Prior decisions:** batch delete via `deleteByIds`; clear-all wipes via `deleteAll` behind a destructive confirm.
- **State of the world:** list/detail/prune exist (ISSUE_02/03).

## Output Format

A single PR containing:

- [ ] Edit-mode state + toggle/select/delete-multiple/clear-all in the VM
- [ ] UI: Select/Done, row checkboxes, "Delete N items", "Clear All" + confirmation
- [ ] VM tests (toggle, batch delete, clear-all) + UI tests (enter edit mode → select → delete; clear-all confirm)

## Examples

**VM test that should pass:**
```kotlin
@Test fun delete_multiple_removes_selected() = runTest {
    fakeDao.seed(5); vm.loadHistory(); vm.enterEditMode()
    val ids = vm.uiState.value.pulls.take(2).map { it.id }.toSet()
    ids.forEach(vm::toggleSelection)
    vm.deleteMultiplePulls(ids)
    assertEquals(3, vm.uiState.value.pulls.size)
}
```

## Constraints

**Scope fence:** No note CRUD (Epic 5). Do not alter prune/storage logic
(ISSUE_03) beyond reuse.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** History gains bulk management without regressing
list/detail/prune.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM 95–100%, components ≥60% (§5); multi-select + clear-all tested incl. the destructive-confirm path.
- [ ] KDoc on the new VM methods.
- [ ] PR includes `Refs #4` and `Closes #27`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `edges`, `history`
