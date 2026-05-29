## Role

You are a Wear OS Compose design-systems engineer applying a cohesive theme
across an existing app.

## Goal

Implement the full `Theme.kt` (purple→blue gradient, black card background,
serif typography scale, 8/16/24dp spacing) via Wear `MaterialTheme` and apply it
across all screens.

## Context

- **Parent epic:** #7
- **Predecessor issue(s):** none for this epic, but the feature screens it themes must exist (Epics 3–6 merged). This is the lead issue of the polish epic.
- **SPEC section:** `plans/SPEC.md` §11 theme (lines 495–498), §3 Theme row, Appendix A `Theme.swift` (line 670). Original: `Configuration/Theme.swift`.
- **Files involved:**
  - `config/Theme.kt` — color set (primary gradient purple→blue TL→BR, black card bg), typography (title ~32sp bold serif, card name ~20sp semibold serif, body ~14sp), spacing 8/16/24
  - touch points across `ui/**` to consume the theme (no behavior change)
  - screenshot/UI tests where practical
- **Prior decisions:** match the original palette; minimal `Theme.kt` stub from Epic 1 gets replaced here.
- **State of the world:** all feature screens exist with minimal styling.

## Output Format

A single PR containing:

- [ ] Full `Theme.kt` + `MaterialTheme` wrapper applied at the root
- [ ] Screens consume theme colors/typography/spacing (no logic changes)
- [ ] Tests/snapshots validating key tokens where practical
- [ ] No new features

## Examples

**Done looks like:** every screen renders with the purple→blue primary, black card
backgrounds, serif titles ~32sp / card names ~20sp / body ~14sp, on an 8/16/24dp
spacing rhythm — visually matching the original.

## Constraints

**Scope fence:** No responsive sizing (ISSUE_02) or a11y semantics (ISSUE_03) —
palette + typography only. No behavior changes.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Pure visual polish — every screen still works exactly
as before.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] No coverage regression; existing UI tests still pass.
- [ ] KDoc on `Theme.kt` public tokens.
- [ ] PR includes `Refs #7` and `Closes #34`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `theming`
