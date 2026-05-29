## Role

You are a Wear OS Tile engineer implementing a tappable draw action with a
deep-link into the app.

## Goal

Make the Tile draw + save a `CardPull` via the shared `DrawUseCase`, render the
result inline, and deep-link into `CardDisplayScreen`.

## Context

- **Parent epic:** #8
- **Predecessor issue(s):** #37 (shared use-case + Tile shell).
- **SPEC section:** `plans/SPEC.md` §10.5 (lines 477–489), §7.4 DB singleton (lines 362–367).
- **Files involved:**
  - `tile/DrawCardTileService.kt` — tap → `DrawUseCase.drawAndSave()` → render card inline → deep-link `CardDisplayScreen`
  - `MainActivity.kt` — handle the deep-link intent → open `CardDisplayScreen` for the drawn pull
  - tests for the Tile draw path + deep-link intent
- **Prior decisions:** Tile satisfies the original's "draw without opening" intent (no Siri analogue); shared use-case + app-scoped DB singleton prevent lock contention.
- **State of the world:** shared use-case + inert Tile shell exist (ISSUE_01).

## Output Format

A single PR containing:

- [ ] Tile tap performs draw+save via `DrawUseCase`, renders the result, deep-links to `CardDisplayScreen`
- [ ] Deep-link handling in `MainActivity`
- [ ] Tests: Tile action saves exactly one pull; deep-link opens the right card; no DB contention with the Activity
- [ ] No complication (ISSUE_03)

## Examples

**Done looks like:** tapping the Tile's DRAW draws a fair card, persists it to the
same history the app shows, renders it on the Tile, and tapping through opens
`CardDisplayScreen` for that exact pull.

## Constraints

**Scope fence:** No complication/app-shortcut (ISSUE_03). Reuse the shared
use-case — do not duplicate draw/save logic in the Tile.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** The Tile draws + deep-links without disturbing the
in-app flow or history.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean.
- [ ] Coverage meets §5 for the draw path; Tile + deep-link tested.
- [ ] KDoc on the Tile service + deep-link contract.
- [ ] PR includes `Refs #8` and `Closes #38`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `tile`
