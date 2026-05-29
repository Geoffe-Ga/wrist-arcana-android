## Role

You are a build/release engineer wiring Kotlin static analysis and coverage into
a Gradle project so local and CI checks are identical.

## Goal

Replace the no-op guards in `scripts/*.sh` with real Gradle-backed ktlint,
detekt, Android Lint, and Kover so `./scripts/check-all.sh` runs the genuine
gates and exits 0 on the current (clean) code.

## Context

- **Parent epic:** #1
- **Predecessor issue(s):** #10 (module exists). Can land in parallel with ISSUE_02 but after ISSUE_01.
- **SPEC section:** `plans/SPEC.md` §14 (lines 555–573), §5 coverage targets (lines 199–209), §13 coverage gate (lines 548–551).
- **Files involved:**
  - `app/build.gradle.kts` / root — apply ktlint, detekt, Kover, Android Lint plugins; config files (`detekt.yml`, `.editorconfig` for ktlint)
  - `scripts/format.sh`, `scripts/lint.sh`, `scripts/test.sh`, `scripts/typecheck.sh`, `scripts/check-all.sh`, `scripts/fix-all.sh` — drop the "not yet scaffolded" no-op and call real tasks
- **Prior decisions:** scripts are the single source of truth (CLAUDE.md §2); CI calls these same scripts. Kover for coverage. Overall coverage floor **≥50%** (target 60%+) with per-layer targets in §5.
- **State of the world:** scripts currently no-op with a clear message and exit 0 (pre-Epic-1 guard).

## Output Format

A single PR containing:

- [ ] ktlint + detekt + Kover + Android Lint configured in Gradle with committed config files
- [ ] `format.sh`→`ktlintFormat`; `lint.sh`→`ktlintCheck`+`detekt`+`lintDebug`; `test.sh`→unit tests + Kover; `typecheck.sh`→compile; `check-all.sh`→all + coverage; `fix-all.sh`→`ktlintFormat`
- [ ] Kover verification rule enforcing the ≥50% overall floor
- [ ] No production code changes beyond what's needed to pass the new gates

## Examples

**Done looks like:**
```
./scripts/check-all.sh
# runs ktlintCheck, detekt, lintDebug, test (JUnit5), koverVerify
# → all green, exits 0
```

## Constraints

**Scope fence:** Do not add the CI workflow changes (ISSUE_04 owns `ci.yml`). Do
not lower any threshold to make things pass — set the ≥50% floor per SPEC §5 and
meet it. No new features.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)` to silence detekt/lint, no `// ktlint-disable`, no `!!`, no
> `@Suppress("UNCHECKED_CAST")`, no empty/`runCatching {}` catches that swallow
> errors, no `@Ignore`d tests without an issue reference, **no lowering
> coverage/quality thresholds**. Fix the root cause. The only exception is the
> documented 4-line escape hatch (third-party-SDK bug / OS-version compat /
> benchmarked-perf / generated code) with reason, reference URL, alternative
> considered, and review date.

**Tracer-code invariant:** Scripts must keep exiting 0 on clean code; never leave
the gate red.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` runs the real tasks and exits 0.
- [ ] `pre-commit run --all-files` is clean (shellcheck on scripts passes).
- [ ] Kover ≥50% floor is enforced and met.
- [ ] PR includes `Refs #1` and `Closes #12`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `build`
