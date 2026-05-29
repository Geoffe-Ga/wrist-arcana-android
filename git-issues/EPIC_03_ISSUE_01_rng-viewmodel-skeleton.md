## Role

You are a Kotlin/Compose engineer setting up an MVVM draw screen with a
testable RNG seam and a `StateFlow`-driven `ViewModel`.

## Goal

Create `RandomGeneratorProtocol` + a `SecureRandom` implementation, the
`CardDrawViewModel` with its full UI-state shape, and a `DrawCardScreen` +
`DrawButton` wired to a **stubbed** `drawCard()` (no real selection yet).

## Context

- **Parent epic:** #3
- **Predecessor issue(s):** none — skeleton issue for Epic 3. (Epic 2 must be merged: models, repos, DAO.)
- **SPEC section:** `plans/SPEC.md` §10.1 `CardDrawViewModel` (lines 449–456), §6.1 DrawCardScreen (lines 223–240), §3 CSPRNG row (line 93).
- **Files involved:**
  - `util/RandomGenerator.kt` — `RandomGeneratorProtocol` + `SecureRandom`-backed impl (`nextInt(bound)`)
  - `viewmodel/CardDrawViewModel.kt` — state data class (`currentCard`, `currentCardPull`, `isDrawing`, `showsStorageWarning`, `errorMessage`) as `StateFlow`; `drawCard()` stub that toggles `isDrawing`; `dismissCard()`, `acknowledgeStorageWarning()`; holds `drawnThisSession` set
  - `ui/draw/DrawCardScreen.kt` + `ui/components/DrawButton.kt` — DRAW button wired to `drawCard()`, spinner while `isDrawing`
  - VM unit test (Turbine) + a Compose smoke test
- **Prior decisions:** RNG behind an interface so VMs are testable with a fake. StateFlow for VM state. Constructor-injected repos/DAO/RNG via a factory.
- **State of the world:** data layer exists (Epic 2); the pager's Draw page is still a placeholder (Epic 1 ISSUE_02).

## Output Format

A single PR containing:

- [ ] `RandomGenerator` interface + `SecureRandom` impl + a `FakeRandomGenerator` test double
- [ ] `CardDrawViewModel` with the full state shape and stubbed `drawCard()`
- [ ] `DrawCardScreen` + `DrawButton`, replacing the Draw placeholder page
- [ ] Turbine VM test (state toggles) + Compose smoke test (button visible, spinner on tap)
- [ ] No real selection/suspense/save (ISSUE_02–05)

## Examples

**VM smoke test:**
```kotlin
@Test fun drawCard_toggles_isDrawing() = runTest {
    vm.uiState.test {
        assertFalse(awaitItem().isDrawing)
        vm.drawCard()
        assertTrue(awaitItem().isDrawing)   // stub flips loading
    }
}
```

## Constraints

**Scope fence:** No no-repeat algorithm (ISSUE_02), no suspense/haptic/save
(ISSUE_03), no preview/display screens (ISSUE_04), no storage dialog (ISSUE_05).

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** The Draw page renders a real button backed by a real
VM; later issues fill in behavior without reshaping the screen.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] VM coverage 95–100% for the state logic present (§5).
- [ ] KDoc on `RandomGeneratorProtocol` + `CardDrawViewModel`.
- [ ] PR includes `Refs #3` and `Closes #19`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `skeleton`, `draw`
