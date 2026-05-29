## Role

You are a Kotlin data engineer wiring kotlinx.serialization decoding of a bundled
JSON resource with strict validation and graceful fallbacks.

## Goal

Import `DecksData.json` verbatim into `res/raw/decks_data.json` and implement
`DeckRepository.loadDecks()` to decode, validate (1 deck × exactly 78 cards,
non-empty fields), and fall back to `TarotDeck.fallback` on any failure.

## Context

- **Parent epic:** #2
- **Predecessor issue(s):** #14 (models + interfaces + `DeckError`).
- **SPEC section:** `plans/SPEC.md` §7.2 JSON schema (lines 318–324), §7.5 `DeckRepository` (lines 370–379), §8.1 `getRandomCard` (lines 393–407 — interface only here).
- **Files involved:**
  - `app/src/main/res/raw/decks_data.json` — verbatim copy from the original's `Resources/DecksData.json`
  - `data/repo/DeckRepository.kt` — real `loadDecks()`, `getCurrentDeck()`, `getRandomCard(deck)` (RNG injected; the RNG impl itself is Epic 3 — accept the interface)
  - test fixtures: malformed JSON (wrong count, empty field, missing file)
- **Prior decisions:** `res/raw` over `assets/` (Appendix B). kotlinx.serialization. Validation throws/falls back per the exact `DeckError` cases. **Do not edit JSON content.**
- **State of the world:** models + stub repos exist (ISSUE_01).

## Output Format

A single PR containing:

- [ ] `res/raw/decks_data.json` (byte-for-byte the original's content)
- [ ] `DeckRepository` real decode + validation + fallback; `getCurrentDeck()` returns the `DEFAULT_DECK_ID` deck or fallback
- [ ] Tests: valid JSON → 1 deck × 78 cards; each malformed fixture → `TarotDeck.fallback` (+ correct `DeckError` logged)
- [ ] No images, no Room, no UI

## Examples

**Tests that should pass:**
```kotlin
@Test fun loads_one_deck_of_78() {
    val decks = repo.loadDecks()
    assertEquals(1, decks.size); assertEquals(78, decks.first().cards.size)
}
@Test fun bad_count_falls_back() {
    val decks = repoWith("deck_with_77_cards.json").loadDecks()
    assertEquals(TarotDeck.fallback.id, decks.first().id)
}
```

## Constraints

**Scope fence:** `CardRepository` (reference browser) is ISSUE_03; images +
resId map are ISSUE_04; Room is ISSUE_05. The RNG implementation is Epic 3 —
depend only on `RandomGeneratorProtocol`. Do not modify the JSON content.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> empty/`runCatching {}` catches that swallow errors (validation must log the
> specific `DeckError`, not silently eat it), no `@Ignore`d tests without an issue
> reference, no lowering thresholds. Fix the root cause. The only exception is the
> documented 4-line escape hatch (third-party-SDK bug / OS-version compat /
> benchmarked-perf / generated code) with reason, reference URL, alternative
> considered, and review date.

**Tracer-code invariant:** A real deck now loads offline; downstream epics can
consume it.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Repository coverage 90–100% (§5); happy path + all malformed fixtures tested.
- [ ] KDoc on `DeckRepository` public methods.
- [ ] PR includes `Refs #2` and `Closes #15`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `data`
