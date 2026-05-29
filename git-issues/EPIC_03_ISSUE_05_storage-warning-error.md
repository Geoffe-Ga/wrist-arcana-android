## Role

You are a Kotlin/Compose engineer adding post-action edge-case handling: a
storage-capacity warning and user-visible error reporting.

## Goal

After a draw, if storage is ≥80% used, raise an informational storage-warning
dialog; on any draw failure, surface `errorMessage` in the UI.

## Context

- **Parent epic:** #3
- **Predecessor issue(s):** #22 (draw→preview→detail flow). Uses `StorageMonitorProtocol` (the full `StatFs` impl is Epic 4 ISSUE_03; here, depend on the **interface** — provide a minimal impl or fake if Epic 4 hasn't landed, and note the dependency).
- **SPEC section:** `plans/SPEC.md` §8.3 storage (lines 413–420), §6.1 step 5 (lines 234–235), §10.1 `showsStorageWarning`/`errorMessage` (lines 450–455), §12 `STORAGE_WARNING_THRESHOLD` (line 518).
- **Files involved:**
  - `util/StorageMonitor.kt` — `StorageMonitorProtocol.isNearCapacity()` (interface; minimal impl acceptable here, full StatFs math owned by Epic 4)
  - `viewmodel/CardDrawViewModel.kt` — set `showsStorageWarning` after save when near capacity; `acknowledgeStorageWarning()`
  - `ui/draw/DrawCardScreen.kt` / preview — render the warning dialog + error message
  - VM + UI tests
- **Prior decisions:** warning is informational (OK button); never throws (silent-zero on error). Threshold 0.80.
- **State of the world:** draw flow + result screens exist; no storage/error surfacing yet.

## Output Format

A single PR containing:

- [ ] `showsStorageWarning` set post-save when `isNearCapacity()`; `acknowledgeStorageWarning()` clears it
- [ ] An informational dialog + an error surface in the draw UI
- [ ] VM tests: warning toggles at the threshold (fake monitor at 79/80/81%); `errorMessage` set on save failure and cleared on dismiss
- [ ] If Epic 4 hasn't landed the full `StorageMonitor`, a minimal interface-satisfying impl + a note in the PR

## Examples

**Test that should pass:**
```kotlin
@Test fun storage_warning_at_threshold() = runTest {
    fakeMonitor.nearCapacity = true
    vm.drawCard(); advanceTimeBy(500); runCurrent()
    assertTrue(vm.uiState.value.showsStorageWarning)
    vm.acknowledgeStorageWarning()
    assertFalse(vm.uiState.value.showsStorageWarning)
}
```

## Constraints

**Scope fence:** Do not build the full `StatFs` math or the History prune flow —
those are Epic 4 ISSUE_03. Stay within the draw screen's edge handling.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** The draw loop now handles its edge cases without
breaking the happy path.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM coverage 95–100% (§5); threshold + error paths tested.
- [ ] KDoc on the storage seam.
- [ ] PR includes `Refs #3` and `Closes #23`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `edges`, `draw`
