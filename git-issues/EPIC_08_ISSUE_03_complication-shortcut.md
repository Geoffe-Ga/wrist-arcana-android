## Role

You are a Wear OS engineer adding an optional quick-launch surface (complication
or app shortcut).

## Goal

Add an **optional** complication / app shortcut that launches straight into a
draw, reusing the shared `DrawUseCase` and the existing deep-link.

## Context

- **Parent epic:** #8
- **Predecessor issue(s):** #38 (Tile draw + deep-link). This closes Epic 8.
- **SPEC section:** `plans/SPEC.md` §10.5 "Optional: a complication / app shortcut" (lines 484–486).
- **Files involved:**
  - a complication data-source service and/or an app shortcut definition
  - `AndroidManifest.xml` — register the surface
  - tests for the launch path
- **Prior decisions:** explicitly **optional** in the SPEC. If on-watch testing shows a complication adds little over the Tile, it's acceptable to ship an app shortcut only — record the decision in the PR.
- **State of the world:** Tile draws + deep-links (ISSUE_02).

## Output Format

A single PR containing:

- [ ] A complication and/or app shortcut launching straight into a draw via the shared use-case + deep-link
- [ ] Manifest registration
- [ ] Tests for the launch path
- [ ] A PR note recording which surface(s) shipped and why

## Examples

**Done looks like:** from the watch face, a complication tap (or long-press app
shortcut) opens the app directly into a fresh draw — no duplicated draw logic.

## Constraints

**Scope fence:** Do not change the Tile (ISSUE_02) or in-app flow beyond reusing
the shared use-case/deep-link. Keep it genuinely optional — if dropped, say so in
the PR and close the issue with rationale rather than shipping a low-value surface.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** The new surface reuses existing logic and disturbs
nothing already shipped.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Launch-path test passes; coverage meets §5.
- [ ] KDoc on the new surface.
- [ ] PR includes `Refs #8` and `Closes #39`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `polish`, `tile`
