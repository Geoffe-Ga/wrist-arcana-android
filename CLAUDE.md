# CLAUDE.md — wrist-arcana-android

Guidance for Claude Code (and the Ralph loop) when working in this repository.

## 1. Project overview

**Wrist Arcana for Wear OS** is a native **Android / Wear OS** port of the
watchOS tarot-reading app *Wrist Arcana*. It recreates the original app
**exactly** — cryptographically fair card draws, persistent reading history with
notes, storage-aware pruning, and a full offline reference browser for all 78
Rider–Waite cards — on Samsung Galaxy Watch, Pixel Watch, and other Wear OS 4+
devices.

**The authoritative plan is [`plans/SPEC.md`](plans/SPEC.md).** Read it before
doing any implementation work. When the SPEC and the original watchOS app
disagree, the original wins (its source lives at
`/Users/geoffgallinger/Projects/wrist-arcana`) — file a SPEC-fix issue.

**Tech stack (see SPEC §3 for the full mapping table):**
- **Language:** Kotlin (latest stable)
- **UI:** Jetpack Compose for Wear OS (`androidx.wear.compose`)
- **Persistence:** Room (the SwiftData analogue)
- **Async/state:** Coroutines + `StateFlow`; Android `ViewModel`
- **DI:** interface-based constructor injection (manual `AppContainer`; Hilt only if justified)
- **Serialization:** kotlinx.serialization (bundled `DecksData.json`, reused verbatim)
- **RNG:** `java.security.SecureRandom` behind a `RandomGeneratorProtocol`
- **Build:** Gradle (Kotlin DSL); single watch module
- **Tests:** JUnit5 + MockK + Turbine (unit), Compose UI test (instrumented)
- **Quality:** ktlint + detekt + Android Lint; coverage via Kover

**Product invariants (never violate):** 100% offline (no network, ever); CSPRNG
draws; no-repeat within a session until the deck is exhausted; ~0.5s suspense
delay; storage warning + prune at 80%; multi-deck built but hidden behind
`FeatureFlags.MULTI_DECK_ENABLED = false`. Watch-only — **no phone module**.

## 2. Critical principles (non-negotiable)

1. **Use project scripts, not direct tools.** Run `./scripts/check-all.sh`,
   `./scripts/format.sh`, `./scripts/lint.sh`, `./scripts/test.sh` — never call
   `gradlew`/`ktlint`/`detekt` ad hoc for gate checks. Scripts keep local and CI
   identical.
2. **No shortcuts — fix root causes.** Forbidden: `@Suppress(...)` to silence
   detekt/lint, `// ktlint-disable`, `!!` to dodge null-safety,
   `@Suppress("UNCHECKED_CAST")`, empty/`runCatching {}` catches that swallow
   errors, commented-out or `@Ignore`d tests without an issue reference,
   lowering coverage/quality thresholds. The only exception is the documented
   4-line escape hatch (third-party-SDK bug / OS-version compat /
   benchmarked-perf / generated code) with a review date — see the
   `max-quality-no-shortcuts` skill.
3. **Stay green.** Never open a PR with red CI; never merge without an `LGTM`
   verdict. Follow the 4-gate flow (§5).
4. **Quality first.** Meet coverage and lint thresholds; don't lower them.
5. **Operate from the project root.** Use relative paths; never `cd` into
   subdirectories in committed commands/scripts (CI runs from root).
6. **TDD.** Red → Green → Refactor. Write the failing test first.

## 3. Build, test & quality commands

```bash
./scripts/check-all.sh     # ktlint + detekt + Android Lint + tests + coverage (the gate)
./scripts/format.sh        # ktlintFormat
./scripts/lint.sh          # ktlintCheck + detekt + lintDebug
./scripts/test.sh          # unit tests + Kover coverage
./scripts/typecheck.sh     # Kotlin compile check
./scripts/fix-all.sh       # auto-fix (ktlintFormat)
./scripts/pr-status.sh status <PR#>   # CI + Claude-review verdict for a PR
pre-commit run --all-files # generic hooks + detect-secrets + shellcheck
```

> Until **Epic 1** lands the Gradle Wear module, the Gradle-backed scripts no-op
> with a clear message and exit 0 so pre-commit/CI stay green. Once the
> `./gradlew` wrapper exists, they run the real tasks. Build/launch commands and
> the Wear emulator target are defined by Epic 1 and added here then.

## 4. Architecture (MVVM + interface DI)

Strict layering, ported from the original (SPEC §4–§5):

- **UI (Compose)** — presentation only, no business logic. Reads VM state, emits
  events. Files under `app/src/main/kotlin/com/wristarcana/ui/`.
- **ViewModels** — own all business logic + state (`StateFlow`); depend on
  **interfaces** so they are unit-testable with fakes. `.../viewmodel/`.
- **Data** — `TarotCard`/`TarotDeck` models, `DeckRepository`/`CardRepository`
  (JSON hydrate + validation + fallbacks), Room `CardPull`/DAO/DB. `.../data/`.
- **Utilities** — `RandomGenerator`, `StorageMonitor`, `NoteInputSanitizer`,
  `DateFormatting`. `.../util/`.
- **Config** — `AppConstants`, `FeatureFlags`, `Theme`. `.../config/`.

Coverage targets: Models/ViewModels/Utilities 95–100%; repositories 90–100%;
components 60%+; overall **≥50% gate** (target 60%+) — mirrors the original.

## 5. Stay-Green workflow (4 gates)

