## Role

You are a Kotlin persistence engineer porting a SwiftData model to Room with a
resilient, crash-proof database initialization.

## Goal

Implement the `CardPull` `@Entity`, `CardPullDao`, and `WristArcanaDatabase` (with
resilient init: destructive recreate → in-memory last resort) as an
application-scoped singleton.

## Context

- **Parent epic:** #2
- **Predecessor issue(s):** #14 (models). Independent of ISSUE_03/04 but file after ISSUE_01.
- **SPEC section:** `plans/SPEC.md` §7.4 persistence (lines 345–367), §10.2 history query caps (lines 457–465), §12 constants (lines 513–524).
- **Files involved:**
  - `data/db/CardPull.kt` — `@Entity` (`id` PK String/UUID, `date` epoch, `cardName`, `deckName`, `cardImageName`, `cardDescription`, `note: String?`) + non-persisted `hasNote`/`truncatedNote`
  - `data/db/CardPullDao.kt` — `insert`, `recent(limit)` (`ORDER BY date DESC LIMIT`), `oldest(limit)` (`ASC`), `delete`, `deleteByIds(ids)`, `deleteAll`, `count`; `Flow<List<CardPull>>` where it simplifies the VM
  - `data/db/WristArcanaDatabase.kt` — single-entity Room DB, resilient init, app-scoped singleton built in `WristArcanaApp`
  - DAO tests (Robolectric or in-memory Room)
- **Prior decisions:** decode/store `id` as String; resilient init mirrors the original's SwiftData fallback chain; one app-scoped DB instance to avoid Tile/Activity lock contention (§7.4).
- **State of the world:** models exist; no persistence yet.

## Output Format

A single PR containing:

- [ ] `CardPull` entity + computed helpers; `CardPullDao`; `WristArcanaDatabase` with resilient init + singleton provider
- [ ] `WristArcanaApp` (Application) builds the DB singleton (if not already created in Epic 1)
- [ ] DAO tests: insert + `recent(100)` ordering, `oldest` ordering, `deleteByIds`, `deleteAll`, `count`; `hasNote`/`truncatedNote` logic; simulated open-failure falls back without crashing
- [ ] No history UI (Epic 4), no draw save call site (Epic 3)

## Examples

**Tests that should pass:**
```kotlin
@Test fun recent_returns_newest_first_capped() {
    (1..120).forEach { dao.insert(pull(date = it.toLong())) }
    val recent = dao.recent(100)
    assertEquals(100, recent.size)
    assertEquals(120L, recent.first().date)   // newest first
}
@Test fun hasNote_false_when_blank() { assertFalse(pull(note = "   ").hasNote) }
```

## Constraints

**Scope fence:** Do not wire the draw→save path (Epic 3) or any history screen
(Epic 4). No storage monitor (Epic 4).

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches (the resilient-init fallback must log each step, not
> silently swallow), no `@Ignore`d tests without an issue reference, no lowering
> thresholds. Fix the root cause. The only exception is the documented 4-line
> escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf /
> generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Persistence is available app-wide; draw + history epics
can read/write pulls.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Model/DAO coverage meets §5 (entity logic 95–100%, DAO via instrumented/Robolectric tests).
- [ ] KDoc on DAO queries + DB init.
- [ ] PR includes `Refs #2` and `Closes #18`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `data`, `persistence`
