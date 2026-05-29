## Epic Summary

Add note-taking to readings: the `NoteInputSanitizer` (exact port of the
original's rules), a `NoteEditorScreen` with a live character counter, and note
CRUD wired into both the draw flow (`CardDisplayScreen`) and history
(`HistoryDetailScreen`). Covers SPEC §9 (sanitizer) and the note portions of §6.2.

## Scope

**In scope:**
- `NoteInputSanitizer`: `MAX_CHARACTERS=500`, `sanitize` (trim → strip control chars except `\n`/`\t` → truncate 500 → collapse `\n{3,}`→`\n\n`), `isValid`, `remainingCharacters`.
- `NoteEditorScreen`: multiline input, sentence capitalization, live remaining-character counter, Save disabled when invalid (empty after trim or >500).
- Note CRUD into the draw flow: add/edit a note on the `CardPull` created by the current draw (persist + reload).
- Note CRUD into `HistoryDetailScreen`: add/edit/delete with a delete-note confirmation.

**Out of scope:**
- The draw flow and history detail screens themselves (Epics 3 & 4 — this epic wires notes *into* them).
- Theming/a11y polish (Epic 7).

## Success Criteria

The epic is done when:

- [ ] `NoteInputSanitizer` passes table tests for trim, control-char stripping (keeps `\n`/`\t`), 500-truncation, `\n{3,}`→`\n\n`, `isValid`, `remainingCharacters`.
- [ ] Editor shows a live counter, disables Save when invalid; empty-after-sanitize saves `note = null`.
- [ ] A note added from the draw's `CardDisplayScreen` persists to that `CardPull` and survives reload.
- [ ] History detail supports add/edit/delete note with a delete confirmation.
- [ ] Child issues closed; sanitizer 95–100% (§5).

## Child Issues

- [ ] #28 — Add NoteInputSanitizer + NoteEditorScreen with live counter
- [ ] #29 — Wire note add/edit persistence into the draw flow
- [ ] #30 — Wire note add/edit/delete into HistoryDetailScreen

## Sequencing Notes

- **Blocks:** nothing downstream.
- **Unblocked by:** Epic 3 (`CardDisplayScreen` + `CardPull` from draw) and Epic 4 (`HistoryDetailScreen`). Sanitizer itself only needs Epic 1.

## SPEC Reference

[`plans/SPEC.md`](../plans/SPEC.md) §9 (lines 429–441), §6.2 NoteEditor (lines 272–276), §6.1 note section (lines 246–252).

## Labels

`epic`, `spec-decomposition`, `notes`