1. **Local:** `./scripts/check-all.sh` exits 0.
2. **CI:** all jobs green (`gh pr checks --watch`).
3. **Coverage:** Kover ≥ threshold.
4. **Review:** Claude-review verdict is `LGTM`.

Conventional commits (`feat:`, `fix:`, `test:`, `refactor:`, `docs:`, `chore:`,
`ci:`). One issue → one branch (`issue/<n>-<slug>`) → one PR with `Closes #<n>`.

## 6. The Ralph Loop

This repo is built by a **caffeinated, local-session Ralph Wiggum loop**, ported
from PillBreakfast. The implementation backlog is filed as GitHub issues (via the
`spec-decomposition` / "decompose" skill against `plans/SPEC.md`); each issue
body is a self-contained 6-component prompt. The loop runs in a long-lived
Claude Code session kept awake by `caffeinate`, woken on PR events by an MCP
subscription. The cloud is a participant, not the engine.

### Topology
1. **Local engine:** a `/loop /ralph-tick` session. `/ralph-tick` is
   **re-entrant** — each tick reads `scripts/ralph/state.json` + open-PR state,
   then does one atomic action.
2. **Inner loop in the cloud:** `ci.yml` (name must stay **"CI"**) runs checks;
   `claude-code-review.yml` posts a `Verdict:` comment (LGTM / CHANGES_REQUESTED
   / COMMENTS); `iteration-trigger.yml` watches for CI-complete + verdict, posts
   a nudge comment that wakes the local session, and auto-squash-merges on
   `LGTM` + fully green (using `GEOFFE_GA_PAT`).
3. **Reactions per wake:** PR merged → record completion, pick next; verdict
   CHANGES_REQUESTED/COMMENTS → run `address-feedback`; CI failed → run
   `ci-debugging`; in-flight, no verdict → `await-claude-review`, end turn.
4. **Groom gate:** every `groom_interval` (default 10) merges, the next tick runs
   `/backlog-grooming` before picking.
5. **Termination:** when `scripts/ralph/pick-next.sh` returns nothing and no PR
   is in flight, the tick announces "Backlog drained" and stops `/loop`.

### Start / stop
```bash
caffeinate -d -i claude --add-dir "$(pwd)"
# inside the session:
/loop /ralph-tick
```
Stop with Ctrl-C or `/loop --stop`.

### Controls
| What | How |
| --- | --- |
| Pause new picks | `touch scripts/ralph/.paused` (remove to resume) |
| Pause auto-merge only | repo variable `RALPH_AUTO_MERGE_DISABLED=true` |
| Skip auto-merge for one PR | add label `do-not-auto-merge` |
| Skip an issue | add label `needs-spec` (picker passes it over) |
| Reset/force groom | edit `scripts/ralph/state.json` → `completed_since_groom` |
| Cloud fallback | Actions → "Ralph (next issue) [manual fallback]" → Run workflow (only when local session is offline) |

### Files
- `.claude/commands/ralph-tick.md` — per-tick orchestrator (`/ralph-tick`).
- `scripts/ralph/PROMPT.md` — per-issue worker contract.
- `scripts/ralph/pick-next.sh` — picker (lowest open `spec-decomposition` child;
  skips `epic` / `future-work` / `needs-spec` / in-flight).
- `scripts/ralph/state.json` — counter, last-completed issue, last-groom time.
- `.github/workflows/iteration-trigger.yml` — inner-loop cadence + auto-merge.
- `.github/workflows/ralph-next.yml` — manual cloud fallback (workflow_dispatch).

### Required secrets / variables
- Secret `CLAUDE_CODE_OAUTH_TOKEN` — reviewer + cloud fallback.
- Secret `GEOFFE_GA_PAT` — PAT (repo scope) so iteration-trigger comments/merges
  fire downstream events and wake the local subscription.
- Variable `RALPH_AUTO_MERGE_DISABLED` (optional), `RALPH_PAUSED` (optional).

### Bootstrap
Like the original's manually-built Xcode skeleton, **Epic 1 (the Gradle Wear
module + working CI) is best landed by hand once**, then merged, before starting
the loop. Ralph picks up from Epic 2 onward. Until `./gradlew` exists, CI/scripts
are intentionally guarded to stay green.

## 7. Skills available

Quality skills (from green): `stay-green`, `max-quality-no-shortcuts`,
`tracer-code`, `prompt-engineering`, `git-workflow`, `testing`,
`comprehensive-pr-review`, `address-feedback`, `ci-debugging`,
`backlog-grooming`, `architectural-decisions`, `bug-squashing-methodology`,
`security`, `error-handling`, `documentation`, and more under `.claude/skills/`.

Ported from PillBreakfast: **`spec-decomposition`** (the "decompose" skill —
turns `plans/SPEC.md` into sequenced epics + child issues; invoke as
`/spec-decomposition`) and **`await-claude-review`** (PR-activity subscription
for the Ralph inner loop).

## 8. Common pitfalls

- Don't add a phone module — this is watch-only (SPEC §2).
- Don't make network calls — all 78 images + metadata ship in-app.
- Decode card `id`s as `String` (the JSON uses ids like `rw-major-00`).
- Keep card image resource names identical to the JSON `imageName`
  (`major_00`, `swords_king`, …).
- Don't rename the `ci.yml` workflow ("CI") — it breaks the Ralph inner loop.
- Don't bypass quality gates; fix root causes (see `max-quality-no-shortcuts`).
