## Role

You are a Kotlin domain-modeling engineer porting Swift value types to idiomatic
Kotlin data classes with exhaustive unit tests.

## Goal

Define `TarotCard`, the `Suit` enum, `TarotDeck`, the `DeckError` hierarchy, and
the repository interfaces (with fallback-returning stub impls), with computed
`displayNumber`/`fullDisplayName` matching the original exactly.

## Context

- **Parent epic:** #2
- **Predecessor issue(s):** none — skeleton issue for Epic 2. (Epic 1 must be merged.)
- **SPEC section:** `plans/SPEC.md` §7.1 models (lines 298–316), §7.5 repos (lines 369–387), §15 String-id coupling (lines 593–594). Original: `/Users/geoffgallinger/Projects/wrist-arcana` `Models/TarotCard.swift`/`TarotDeck.swift` (source of truth).
- **Files involved:**
  - `data/model/TarotCard.kt` — data class (`id: String`, name, imageName, suit, number, upright, reversed, keywords) + `Suit` enum + computed props + `emergencyFallback`
  - `data/model/TarotDeck.kt` — data class + `cardCount` + `fallback`/`riderWaite`
  - `data/repo/DeckRepositoryProtocol.kt` / `CardRepositoryProtocol.kt` + stub impls returning fallbacks
  - `data/repo/DeckError.kt` — sealed class (`fileNotFound`, `noDeckFound`, `invalidDeckSize`, `invalidCardData`, `loadFailed`, `notFound`)
- **Prior decisions:** decode `id` as **String** (not UUID). `Suit` carries `icon`, `cardCount`, `sortOrder` (Major=0, Swords=1, Wands=2, Pentacles=3, Cups=4). kotlinx.serialization `@Serializable` on the models.
- **State of the world:** module + pager exist (Epic 1); no data layer yet.

## Output Format

A single PR containing:

- [ ] Model + enum + deck + error files above; `@Serializable` annotations
- [ ] Repo interfaces + stub implementations returning `TarotDeck.fallback` / Fool card
- [ ] Unit tests covering `displayNumber` (Major Roman numerals 0…XXI; minors Ace/2–10/Page/Knight/Queen/King via number 1/11/12/13/14), `fullDisplayName`, suit counts + sort order, `emergencyFallback`
- [ ] No JSON loading, no images, no Room (later issues)

## Examples

**Test that should pass:**
```kotlin
@Test fun displayNumber_maps_major_and_minor() {
    assertEquals("I", magician.displayNumber)        // Major #1 → Roman
    assertEquals("Ace", swordsAce.displayNumber)      // minor #1 → Ace
    assertEquals("Page", swordsPage.displayNumber)    // minor #11 → Page
}
@Test fun suits_sorted() {
    assertEquals(listOf(MAJOR_ARCANA, SWORDS, WANDS, PENTACLES, CUPS), Suit.entries.sortedBy { it.sortOrder })
}
```

## Constraints

**Scope fence:** No real JSON decode, image resolution, or persistence — stubs
return fallbacks only. Those are ISSUE_02/03/04/05. Port the display mappings
**exactly** from the original; if SPEC and original disagree, the original wins —
file a SPEC-fix note.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)` to silence detekt/lint, no `// ktlint-disable`, no `!!`, no
> `@Suppress("UNCHECKED_CAST")`, no error-swallowing catches, no `@Ignore`d tests
> without an issue reference, no lowering thresholds. Fix the root cause. The only
> exception is the documented 4-line escape hatch (third-party-SDK bug /
> OS-version compat / benchmarked-perf / generated code) with reason, reference
> URL, alternative considered, and review date.

**Tracer-code invariant:** Stub repos must satisfy the interfaces so downstream UI
epics can compile against them before real loading lands.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Model coverage 95–100% (§5); `displayNumber`/`fullDisplayName` tested across all card categories.
- [ ] KDoc on public models + computed props.
- [ ] PR includes `Refs #2` and `Closes #14`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `skeleton`, `data`
