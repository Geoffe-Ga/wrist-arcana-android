## Role

You are a Wear OS Compose + MVVM engineer wiring a list to real persistence and
building its detail screen.

## Goal

Implement `loadHistory()` (recent 100, date desc, from the DAO), the full
`HistoryRow` (thumbnail + name + date + truncated note + note indicator), and
`HistoryDetailScreen` (image, name, date drawn, meaning).

## Context

- **Parent epic:** #4
- **Predecessor issue(s):** #24 (VM + screen skeleton).
- **SPEC section:** `plans/SPEC.md` §6.2 list/detail (lines 255–270), §7.4 `recent(100)` + `truncatedNote`/`hasNote` (lines 354–360), §10.2 `loadHistory` (lines 461–465).
- **Files involved:**
  - `viewmodel/HistoryViewModel.kt` — `loadHistory()` → `dao.recent(100)` (or `Flow`), date desc
  - `ui/components/HistoryRow.kt` — thumbnail (via resId map) + name + formatted date + truncated note + indicator
  - `ui/history/HistoryDetailScreen.kt` — image, name, date drawn, upright meaning (note management is Epic 5)
  - `util/DateFormatting.kt` — `java.time` localized medium/short (if not already present)
  - VM + Compose UI tests
- **Prior decisions:** date desc, cap 100; `DateFormatting` via `java.time`. Detail's note section is a placeholder until Epic 5.
- **State of the world:** VM/screen skeleton + empty state exist (ISSUE_01).

## Output Format

A single PR containing:

- [ ] Real `loadHistory()` (recent 100, date desc); reactive `Flow` where it simplifies the VM
- [ ] Full `HistoryRow` + `HistoryDetailScreen`
- [ ] `DateFormatting` util + tests
- [ ] VM tests (cap at 100, ordering) + UI tests (row renders, tap → detail)

## Examples

**VM test that should pass:**
```kotlin
@Test fun load_caps_at_100_newest_first() = runTest {
    fakeDao.seed(120)
    vm.loadHistory()
    val pulls = vm.uiState.value.pulls
    assertEquals(100, pulls.size)
    assertTrue(pulls.zipWithNext().all { (a, b) -> a.date >= b.date })
}
```

## Constraints

**Scope fence:** No storage/prune (ISSUE_03), no multi-select/clear-all
(ISSUE_04), no note add/edit/delete (Epic 5).

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** History now shows real saved readings and opens a real
detail view.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM 95–100%, `DateFormatting` 95–100%, components ≥60% (§5).
- [ ] KDoc on `loadHistory` + `DateFormatting`.
- [ ] PR includes `Refs #4` and `Closes #25`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `history`
