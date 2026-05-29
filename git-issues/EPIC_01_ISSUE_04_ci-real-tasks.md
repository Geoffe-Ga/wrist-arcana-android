## Role

You are a CI engineer configuring GitHub Actions for an Android/Wear OS Gradle
project, mindful that downstream automation keys off the workflow name.

## Goal

Make `ci.yml` (job name **"CI"**) run the real quality scripts + assemble a debug
APK + enforce the Kover coverage gate, so every PR gets a genuine green/red
signal.

## Context

- **Parent epic:** #1
- **Predecessor issue(s):** #12 (real scripts must exist first).
- **SPEC section:** `plans/SPEC.md` §14 CI (lines 564–573), §13 coverage (lines 548–551). CLAUDE.md §6 (CI name must stay "CI" for `iteration-trigger.yml`).
- **Files involved:**
  - `.github/workflows/ci.yml` — JDK 17 + Gradle cache; run `./scripts/lint.sh`, `./scripts/test.sh`, `./gradlew assembleDebug`; Kover
  - optionally a pre-commit job (generic hooks + ktlint + detect-secrets + shellcheck)
- **Prior decisions:** CI invokes the **same scripts** as local (CLAUDE.md §2). Job name **must stay "CI"** — `iteration-trigger.yml`'s `workflow_run` filter matches on it; renaming breaks the Ralph inner loop.
- **State of the world:** `ci.yml` exists but is guarded to no-op until the Gradle skeleton lands.

## Output Format

A single PR containing:

- [ ] `ci.yml` running JDK 17 + Gradle cache → `./scripts/lint.sh` + `./scripts/test.sh` (Kover) + `./gradlew assembleDebug`
- [ ] Coverage gate wired (Kover ≥50% floor fails the build below threshold)
- [ ] Workflow name preserved as **"CI"**
- [ ] (Optional) Wear emulator matrix for instrumented tests — may be deferred; if so, note it in the PR

## Examples

**Done looks like:**
```
# On a PR: CI job "CI" runs and goes green:
#   ✓ lint (ktlint + detekt + Android Lint)
#   ✓ test + Kover (≥50%)
#   ✓ assembleDebug
```

## Constraints

**Scope fence:** Do not change the script internals (ISSUE_03 owns them) beyond
calling them from CI. Do not rename `ci.yml`'s workflow/job from "CI". No app
feature code.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, **no
> lowering coverage/quality thresholds** to make CI pass. Fix the root cause. The
> only exception is the documented 4-line escape hatch (third-party-SDK bug /
> OS-version compat / benchmarked-perf / generated code) with reason, reference
> URL, alternative considered, and review date.

**Tracer-code invariant:** CI must be green on `main` after merge; never leave the
default branch red.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0 locally.
- [ ] `pre-commit run --all-files` is clean.
- [ ] CI job "CI" is green on the PR (lint + test/Kover + assembleDebug).
- [ ] PR includes `Refs #1` and `Closes #13`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `ci`
