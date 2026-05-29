## Role

You are a senior Android/Wear OS engineer bootstrapping a brand-new Gradle
(Kotlin DSL) project for a Wear OS 4+ watch app. You know Compose for Wear OS,
version catalogs, and standalone watch manifests.

## Goal

Create the single `:app` Gradle Wear module so that `./gradlew assembleDebug`
produces an installable APK that launches a blank `MainActivity` on a Wear OS 4
emulator.

## Context

- **Parent epic:** #1
- **Predecessor issue(s):** none — this is the skeleton issue for Epic 1 and the whole app.
- **SPEC section:** `plans/SPEC.md` §4 (lines 111–179), §3 tech mapping (lines 75–107), §15 Wear concerns (lines 577–594).
- **Files involved:**
  - `settings.gradle.kts`, root `build.gradle.kts`, `gradle/libs.versions.toml` — module + version catalog
  - `app/build.gradle.kts` — `com.android.application` + Wear Compose deps, `minSdk 30`, target latest
  - `app/src/main/AndroidManifest.xml` — `<uses-feature android.hardware.type.watch>`, `standalone=true`, `VIBRATE`
  - `app/src/main/kotlin/com/wristarcana/MainActivity.kt` — `ComponentActivity` + `setContent {}`
  - `app/src/main/kotlin/com/wristarcana/config/Theme.kt` — minimal Wear `MaterialTheme` stub (full palette is Epic 7)
- **Prior decisions:** Kotlin DSL, single `:app` module, manual DI, kotlinx.serialization (added when first used in Epic 2). Default nav primitive `HorizontalPager` (wired in ISSUE_02).
- **State of the world:** repo has scaffolding (scripts, CLAUDE.md, CI guarded to no-op) but **no Gradle module and no `./gradlew`** yet.

## Output Format

A single PR containing:

- [ ] `settings.gradle.kts` + root `build.gradle.kts` + `gradle/libs.versions.toml` + `app/build.gradle.kts`
- [ ] Gradle wrapper (`gradlew`, `gradlew.bat`, `gradle/wrapper/*`) pinned to a current stable Gradle
- [ ] `AndroidManifest.xml` (standalone watch), `MainActivity.kt`, minimal `Theme.kt`
- [ ] A smoke unit test (e.g. JUnit5 sanity test) proving the module compiles and the test task runs
- [ ] No business logic, no extra screens — blank activity only

## Examples

**Manifest essentials that must be present:**
```xml
<uses-feature android:name="android.hardware.type.watch" />
<uses-permission android:name="android.permission.VIBRATE" />
<application ...>
  <meta-data android:name="com.google.android.wearable.standalone" android:value="true" />
  <activity android:name=".MainActivity" android:exported="true"> ... </activity>
</application>
```

**Done looks like:**
```
./gradlew assembleDebug   # BUILD SUCCESSFUL, app-debug.apk produced
# installs + launches a blank screen on a Wear OS 4 emulator
```

## Constraints

**Scope fence:** Do not add the pager, any data/models, or real theming — those
are ISSUE_02 and later epics. Do not wire the real quality scripts/CI yet
(ISSUE_03/04). If you touch files outside the list above, stop and check.

**Anti-bypass (non-negotiable, per CLAUDE.md §2 / `max-quality-no-shortcuts`):**

> No `@Suppress(...)` to silence detekt/lint, no `// ktlint-disable`, no `!!` to
> dodge null-safety, no `@Suppress("UNCHECKED_CAST")`, no empty/`runCatching {}`
> catches that swallow errors, no `@Ignore`d tests without an issue reference, no
> lowering coverage/quality thresholds. Fix the root cause. The only exception is
> the documented 4-line escape hatch (third-party-SDK bug / OS-version compat /
> benchmarked-perf / generated code) — and it must include the reason, a
> reference URL, an alternative considered, and a review date.

**Tracer-code invariant:** After this PR the app must build, launch, and stay
green. Subsequent issues replace the blank activity's content; nothing here may
block them.

## Definition of Done (stay-green)

- [ ] `./scripts/check-all.sh` exits 0 (now backed by real Gradle tasks for this module).
- [ ] `pre-commit run --all-files` is clean — no skipped or bypassed hooks.
- [ ] `./gradlew assembleDebug` produces an APK that launches on a Wear OS 4 emulator.
- [ ] KDoc on any public entry points (`MainActivity`).
- [ ] PR uses the git-workflow template and includes `Refs #1` and `Closes #10`.
- [ ] Latest Claude reviewer `Verdict:` on HEAD is `LGTM`.

## Labels

`spec-decomposition`, `skeleton`, `build`
