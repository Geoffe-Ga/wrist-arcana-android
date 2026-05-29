## Epic Summary

Build the offline data foundation: domain models (`TarotCard`/`TarotDeck`),
verbatim `DecksData.json` + 78 card images, repositories with validation and
fallbacks, and the Room `CardPull` entity/DAO/DB with resilient init. After this
epic the app can load all 78 cards from bundled resources with zero network and
persist pulls. Covers SPEC §7 in full.

## Scope

**In scope:**
- `TarotCard` (decode `id` as **String**), `Suit` enum (icon/cardCount/sortOrder), `TarotDeck`; computed `displayNumber`/`fullDisplayName`; `emergencyFallback`/`fallback`.
- `DecksData.json` copied verbatim → `res/raw/decks_data.json`; kotlinx.serialization decode.
- `DeckRepository`/`CardRepository` behind interfaces, with validation (≥1 deck; exactly 78 cards; non-empty fields) + `DeckError` cases + fallbacks.
- 78 card images imported into `res/drawable-*`; a name→drawable-resId map; asset-integrity test (all 78 `imageName`s resolve).
- Room `CardPull` `@Entity`, `CardPullDao`, `WristArcanaDatabase` (resilient init: destructive recreate → in-memory last resort), app-scoped singleton.

**Out of scope:**
- Drawing/selecting cards (Epic 3), history UI (Epic 4), reference UI (Epic 6).
- `CardImage` composable rendering (Epic 3/7) — this epic only delivers the resId map + integrity test.

## Success Criteria

The epic is done when:

- [ ] `DeckRepository.loadDecks()` returns 1 deck × 78 valid cards from bundled JSON; malformed fixtures fall back to `TarotDeck.fallback`.
- [ ] `CardRepository` returns all 78 cards sorted by `suit.sortOrder` then `number`, filters by suit, looks up by id, returns 5 sorted suits.
- [ ] Asset-integrity test proves every `imageName` in the JSON resolves to a real drawable (the "78 present" gate).
- [ ] Room DAO insert/recent(100)/oldest/delete/deleteByIds/deleteAll/count all pass; DB survives a simulated open failure.
- [ ] All child issues are closed; coverage meets §5 (models/repos 90–100%).

## Child Issues

- [ ] #14 — Add TarotCard/Suit/TarotDeck models, DeckError, and repo interfaces
- [ ] #15 — Load DecksData.json and implement DeckRepository with validation+fallback
- [ ] #16 — Implement CardRepository (sorted getAll/getCards/getCard/getSuits)
- [ ] #17 — Import 78 card images + name->resId map + asset-integrity test
- [ ] #18 — Add Room CardPull entity/DAO/DB with resilient init

## Sequencing Notes

- **Blocks:** Epics 3, 4, 5, 6, 9 (all consume models/repos/DB).
- **Unblocked by:** Epic 1 (module must exist).
- Asset issue decides per-density vs single `drawable-nodpi` (Appendix B) after on-watch memory check.

## SPEC Reference

[`plans/SPEC.md`](../plans/SPEC.md) §7 (lines 296–388), §12 constants (lines 513–524), §15 memory/data-coupling (lines 577–594), Appendix A file map.

## Labels

`epic`, `spec-decomposition`, `data`
