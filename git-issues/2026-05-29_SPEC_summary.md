# Wrist Arcana for Wear OS — Decomposition Summary

One-page restatement of [`plans/SPEC.md`](../plans/SPEC.md) (Draft v1.0). This is
the backlog trail: how the SPEC was sliced into epics and issues.

## What we're building

A native **Wear OS / Android** port of the watchOS tarot app *Wrist Arcana* —
faithful feature parity, not a redesign. Tap DRAW → cryptographically fair card
from the 78-card Rider–Waite deck → art + meaning → persistent history with
notes. Plus an offline reference browser for all 78 cards. Watch-only; **no phone
module**.

## Non-negotiable invariants (SPEC §1)

- **100% offline** — no network calls, ever. All 78 images + metadata ship in-app.
- **CSPRNG draws** — `SecureRandom` behind a `RandomGeneratorProtocol`.
- **No-repeat within a session** — each card appears once before any repeat, then reshuffle.
- **Persistent history** — capped/queried for watch perf; storage monitoring + prune at 80%.
- **~0.5s suspense delay** on each draw (cancellable).
- **Multi-deck built but hidden** behind `FeatureFlags.MULTI_DECK_ENABLED = false`.

## Stack (SPEC §3)

Kotlin · Jetpack Compose for Wear OS · Room · Coroutines + StateFlow · manual
constructor DI (interfaces) · kotlinx.serialization · `SecureRandom` · Gradle
(Kotlin DSL), single `:app` module · JUnit5 + MockK + Turbine + Compose UI test ·
ktlint + detekt + Android Lint · Kover.

## Source of truth

The original watchOS app at `/Users/geoffgallinger/Projects/wrist-arcana`. When
SPEC and original disagree, **the original wins** — file a SPEC-fix issue.
`DecksData.json` and the 78 card images are reused **verbatim**.

## Epic map (tracer-code order — skeleton first, demoable at every step)

| # | Epic | Outcome | SPEC |
|---|------|---------|------|
| 1 | Project skeleton & CI | Empty 3-page pager builds + launches; CI green; real quality scripts | §4, §14, §16.1 |
| 2 | Data layer | JSON + 78 images load offline; models, repos w/ validation+fallback; Room DAO/DB | §7 |
| 3 | Draw experience | CSPRNG no-repeat draw, suspense, haptic, save, preview + display | §6.1, §8, §10.1 |
| 4 | History | List/detail, multi-select delete, clear-all, storage monitor + prune | §6.2, §8.3, §10.2 |
| 5 | Notes | `NoteInputSanitizer`, editor, note CRUD into draw + history detail | §6.2, §9 |
| 6 | Reference browser | Suit list → card list → reference detail (upright/reversed/keywords) | §6.3, §10.3 |
| 7 | Theming, a11y & responsive | Theme palette, BoxWithConstraints sizing, semantics/TalkBack | §11 |
| 8 | Quick-draw surfaces | Tile (shared draw use-case) + optional complication | §10.5 |
| 9 | Multi-deck (deferred) | DeckSelection behind `MULTI_DECK_ENABLED` — `future-work` | §10.4, §16.9 |

## Cross-epic sequencing

- **Epic 1 is hand-built once** (bootstrap), then merged, before the Ralph loop runs. Ralph picks up from Epic 2.
- Epic 2 unblocks 3–6 (all need models + repos + DB).
- Epic 5 (Notes) blocks on Epic 3 (draw flow) + Epic 4 (history detail) existing.
- Epic 7 (Theming/a11y) is a late polish pass; safe to run after the feature epics land.
- Epic 8 (Tile) blocks on Epic 3 (the draw use-case it shares).
- Epic 9 (Multi-deck) is deferred — `future-work` label keeps the Ralph picker off it until unparked.

## Open questions (Appendix B) — defaults adopted, decided inside epics

- Per-density drawables vs single `drawable-nodpi` → **Epic 2 asset issue decides** after on-watch memory test.
- Hilt vs manual DI → **manual** (revisit only if Tile+Activity+tests wiring gets unwieldy — Epic 8).
- `res/raw` vs `assets/` for JSON → **`res/raw`** (simpler with kotlinx.serialization).
- Nav primitive (HorizontalPager vs SwipeDismissableNavHost) → **prototype in Epic 1**; default HorizontalPager.
