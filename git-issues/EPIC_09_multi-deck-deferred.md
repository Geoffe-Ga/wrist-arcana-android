## Epic Summary

**Deferred / flag-gated.** Build the multi-deck selection code path behind
`FeatureFlags.MULTI_DECK_ENABLED` (default **false**) so it is code-complete but
never surfaced in v1.0 — the IAP future-work hook. Covers SPEC §10.4 and §16.9.

> **`future-work` label:** this epic and its children carry `future-work` so the
> Ralph picker (`pick-next.sh`) skips them. Unpark by removing the label when
> multi-deck is greenlit.

## Scope

**In scope:**
- `DeckSelectionViewModel`: state (`availableDecks`, `selectedDeckId`, `errorMessage`) + `loadDecks()`/`selectDeck(id)`.
- `DeckSelectionScreen` surfaced **only** when `FeatureFlags.MULTI_DECK_ENABLED == true`.
- Wiring deck selection into the draw/reference paths, gated by the flag.

**Out of scope (v1.0 product invariant):**
- Exposing any of this with the flag on by default — it stays hidden.
- IAP/purchase flow, additional deck content/art — separate future SPEC.

## Success Criteria

The epic is done when:

- [ ] `DeckSelectionViewModel` loads decks and selects by id (unit-tested).
- [ ] With the flag **off** (default), no deck-selection UI is reachable anywhere (parity invariant holds).
- [ ] With the flag **on** (test-only), deck selection surfaces and switches the active deck.
- [ ] Child issues closed; the v1.0 build ships with the flag off.

## Child Issues

- [ ] #40 — Add DeckSelection VM+screen behind MULTI_DECK_ENABLED
- [ ] #41 — Wire deck selection into draw/reference (flag-gated)

## Sequencing Notes

- **Deferred:** `future-work` keeps the Ralph picker off this until unparked.
- **Unblocked by:** Epic 2 (multi-deck repos/models) and a stable draw/reference path (Epics 3, 6).

## SPEC Reference

[`plans/SPEC.md`](../plans/SPEC.md) §10.4 (lines 472–475), §16.9 (lines 624–625), §12 `MULTI_DECK_ENABLED` (line 523), §2 non-goals (lines 65–71).

## Labels

`epic`, `spec-decomposition`, `future-work`, `multi-deck`
