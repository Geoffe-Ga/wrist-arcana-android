## Role

You are a Kotlin/Compose engineer wiring note persistence into the draw flow's
card detail screen.

## Goal

Wire note add/edit into `CardDisplayScreen` so a note typed there persists to the
`CardPull` created by the current draw and survives reload.

## Context

- **Parent epic:** #5
- **Predecessor issue(s):** #28 (sanitizer + editor) and Epic 3 ISSUE_04 (`CardDisplayScreen` + `currentCardPull`).
- **SPEC section:** `plans/SPEC.md` §6.1 note section (lines 246–252), §9 saving rules (lines 439–441).
- **Files involved:**
  - `viewmodel/CardDrawViewModel.kt` (or a shared note path) — `startAddingNote`, `saveNote` (sanitize → empty ⇒ `note=null` ⇒ update the pull via DAO ⇒ reload)
  - `ui/draw/CardDisplayScreen.kt` — replace the placeholder note affordance: "Add Note" / bordered note box + "Edit Note"; open `NoteEditorScreen`
  - VM + UI tests
- **Prior decisions:** sanitize on save; empty-after-sanitize stores `null`; persist to the existing `CardPull` (don't create a new row).
- **State of the world:** sanitizer/editor exist (ISSUE_01); display screen has a non-functional note placeholder (Epic 3).

## Output Format

A single PR containing:

- [ ] Note add/edit wired into the draw's `CardDisplayScreen` with real persistence
- [ ] `saveNote` sanitizes + nulls empty + updates the pull + reloads
- [ ] VM tests (save sanitizes, empty→null, persists to the right id) + UI test (add note → reopen shows it)
- [ ] No history-detail note CRUD (ISSUE_03)

## Examples

**VM test that should pass:**
```kotlin
@Test fun saveNote_persists_sanitized_and_nulls_empty() = runTest {
    vm.drawCard(); advanceTimeBy(500); runCurrent()
    val id = vm.uiState.value.currentCardPull!!.id
    vm.saveNote("  hello \n\n\n\n world  ")
    assertEquals("hello\n\nworld", fakeDao.byId(id)!!.note)
    vm.saveNote("   ")
    assertNull(fakeDao.byId(id)!!.note)
}
```

## Constraints

**Scope fence:** History-detail note CRUD is ISSUE_03. Don't reshape the display
screen beyond the note section.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Notes now persist from the draw flow without breaking
the draw/preview/detail loop.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM 95–100% (§5); save/sanitize/null/persist paths tested.
- [ ] KDoc on the note methods.
- [ ] PR includes `Refs #5` and `Closes #29`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `notes`
