## Epic Summary

Map the original's "Draw Tarot Card" App Intent to Wear OS: a **Tile** that draws
+ saves a card and deep-links into `CardDisplayScreen`, plus an optional
complication/app-shortcut. Requires extracting the draw+save logic into a shared
use-case so the Activity, Tile, and tests share one code path. Covers SPEC §10.5.

## Scope

**In scope:**
- Extract a shared `DrawUseCase` (draw + save) and refactor `CardDrawViewModel` to use it (no behavior change to Epic 3's flow).
- `DrawCardTileService`: a Tile showing a DRAW button; tapping draws via the shared use-case, persists the `CardPull`, renders the result inline, and deep-links into `CardDisplayScreen`.
- (Optional) a complication / app shortcut that launches straight into a draw.
- Use the application-scoped Room singleton so the Tile and Activity don't contend on the DB (SPEC §7.4).

**Out of scope:**
- Any change to the in-app draw UX (Epic 3 owns it; this epic only shares its logic).
- Voice/"hands-free" parity — Wear OS has no Siri analogue (SPEC §15); the Tile satisfies "draw without opening".

## Success Criteria

The epic is done when:

- [ ] Draw+save logic lives in one shared use-case used by the Activity, the Tile, and tests.
- [ ] The Tile draws + saves a `CardPull` and deep-links into `CardDisplayScreen`.
- [ ] No DB lock contention between Tile and Activity (shared singleton).
- [ ] Existing Epic 3 draw behavior is unchanged (regression tests green).
- [ ] Child issues closed.

## Child Issues

- [ ] #37 — Extract shared DrawUseCase + DrawCardTileService shell
- [ ] #38 — Tile draws+saves via use-case and deep-links to CardDisplay
- [ ] #39 — Add optional complication / app shortcut quick-draw

## Sequencing Notes

- **Blocks:** nothing.
- **Unblocked by:** Epic 3 (the draw logic it shares) and Epic 2 (DB singleton). Best run after Epic 3 is stable.

## SPEC Reference

[`plans/SPEC.md`](../plans/SPEC.md) §10.5 (lines 477–489), §7.4 DB singleton (lines 362–367), §15 no-Siri (lines 577–594), §3 App Intent row.

## Labels

`epic`, `spec-decomposition`, `tile`
