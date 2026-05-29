## Role

You are a Wear OS engineer extracting shared domain logic and scaffolding a Tile
service.

## Goal

Extract a shared `DrawUseCase` (draw + save) used by the Activity, the Tile, and
tests; refactor `CardDrawViewModel` onto it with **no behavior change**; and add a
`DrawCardTileService` shell rendering a DRAW button.

## Context

- **Parent epic:** #8
- **Predecessor issue(s):** none for this epic, but Epic 3 (draw logic) and Epic 2 (DB singleton) must be merged. Skeleton issue for Epic 8.
- **SPEC section:** `plans/SPEC.md` §10.5 (lines 477–489), §7.4 DB singleton (lines 362–367), §15 standalone/no-Siri (lines 577–594).
- **Files involved:**
  - `domain/DrawUseCase.kt` (new) — encapsulates select (no-repeat) + save `CardPull`, depends on repos/DAO/RNG interfaces
  - `viewmodel/CardDrawViewModel.kt` — delegate draw+save to `DrawUseCase` (regression-safe refactor)
  - `tile/DrawCardTileService.kt` — Tile shell with a DRAW button (no draw action yet)
  - `AndroidManifest.xml` — register the Tile service
  - regression tests proving Epic 3 behavior is unchanged
- **Prior decisions:** one shared code path for Activity/Tile/tests (the original shares `sharedModelContainer` for this); manual DI; app-scoped Room singleton.
- **State of the world:** in-app draw works (Epic 3); no shared use-case or Tile yet.

## Output Format

A single PR containing:

- [ ] `DrawUseCase` + `CardDrawViewModel` refactored onto it (behavior identical)
- [ ] `DrawCardTileService` shell + manifest registration
- [ ] Regression tests: existing draw VM tests still pass; a `DrawUseCase` unit test (no-repeat + save)
- [ ] No Tile draw action / deep-link yet (ISSUE_02)

## Examples

**Use-case test that should pass:**
```kotlin
@Test fun useCase_draws_and_saves() = runTest {
    val card = drawUseCase.drawAndSave()
    assertNotNull(card)
    assertEquals(1, fakeDao.inserted.size)
}
```

## Constraints

**Scope fence:** No Tile draw behavior/deep-link (ISSUE_02), no complication
(ISSUE_03). The refactor must not change the in-app draw UX.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Draw still works in-app; the Tile shell appears but is
inert until ISSUE_02. (The refactor lands *alongside* the Tile feature it enables
— not as a standalone refactor.)

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM/use-case 95–100% (§5); Epic 3 regression tests green.
- [ ] KDoc on `DrawUseCase`.
- [ ] PR includes `Refs #8` and `Closes #37`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `skeleton`, `tile`
