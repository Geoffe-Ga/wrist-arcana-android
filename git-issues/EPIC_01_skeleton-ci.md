## Epic Summary

Stand up the Gradle Wear OS module, manifest, and an empty 3-page pager that
**builds and launches** on a Wear OS 4+ emulator, with **real** quality scripts
and **green CI**. This is the tracer-code skeleton for the whole app: every later
epic replaces a placeholder page or stub with real logic. Covers SPEC §4 (project
structure), §14 (build/CI/quality), and §16.1.

> **Bootstrap note (SPEC §16.1 / CLAUDE.md §6):** like the original's manual
> Xcode skeleton, this epic is **landed by hand once** and merged before the
> Ralph loop starts. Ralph picks up from Epic 2. The child issues below exist for
> traceability; build them in as few hand-made PRs as is practical.

## Scope

**In scope:**
- Single `:app` Gradle module (Kotlin DSL) + `gradle/libs.versions.toml` version catalog.
- `AndroidManifest.xml`: `<uses-feature android.hardware.type.watch>`, `standalone=true`, `VIBRATE` permission.
- `MainActivity` (`ComponentActivity` + `setContent { WristArcanaRoot() }`).
- `WristArcanaRoot` 3-page `HorizontalPager` (Reference / **Draw default idx 1** / History) with placeholder content.
- Real quality scripts (`format/lint/test/typecheck/check-all.sh`) running Gradle-backed ktlint/detekt/Android Lint/Kover.
- `ci.yml` (job name **"CI"**) runs the real scripts + assembles a debug APK + coverage gate.

**Out of scope:**
- Any real data, draw logic, history, notes, reference content (later epics).
- Theming polish beyond a minimal `Theme.kt` stub (Epic 7 owns the full palette).

## Success Criteria

The epic is done when:

- [ ] `./gradlew assembleDebug` produces an installable APK that launches on a Wear OS 4 emulator.
- [ ] The 3-page pager swipes Reference ↔ Draw (default) ↔ History with placeholder content.
- [ ] `./scripts/check-all.sh` runs the **real** Gradle tasks (no more no-op guard) and exits 0.
- [ ] CI (`ci.yml`, job name "CI") is green: ktlint + detekt + Android Lint + unit tests + Kover + assembleDebug.
- [ ] All child issues are closed.

## Child Issues

- [ ] #10 — Wire Gradle Wear module, manifest, and MainActivity skeleton
- [ ] #11 — Add 3-page HorizontalPager (Reference/Draw/History) with placeholders
- [ ] #12 — Wire real ktlint/detekt/Android Lint/Kover quality scripts
- [ ] #13 — Run real quality tasks + assembleDebug + coverage gate in CI

## Sequencing Notes

- **Blocks:** every other epic — nothing compiles until the module exists.
- **Hand-built bootstrap:** merge this before starting `/loop /ralph-tick`.
- Decide the nav primitive here (HorizontalPager vs SwipeDismissableNavHost+pager — Appendix B); default HorizontalPager.

## SPEC Reference

[`plans/SPEC.md`](../plans/SPEC.md) §4 (lines 111–179), §14 (lines 555–573), §16.1 (lines 603–607), §15 Wear concerns (lines 577–594).

## Labels

`epic`, `spec-decomposition`, `skeleton`
