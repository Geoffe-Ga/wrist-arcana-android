## Role

You are a Kotlin/Compose engineer completing note management in the history
detail screen, including destructive deletion with confirmation.

## Goal

Wire note add/edit/delete into `HistoryDetailScreen` (delete behind a delete-note
confirmation), persisting changes to the selected `CardPull` and reloading
history.

## Context

- **Parent epic:** #5
- **Predecessor issue(s):** #29 (note save path) and Epic 4 ISSUE_02 (`HistoryDetailScreen`).
- **SPEC section:** `plans/SPEC.md` §6.2 HistoryDetail note management (lines 268–270), §10.2 note CRUD (lines 462–465), §9 (lines 429–441).
- **Files involved:**
  - `viewmodel/HistoryViewModel.kt` — `startAddingNote`, `saveNote`, `deleteNote`, `dismissNoteEditor`, `isEditingExistingNote`; fetch pull by id → update note → persist → reload
  - `ui/history/HistoryDetailScreen.kt` — add/edit/delete note UI + delete-note confirmation dialog; open `NoteEditorScreen`
  - VM + UI tests
- **Prior decisions:** reuse `NoteInputSanitizer` + `NoteEditorScreen`; delete requires confirmation; editing fetches by id, updates, persists, reloads.
- **State of the world:** draw-flow note CRUD exists (ISSUE_02); history detail has a placeholder note section.

## Output Format

A single PR containing:

- [ ] Note add/edit/delete in `HistoryViewModel` + `HistoryDetailScreen`
- [ ] Delete-note confirmation dialog
- [ ] VM tests (edit existing, delete nulls note, reload reflects change) + UI test (edit → save → shown; delete → confirm → gone)

## Examples

**VM test that should pass:**
```kotlin
@Test fun deleteNote_clears_and_reloads() = runTest {
    fakeDao.seed(1, note = "keep me"); vm.loadHistory()
    val p = vm.uiState.value.pulls.first(); vm.selectPull(p)
    vm.deleteNote()
    assertNull(fakeDao.byId(p.id)!!.note)
    assertFalse(vm.uiState.value.pulls.first().hasNote)
}
```

## Constraints

**Scope fence:** This closes Epic 5 — no new note surfaces beyond draw + history
detail. Don't touch multi-select/clear-all (Epic 4 ISSUE_04) beyond reuse.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Full note lifecycle works from both entry points; the
rest of history is unaffected.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM 95–100% (§5); add/edit/delete + confirm tested.
- [ ] KDoc on the note CRUD methods.
- [ ] PR includes `Refs #5` and `Closes #30`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `notes`
