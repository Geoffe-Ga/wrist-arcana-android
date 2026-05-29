## Role

You are a Kotlin/coroutines engineer implementing a cancellable suspense delay,
haptic feedback, and history persistence inside a `ViewModel`.

## Goal

Complete `drawCard()`: a cancellable ~500ms suspense delay, then select → save a
`CardPull` → fire a haptic on success, with clean cancellation if the user
navigates away mid-draw.

## Context

- **Parent epic:** #3
- **Predecessor issue(s):** #20 (real selection).
- **SPEC section:** `plans/SPEC.md` §8.4 suspense (lines 422–426), §8.2 save (lines 409–411), §6.1 draw steps (lines 228–240), §3 haptics row (line 94), §12 `MIN_DRAW_DURATION_MS` (line 519).
- **Files involved:**
  - `viewmodel/CardDrawViewModel.kt` — `drawCard()` does delay → cancellation check → select → `dao.insert(CardPull{…})` → haptic → clear loading; `errorMessage` on failure
  - `config/AppConstants.kt` — `MIN_DRAW_DURATION_MS = 500` (+ others per §12 if not present)
  - a haptic seam (e.g. `HapticFeedbackProtocol` wrapping `Vibrator`/`VibrationEffect`) so it's testable
  - VM tests with `runTest` + fake clock + fake DAO/haptic
- **Prior decisions:** `delay(500)` inside `viewModelScope`, cancellable; persist `CardPull{ id=UUID, date=now, cardName, deckName, cardImageName=card.imageName, cardDescription=card.upright, note=null }`.
- **State of the world:** selection works (ISSUE_02); no delay/save/haptic yet.

## Output Format

A single PR containing:

- [ ] Cancellable suspense delay + select + save + haptic in `drawCard()`
- [ ] `HapticFeedbackProtocol` + real impl + fake
- [ ] `AppConstants` populated per §12
- [ ] VM tests: a successful draw inserts exactly one pull with the right fields; cancellation mid-delay inserts nothing; haptic fires once on success; `errorMessage` set on save failure
- [ ] No preview/display screens (ISSUE_04), no storage dialog (ISSUE_05)

## Examples

**Test that should pass:**
```kotlin
@Test fun successful_draw_saves_one_pull() = runTest {
    vm.drawCard(); advanceTimeBy(500); runCurrent()
    assertEquals(1, fakeDao.inserted.size)
    assertEquals(vm.uiState.value.currentCard!!.imageName, fakeDao.inserted.first().cardImageName)
    assertEquals(1, fakeHaptic.clicks)
}
```

## Constraints

**Scope fence:** No preview/detail UI (ISSUE_04). The storage-warning dialog is
ISSUE_05 (compute-and-flag may be stubbed here, dialog wiring lands there).

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> empty/`runCatching {}` catches that swallow errors (a save failure must set
> `errorMessage`, not vanish), no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** A draw now persists to history and buzzes — the app is
meaningfully demoable.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM coverage 95–100% (§5); success, cancellation, and failure paths tested.
- [ ] KDoc on `drawCard` + haptic seam.
- [ ] PR includes `Refs #3` and `Closes #21`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `draw`
