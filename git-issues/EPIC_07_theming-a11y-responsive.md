## Epic Summary

The polish pass: apply the full theme palette, reproduce the original's
percentage-of-screen responsive sizing across round/square/small Wear devices,
and make every interactive element accessible (semantics + TalkBack). This epic
adds **no new features** — it tightens what Epics 3–6 already built. Covers SPEC
§11.

## Scope

**In scope:**
- `Theme.kt`: purple→blue primary gradient (TL→BR), black card background, typography (title ~32sp bold serif, card name ~20sp semibold serif, body ~14sp), 8/16/24dp spacing; Wear `MaterialTheme`. Applied across all screens.
- Responsive sizing via `BoxWithConstraints`: DRAW button (~70% width, clamp 120–160dp, ≤~60% height), title ~12% height; card aspect `aspectRatio(11f/19f)`; account for `TimeText`/inset.
- `CardImage` placeholder: purple/blue gradient box (11:19) with icon + card name when a drawable can't resolve.
- Accessibility: `contentDescription`/semantics on every interactive element (DRAW = "Draw a tarot card", card image = "Tarot card: <name>"); history rows merge semantics; verify with TalkBack.

**Out of scope:**
- New screens or behaviors — strictly polish.
- The Tile (Epic 8) and multi-deck (Epic 9).

## Success Criteria

The epic is done when:

- [ ] The theme palette + typography match the original across all screens.
- [ ] DRAW button and title scale correctly on round, square, and small-screen Wear targets; cards hold 11:19.
- [ ] Unresolved drawables render the gradient placeholder with the card name.
- [ ] Every interactive element has a semantics label; TalkBack reads the app coherently; history rows are single merged nodes.
- [ ] Child issues closed.

## Child Issues

- [ ] #34 — Implement Theme.kt palette + typography across screens
- [ ] #35 — Add responsive BoxWithConstraints sizing + CardImage placeholder
- [ ] #36 — Add accessibility semantics + TalkBack pass

## Sequencing Notes

- **Unblocked by:** Epics 3–6 (the screens it polishes must exist). Run late.
- Parallel-safe internally; each child touches presentation only.

## SPEC Reference

[`plans/SPEC.md`](../plans/SPEC.md) §11 (lines 493–509), §6.1 responsive button (lines 223–227), §15 round/square (lines 577–589).

## Labels

`epic`, `spec-decomposition`, `theming`
