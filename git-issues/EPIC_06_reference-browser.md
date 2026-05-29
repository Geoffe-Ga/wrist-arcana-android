## Epic Summary

Build the offline reference browser: browse all 78 cards by suit without drawing.
Suit list → card list → reference detail showing upright/reversed meanings and
keyword chips. Covers SPEC §6.3 (reference flow) and §10.3
(`CardReferenceViewModel`).

## Scope

**In scope:**
- `CardReferenceViewModel`: state (`suits`, `selectedSuit`, `cardsInSuit`, `selectedCard`) + `loadSuits`/`selectSuit`/`selectCard`/`deselectCard`/`cardCount`.
- `CardReferenceScreen`: 5 suits in fixed order (Major 22 ⭐, Swords 14 ⚔️, Wands 14 🪄, Pentacles 14 🪙, Cups 14 🏆) with icon + name + count.
- `CardListScreen`: cards in the chosen suit sorted by number (thumbnail + full display name).
- `CardReferenceDetailScreen`: image, name + suit + display number (e.g. "⭐ Major Arcana • I"), Upright (up-arrow, green), Reversed (down-arrow, orange), Keywords as wrapping chips.
- `FlowRow` component for the keyword chips (blue-tinted, ~12dp radius).

**Out of scope:**
- Drawing (Epic 3) — reference is browse-only.
- Full theme palette / a11y polish (Epic 7) — minimal styling here, polish later.

## Success Criteria

The epic is done when:

- [ ] Reference screen lists the 5 suits in fixed order with correct counts and icons.
- [ ] Selecting a suit lists its cards sorted by number; selecting a card opens detail.
- [ ] Detail renders image, name + suit + display number, Upright + Reversed sections, and keyword chips via `FlowRow`.
- [ ] Navigation suit → list → detail works (Compose UI tests).
- [ ] Child issues closed; VM 95–100% (§5).

## Child Issues

- [ ] #31 — Add CardReferenceViewModel + suit list screen skeleton
- [ ] #32 — Add CardListScreen (cards sorted by number)
- [ ] #33 — Add CardReferenceDetailScreen + FlowRow keyword chips

## Sequencing Notes

- **Blocks:** nothing downstream.
- **Unblocked by:** Epic 2 (`CardRepository` + image resId map). Parallel-safe with Epics 3–5.

## SPEC Reference

[`plans/SPEC.md`](../plans/SPEC.md) §6.3 (lines 277–293), §10.3 (lines 467–470), §7.1 displayNumber/fullDisplayName (lines 300–312).

## Labels

`epic`, `spec-decomposition`, `reference`
