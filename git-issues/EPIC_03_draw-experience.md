## Epic Summary

Implement the core loop: tap DRAW → CSPRNG no-repeat selection → ~0.5s suspense →
save to history → haptic → card preview → full card display. This is the app's
headline feature. Covers SPEC §6.1 (draw flow), §8 (algorithms), §10.1
(`CardDrawViewModel`).

## Scope

**In scope:**
- `RandomGeneratorProtocol` + `SecureRandom` implementation.
- `CardDrawViewModel`: state (`currentCard`, `currentCardPull`, `isDrawing`, `showsStorageWarning`, `errorMessage`) + session `drawnThisSession` set.
- No-repeat algorithm (§8.1), cancellable 500ms suspense delay (§8.4), haptic on success, save `CardPull` (§8.2), post-draw storage check → warning dialog.
- `DrawButton` (responsive via `BoxWithConstraints`), `DrawCardScreen`, `CardPreviewScreen`, `CardDisplayScreen` (image/name/upright + note-section placeholder), preview→detail navigation.

**Out of scope:**
- Note persistence/editor (Epic 5 wires note CRUD into `CardDisplayScreen`).
- Full theme palette / a11y polish (Epic 7).
- Tile/quick-draw (Epic 8) — but extract draw+save so Epic 8 can share it (light touch here; the formal shared use-case lands in Epic 8).

## Success Criteria

The epic is done when:

- [ ] Tapping DRAW shows a card after ~500ms and persists a `CardPull`; navigating away mid-draw cancels cleanly.
- [ ] No-repeat invariant holds: across 78 draws every card appears exactly once, then the set resets (statistical test).
- [ ] A haptic fires on a successful draw; storage warning dialog appears when ≥80% used.
- [ ] Preview → detail navigation works; detail shows image (11:19), name, upright meaning.
- [ ] Child issues closed; VM coverage 95–100% (§5).

## Child Issues

- [ ] #19 — Add RandomGenerator + CardDrawViewModel state + DrawCardScreen skeleton
- [ ] #20 — Implement CSPRNG no-repeat selection algorithm
- [ ] #21 — Add suspense delay, haptic, and save-to-history on draw
- [ ] #22 — Add CardPreviewScreen + CardDisplayScreen with preview->detail nav
- [ ] #23 — Add post-draw storage warning dialog and error surfacing

## Sequencing Notes

- **Blocks:** Epic 5 (note CRUD into draw flow), Epic 8 (shared draw use-case).
- **Unblocked by:** Epic 2 (needs models, repos, `CardPull` DAO).
- Parallel-safe with Epic 6 (Reference) once Epic 2 lands.

## SPEC Reference

[`plans/SPEC.md`](../plans/SPEC.md) §6.1 (lines 221–252), §8 (lines 391–426), §10.1 (lines 449–456), §11 responsive sizing (lines 494–509).

## Labels

`epic`, `spec-decomposition`, `draw`
