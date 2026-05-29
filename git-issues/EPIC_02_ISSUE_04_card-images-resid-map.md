## Role

You are an Android asset-pipeline engineer importing image assets and generating
a reliable name→resource-id lookup, with a CI gate proving completeness.

## Goal

Import all 78 card images into `res/drawable-*`, provide a name→drawable-resId map
(no runtime reflection), and add an asset-integrity test proving every `imageName`
in the JSON resolves to a real drawable.

## Context

- **Parent epic:** #2
- **Predecessor issue(s):** #15 (JSON provides the `imageName` list to validate against).
- **SPEC section:** `plans/SPEC.md` §7.3 image pipeline (lines 326–343), §7.5 resId map (lines 385–387), §15 memory (lines 581–584), Appendix B density buckets (lines 680–682).
- **Files involved:**
  - `app/src/main/res/drawable-*/<imageName>.png` (78 cards) — names lowercase, **exactly** matching JSON `imageName` (`major_00`, `swords_king`, `cups_01`, …)
  - a generated or hand-kept `CardImageMap.kt` (name→`@DrawableRes` id)
  - asset-integrity test iterating the JSON's `imageName`s
- **Prior decisions:** source art from the original's asset catalog / `scripts/RWS_Cards_Processed/`. Map Apple scales → density buckets (`@1x→mdpi`, `@2x→xhdpi`, `@3x→xxxhdpi`); **single `drawable-nodpi` bucket is acceptable** if on-watch memory testing is fine — decide and record the choice here. Prefer the name→resId map over `resources.getIdentifier` reflection.
- **State of the world:** models + repos + JSON exist; no images yet.

## Output Format

A single PR containing:

- [ ] 78 drawables placed in the chosen density bucket(s) with exact `imageName` names
- [ ] `CardImageMap` resolving every `imageName` to a `@DrawableRes` id without reflection
- [ ] Asset-integrity test: every JSON `imageName` resolves to a real drawable (the "78 present" gate)
- [ ] A short note in the PR recording the density-bucket decision (per-density vs `nodpi`) and the memory rationale

## Examples

**The gate test:**
```kotlin
@Test fun every_card_image_resolves() {
    val names = deckRepository.loadDecks().flatMap { it.cards }.map { it.imageName }
    assertEquals(78, names.size)
    names.forEach { assertNotEquals(0, CardImageMap.resId(it)) { "missing drawable: $it" } }
}
```

## Constraints

**Scope fence:** No `CardImage` composable rendering/placeholder (Epic 3/7) — only
the resId map + integrity test here. Do not rename images away from the JSON
`imageName`. Room is ISSUE_05.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)`/`// ktlint-disable`/`!!`/`@Suppress("UNCHECKED_CAST")`, no
> error-swallowing catches, no `@Ignore`d tests without an issue reference, no
> lowering thresholds. Fix the root cause. The only exception is the documented
> 4-line escape hatch (third-party-SDK bug / OS-version compat / benchmarked-perf
> / generated code) with reason, reference URL, alternative considered, and review
> date.

**Tracer-code invariant:** Art now resolves by name; UI epics can render real cards.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0.
- [ ] `pre-commit run --all-files` is clean (large-files hook satisfied for PNGs, or LFS/justification noted).
- [ ] Asset-integrity test passes (all 78 resolve).
- [ ] PR includes `Refs #2` and `Closes #17`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `core`, `data`, `assets`
