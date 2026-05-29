## Role

You are a Kotlin engineer porting storage-capacity math and a destructive prune
flow with careful boundary testing.

## Goal

Implement `StorageMonitor` (full `StatFs` math, silent-zero on error) and the
History prune flow: on load, if storage ≥80% used, show a "Delete Oldest 50?"
dialog whose confirmation deletes the oldest 50 pulls.

## Context

- **Parent epic:** #4
- **Predecessor issue(s):** #25 (history load). This issue delivers the canonical `StorageMonitor` that Epic 3 ISSUE_05 depended on via interface.
- **SPEC section:** `plans/SPEC.md` §8.3 storage + prune (lines 413–420), §6.2 prune dialog (line 264), §10.2 `pruneOldestPulls(50)` (lines 462–465), §12 threshold (line 518).
- **Files involved:**
  - `util/StorageMonitor.kt` — `isNearCapacity()` via `StatFs(filesDir.path)`: `total = blockCountLong*blockSizeLong`, `used = total-free`, `used/total > 0.80`; false if `total<=0`; return 0 / never throw on error
  - `viewmodel/HistoryViewModel.kt` — `checkStorageAndPruneIfNeeded()`, `pruneOldestPulls(50)` (`oldest(50)` → `deleteByIds`); `showsPruningAlert`
  - `ui/history/HistoryScreen.kt` — prune dialog
  - boundary tests + VM tests
- **Prior decisions:** silent-zero behavior matches the original; prune deletes oldest 50 on confirm only.
- **State of the world:** history load + detail exist (ISSUE_02).

## Output Format

A single PR containing:

- [ ] Full `StorageMonitor` with `StatFs` math + silent-zero error handling
- [ ] Prune dialog + `checkStorageAndPruneIfNeeded` + `pruneOldestPulls(50)`
- [ ] Boundary tests (0 / 79% / 80% / 81% / total=0) + VM prune test
- [ ] No multi-select/clear-all (ISSUE_04)

## Examples

**Boundary test that should pass:**
```kotlin
@Test fun threshold_boundaries() {
    assertFalse(monitor(used = 79, total = 100).isNearCapacity())
    assertTrue(monitor(used = 80, total = 100).isNearCapacity())   // > 0.80? 80/100=0.80 → match original's exact comparison
    assertFalse(monitor(used = 0, total = 0).isNearCapacity())     // total<=0 → false, never throws
}
```
> Port the exact comparison (`> 0.80` vs `>= 0.80`) from the original; the original wins.

## Constraints

**Scope fence:** No multi-select edit mode or clear-all (ISSUE_04). Do not change
the draw-screen storage warning (Epic 3 ISSUE_05) beyond pointing it at this
canonical `StorageMonitor`.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> empty/`runCatching {}` catches that hide real errors (silent-zero is a
> *deliberate, documented* return value, not a swallowed exception — implement it
> explicitly), no `@Ignore`d tests without an issue reference, no lowering
> thresholds. Fix the root cause. The only exception is the documented 4-line
> escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf /
> generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** History self-prunes under storage pressure without
breaking normal loads.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] `StorageMonitor` 95–100%, VM 95–100% (§5); all boundaries tested.
- [ ] KDoc on `StorageMonitor` + prune methods.
- [ ] PR includes `Refs #4` and `Closes #26`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `history`
