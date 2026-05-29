# Wrist Arcana for Wear OS — Port Specification (SPEC)

> **Status:** Draft v1.0 — authoritative source for decomposition.
> **Purpose:** Recreate the **Wrist Arcana** watchOS tarot app *exactly as it is
> today* as a native **Wear OS / Android** watch app (Samsung Galaxy Watch,
> Pixel Watch, and other Wear OS 4+ devices). This document is the single
> source of truth an agent (or the Ralph loop, via `decompose`) uses to plan
> and build the port. It is intentionally **high-level and complete** — the
> per-issue breakdown is produced afterward by the `spec-decomposition`
> (`decompose`) skill.

---

## 0. How to use this document

1. Read this SPEC end-to-end before writing any code.
2. Run the `decompose` skill against it to file epics + child issues.
3. The Ralph loop (`/loop /ralph-tick`) then works issues one at a time.
4. The **source of truth for behavior** is the original watchOS app at
   `/Users/geoffgallinger/Projects/wrist-arcana` (referred to below as
   "the iOS repo" / "the original"). When this SPEC and the original
   disagree, **the original wins** — file a SPEC fix issue.

The bundled data file `DecksData.json` and the 78 card images are **reused
verbatim** from the original. Porting is about re-implementing behavior on a
new UI/persistence stack, not redesigning the product.

---

## 1. Product overview

Wrist Arcana is a **fully offline** tarot-card reading app for smartwatches.
Core promise: tap a button, get a cryptographically fair random card from the
78-card Rider–Waite deck, see its art and meaning, and keep a persistent
history of your readings with optional notes. A reference browser lets you
read every card's upright/reversed meanings and keywords without drawing.

**Non-negotiable product invariants** (carried over from the original):

- **100% offline.** No network calls, ever. All 78 card images and all card
  metadata ship inside the app. (Apple rejected connectivity-dependent watch
  apps; Wear OS review + the product thesis demand the same.)
- **Cryptographically fair draws.** Use a CSPRNG, not a seeded PRNG.
- **No-repeat within a session.** Each card appears once before any repeats,
  until the full deck has been drawn, then the cycle resets.
- **Persistent history**, capped/queried for watch performance, with storage
  monitoring and pruning.
- **Suspense delay** of ~0.5s on each draw for UX anticipation.
- **Multi-deck is built but hidden** behind a feature flag (IAP future work).

---

## 2. Goals / Non-goals

### Goals
- Faithful feature parity with the current watchOS app (every screen, every
  behavior listed in §6–§10).
- Idiomatic Wear OS implementation: Kotlin + Jetpack Compose for Wear OS +
  Room, MVVM, dependency injection, ≥ the original's test coverage bar.
- Reuse the original's `DecksData.json` and 78 card images unchanged (only
  repackaged into Android resources).
- Same quality gates as the original (tests-first/TDD, lint/format clean,
  CI green) enforced through this repo's green scaffold + Ralph loop.

### Non-goals (v1.0)
- Multi-deck UI (flag stays off — code path built, not exposed).
- Phone companion app. This is a **watch-only** app (mirrors the original's
  "no iOS stub target" decision). A phone module is explicitly out of scope.
- Cloud sync, accounts, analytics, ads, network of any kind.
- New features not present in the original. Parity first; net-new is a
  separate SPEC.

---

## 3. Technology mapping (watchOS → Wear OS)

This is the canonical translation table. Every architectural decision below
derives from it.

| Concern | Original (watchOS) | Port (Wear OS / Android) |
|---|---|---|
| Language | Swift 5.9+ | **Kotlin** (latest stable) |
| UI framework | SwiftUI (watchOS 10+) | **Jetpack Compose for Wear OS** (`androidx.wear.compose`) |
| Min platform | watchOS 10.0 | **Wear OS 4 / API 33** (`minSdk` 30 acceptable; target latest) |
| App entry / scene | `@main App` + `WindowGroup` | `ComponentActivity` + `setContent {}` (or Wear `SwiftUI`-equiv `WearApp`) |
| Navigation | `TabView(.page)` (3 swipe tabs) | `HorizontalPager` (Wear Compose) or `SwipeDismissableNavHost` + pager |
| Persistence | **SwiftData** (`@Model`, `ModelContext`) | **Room** (`@Entity`, `@Dao`, `RoomDatabase`) |
| Async | `async/await`, `@MainActor` | Kotlin **coroutines** + `Dispatchers.Main`/`viewModelScope`, `Flow` |
| State / VM | `ObservableObject` + `@Published` | `ViewModel` + `StateFlow`/`MutableStateFlow` (or Compose `mutableStateOf`) |
| DI | Protocol-based manual injection | Interfaces + constructor injection (Hilt **optional**; manual DI is fine and matches the original's style) |
| Bundled data | `DecksData.json` in bundle, decoded via `Codable` | Same JSON in `res/raw/` or `assets/`, decoded via **kotlinx.serialization** (preferred) or Moshi |
| Images | Asset Catalog imagesets (@1x/2x/3x) | **drawable resources** (or `assets/`) loaded by name; density buckets mdpi…xxxhdpi |
| CSPRNG | `SystemRandomNumberGenerator` | `java.security.SecureRandom` (wrapped behind an interface) |
| Haptics | `WKInterfaceDevice.current().play(.click)` | `Vibrator`/`VibratorManager` (`VibrationEffect`) or Wear `HapticFeedback` |
| Storage stats | `FileManager.attributesOfFileSystem` | `StatFs` on the app's files dir, or `StorageManager` |
| Date formatting | `DateFormatter` (medium/short) | `java.time` + `DateTimeFormatter` (localized medium/short) |
| Siri Shortcut / App Intent | `AppIntent` "Draw Tarot Card" | **Wear OS Tile** + optional **App Action / quick-launch complication**; the "draw and tell me" intent maps to a Tile tap or complication tap (see §10.4) |
| Build system | Xcode project | **Gradle (Kotlin DSL)**, single `:wear` (or `:app`) module |
| Unit tests | XCTest / Swift Testing | **JUnit5** + **Turbine** (Flow) + **MockK** + Robolectric where needed |
| UI tests | XCUITest | **Compose UI test** (`createAndroidComposeRule`) + (optional) UiAutomator |
| Lint/format | SwiftLint + SwiftFormat | **ktlint** + **detekt** (+ Android Lint) |
| Coverage | xccov | **Kover** (or JaCoCo) |

**Decision defaults** (override only with a logged `architectural-decisions`
note): kotlinx.serialization for JSON, manual constructor DI (no Hilt unless an
issue justifies it), StateFlow for VM state, drawable resources for card art,
SecureRandom behind a `RandomGenerator` interface.

---

## 4. Target project structure

A single Gradle module (watch-only). Mirror the original's package layout so
the mapping stays legible.

```
wrist-arcana-android/
├── settings.gradle.kts
├── build.gradle.kts                      # root
├── gradle/libs.versions.toml             # version catalog
├── app/                                  # the Wear OS module (name :app)
│   ├── build.gradle.kts                  # com.android.application + wear deps
│   └── src/
│       ├── main/
│       │   ├── AndroidManifest.xml       # <uses-feature android.hardware.type.watch>, standalone=true
│       │   ├── kotlin/com/wristarcana/
│       │   │   ├── WristArcanaApp.kt      # Application; builds the Room DB singleton
│       │   │   ├── MainActivity.kt        # ComponentActivity; setContent { WristArcanaRoot() }
│       │   │   ├── ui/                     # ← Views (Compose)
│       │   │   │   ├── WristArcanaRoot.kt  # pager host (Reference / Draw / History)
│       │   │   │   ├── draw/DrawCardScreen.kt
│       │   │   │   ├── draw/CardPreviewScreen.kt
│       │   │   │   ├── draw/CardDisplayScreen.kt
│       │   │   │   ├── history/HistoryScreen.kt
│       │   │   │   ├── history/HistoryDetailScreen.kt
│       │   │   │   ├── note/NoteEditorScreen.kt
│       │   │   │   ├── reference/CardReferenceScreen.kt
│       │   │   │   ├── reference/CardListScreen.kt
│       │   │   │   ├── reference/CardReferenceDetailScreen.kt
│       │   │   │   └── components/         # ← Components
│       │   │   │       ├── DrawButton.kt    # CTAButton
│       │   │   │       ├── CardImage.kt     # CardImageView (+ placeholder)
│       │   │   │       ├── HistoryRow.kt
│       │   │   │       └── FlowRow.kt       # keyword chips (Compose FlowRow)
│       │   │   ├── viewmodel/              # ← ViewModels
│       │   │   │   ├── CardDrawViewModel.kt
│       │   │   │   ├── HistoryViewModel.kt
│       │   │   │   ├── CardReferenceViewModel.kt
│       │   │   │   └── DeckSelectionViewModel.kt
│       │   │   ├── data/                    # ← Models + repositories + persistence
│       │   │   │   ├── model/TarotCard.kt   # data class + Suit enum
│       │   │   │   ├── model/TarotDeck.kt
│       │   │   │   ├── db/CardPull.kt        # @Entity (was SwiftData @Model)
│       │   │   │   ├── db/CardPullDao.kt
│       │   │   │   ├── db/WristArcanaDatabase.kt
│       │   │   │   ├── repo/DeckRepository.kt + DeckRepositoryProtocol (interface)
│       │   │   │   └── repo/CardRepository.kt + CardRepositoryProtocol (interface)
│       │   │   ├── util/                    # ← Utilities
│       │   │   │   ├── RandomGenerator.kt    # SecureRandom impl behind interface
│       │   │   │   ├── StorageMonitor.kt
│       │   │   │   ├── NoteInputSanitizer.kt
│       │   │   │   └── DateFormatting.kt
│       │   │   ├── config/                  # ← Configuration
│       │   │   │   ├── AppConstants.kt
│       │   │   │   ├── FeatureFlags.kt
│       │   │   │   └── Theme.kt              # Wear MaterialTheme colors/typography
│       │   │   ├── tile/                     # Wear OS Tile (maps the App Intent)
│       │   │   │   └── DrawCardTileService.kt
│       │   │   └── res/ or assets/
│       │   │       ├── raw/decks_data.json   # verbatim copy of DecksData.json
│       │   │       └── drawable-*/major_00.png … (78 cards × density buckets)
│       ├── test/        # JUnit unit tests (VMs, repos, utils, models)
│       └── androidTest/ # Compose UI tests
└── plans/               # this SPEC + decomposition artifacts (git-issues/)
```

> **Naming:** keep Kotlin file/type names 1:1 with the Swift originals where it
> aids traceability (e.g. `CardDrawViewModel`, `NoteInputSanitizer`). Card image
> resource names must match the original asset names exactly (see §7.3).

---

## 5. Architecture (MVVM + protocol/interface DI)

Preserve the original's strict layering:

- **UI (Compose)** — presentation only, no business logic. Reads
  `StateFlow`/state from a ViewModel, emits user events back to it.
- **ViewModels** — own all business logic and state; depend on **interfaces**
  (`DeckRepositoryProtocol`, `CardRepositoryProtocol`, `StorageMonitorProtocol`,
  `RandomGeneratorProtocol`) so they are 100% unit-testable with fakes/mocks.
- **Data layer** — repositories hydrate decks from JSON and persist pulls via
  Room DAO. Models are plain data classes / Room entities.
- **DI** — manual constructor injection (a small `AppContainer`/factory built in
  `WristArcanaApp`), matching the original's protocol-injection approach.
  ViewModels constructed via `ViewModelProvider.Factory` (or `viewModelFactory`)
  so the `ModelContext` analogue (the DAO) and repos are injected.

Coverage expectations (carry over the original's bar):

| Layer | Target |
|---|---|
| Models (TarotCard/Deck/CardPull) | 95–100% |
| ViewModels | 95–100% |
| Utilities (RNG, StorageMonitor, Sanitizer, DateFormatting) | 95–100% |
| Repositories | 90–100% |
| Components (composables with logic) | 60%+ |
| Screens | functional coverage via Compose UI tests |
| **Overall** | **≥50% gate** (match the original's CI floor; aim 60%+) |

---

## 6. Screens & navigation (feature parity)

The app is a 3-page horizontal pager. **Default/initial page is Draw (index 1).**

```
[0] Reference  ←→  [1] Draw (default)  ←→  [2] History
```

### 6.1 Draw flow (the core loop)

**DrawCardScreen** (was `DrawCardView`):
- Shows the app title ("Tarot"/"Wrist Arcana") and a large circular **DRAW**
  button (`DrawButton` / CTAButton). Button sizing is responsive to screen size
  (original: ~70% width, clamped 120–160dp, capped to ~60% available height;
  title ~12% screen height). Use `BoxWithConstraints` to replicate.
- Tapping DRAW:
  1. Enters loading state (button shows a progress spinner; disabled).
  2. Waits the **minimum draw duration** (~500ms) for suspense, *and* checks for
     cancellation if the user navigates away.
  3. Selects a random un-drawn card (CSPRNG, no-repeat — §8.1).
  4. Saves a `CardPull` to history (§8.2).
  5. Checks storage; if ≥80% used, raises a storage-warning dialog (§8.3).
  6. Fires a **haptic** ("click"-style) on success.
- On success a **CardPreviewScreen** is presented (full-bleed card art on a
  near-black background). From preview the user can open **CardDisplayScreen**
  (full detail). Replicate the original's modal layering with Compose
  navigation/`Dialog`/full-screen destinations.

**CardPreviewScreen** (was `CardPreviewView`):
- Black (~90% opacity) background, centered card image sized to the card aspect
  ratio (the original uses an 11:19 portrait card aspect). Tappable to open
  detail. Controls: a "Done"/dismiss action and an "info" action → open detail.

**CardDisplayScreen** (was `CardDisplayView`):
- Card image (11:19), card name (serif, ~20sp semibold), **upright meaning**.
- Note section: if a note exists, show it in a bordered box + "Edit Note";
  otherwise an "Add Note" (prominent) button. "Done" dismisses.
- "Add/Edit Note" opens **NoteEditorScreen**; saving persists the note to the
  `CardPull` created by this draw (§9).

### 6.2 History flow

**HistoryScreen** (was `HistoryView`):
- Scrollable list of `CardPull`s (most-recent first), each a **HistoryRow**
  (thumbnail + name + date + truncated note + note indicator). Tapping a row →
  **HistoryDetailScreen**.
- **Empty state:** "No Readings Yet" + sparkles icon.
- **Management:** a "Select" action enters multi-select edit mode; a "Clear All"
  action wipes history (with a destructive confirmation dialog).
- **Edit mode:** each row toggles a checkbox; a bottom "Delete N items" action
  performs a batch delete; "Done" exits edit mode.
- **Pruning:** on load, if storage ≥80%, show a "Storage Full — Delete Oldest
  50?" dialog → prune oldest 50 (§8.3).
- Pull-to-refresh (or on-resume) reloads history.

**HistoryDetailScreen** (was `HistoryDetailView`):
- Card image, name, **date drawn**, meaning, and full note management
  (add/edit/delete with a delete-note confirmation).

**NoteEditorScreen** (was `NoteEditorView`):
- Multiline text input, sentence capitalization, **live remaining-character
  counter** (max 500). Save is disabled when invalid (empty after trim or >500).
  Cancel/Save actions. Sanitization rules per §9.

### 6.3 Reference flow (browse, no draw)

**CardReferenceScreen** (was `CardReferenceView`):
- List of the **5 suits** in fixed order with icon + name + card count:
  Major Arcana (22, ⭐), Swords (14, ⚔️), Wands (14, 🪄), Pentacles (14, 🪙),
  Cups (14, 🏆). Tapping a suit → **CardListScreen**.

**CardListScreen** (was `CardListView`):
- Cards within the chosen suit (sorted by number), each a thumbnail + full
  display name. Tap → **CardReferenceDetailScreen**.

**CardReferenceDetailScreen** (was `CardReferenceDetailView`):
- Scrollable: card image, name + suit + display number (e.g. "⭐ Major Arcana •
  I"), **Upright** section (up-arrow, green accent), **Reversed** section
  (down-arrow, orange accent), and **Keywords** rendered as wrapping chips
  (Compose `FlowRow`, blue-tinted, ~12dp corner radius).

---

## 7. Data layer

### 7.1 Domain models

**`TarotCard`** (Swift struct → Kotlin data class; `Serializable`):
- `id: String` (the JSON uses string ids like `rw-major-00`; original decodes a
  `UUID` — **decode as String** to avoid UUID-format coupling, see §7.4),
  `name: String`, `imageName: String`, `suit: Suit`, `number: Int`,
  `upright: String`, `reversed: String`, `keywords: List<String>`.
- `Suit` enum: `MAJOR_ARCANA("Major Arcana")`, `SWORDS`, `WANDS`, `PENTACLES`,
  `CUPS`. Each carries `icon`, `cardCount`, `sortOrder` (Major=0, Swords=1,
  Wands=2, Pentacles=3, Cups=4) — match the original ordering exactly.
- Computed: `displayNumber` (Major → Roman numerals 0/`0`…`XXI`; minors →
  `Ace`/`Page`/`Knight`/`Queen`/`King`/`2`–`10` where number 1=Ace, 11=Page,
  12=Knight, 13=Queen, 14=King), `fullDisplayName` (Major → "I - The Magician"
  style; minors → plain name). **Port the exact mapping from the original.**
- `emergencyFallback`: a single "The Fool" card used if JSON load fails.

**`TarotDeck`** (data class): `id: String`, `name: String`,
`cards: List<TarotCard>`, computed `cardCount`. Static `fallback`/`riderWaite`
single-card decks for resilience.

### 7.2 JSON (`DecksData.json`) — schema (reuse verbatim)

Top-level `{ "decks": [ { "id", "name", "cards": [ Card… ] } ] }`. Each card:
`id, name, imageName, number, suit, upright, reversed, keywords[]`. One deck
("Rider-Waite", id `rider-waite-smith`), **78 cards**. Copy the file unchanged
into `res/raw/decks_data.json` (lowercase + underscores per Android resource
naming) or `assets/DecksData.json`. **Do not edit the content.**

### 7.3 Card images (78) — asset pipeline

- Naming (must match `imageName` in JSON and the original asset names):
  - Major: `major_00` … `major_21`
  - Minors per suit: `<suit>_01` … `<suit>_10`, `<suit>_page`, `<suit>_knight`,
    `<suit>_queen`, `<suit>_king` for suit ∈ {swords, wands, pentacles, cups}.
- Source art lives in the original repo's asset catalog (`@1x/@2x/@3x` PNGs) and
  in `scripts/RWS_Cards_Processed/` of the original. **Pipeline:** map Apple
  scales → Android density buckets and place into `res/drawable-*`:
  - `@1x → drawable-mdpi`, `@2x → drawable-xhdpi`, `@3x → drawable-xxxhdpi`
    (closest density equivalents; acceptable to ship a single high-res bucket
    `drawable-nodpi` if memory testing on-watch is fine — decide in the asset
    epic). Resource names must be lowercase: `major_00.png`, `cups_ace.png`?
    **No** — keep the JSON's exact `imageName` (`cups_01`, `swords_king`) so the
    loader can resolve `resources.getIdentifier(imageName, "drawable", pkg)` or a
    pre-built name→resId map (preferred over reflection; see §7.5).
- A build/CI check should assert **all 78 image names referenced by the JSON
  resolve to a real drawable** (port of the original's "78 cards present" check).

### 7.4 Persistence (`CardPull` → Room)

`CardPull` `@Entity` columns (1:1 with the SwiftData model):
`id: String` (PK, unique — use UUID string), `date: Long`/`Instant` (epoch),
`cardName: String`, `deckName: String`, `cardImageName: String`,
`cardDescription: String` (upright meaning *as of draw time*), `note: String?`.
Computed (non-persisted) helpers: `hasNote` (note non-blank after trim),
`truncatedNote` (first ~80 chars + "…").

`CardPullDao` queries:
- `insert(pull)`.
- `recent(limit: Int)`: `ORDER BY date DESC LIMIT :limit` — used by History with
  **limit 100** (the original's `maxPullsToDisplay`).
- `oldest(limit: Int)`: `ORDER BY date ASC LIMIT :limit` — used by prune.
- `delete(pull)`, `deleteByIds(ids)`, `deleteAll()`, `count()`.
- Expose `Flow<List<CardPull>>` for reactive history where it simplifies the VM.

`WristArcanaDatabase`: single-entity Room DB. Mirror the original's resilient
init — on open failure, fall back to a destructive recreate, and as a last
resort an **in-memory** database (so an upgrade can never crash the app). Build
the DB once as an application-scoped singleton (the SwiftData
`sharedModelContainer` analogue) to avoid lock contention with the Tile service.

### 7.5 Repositories

**`DeckRepository : DeckRepositoryProtocol`**
- `loadDecks(): List<TarotDeck>` — read `decks_data.json`, decode, **validate**:
  ≥1 deck; each deck has **exactly 78 cards**; each card has non-empty `name`,
  `imageName`, `upright`, `reversed`. On any failure: log + return
  `TarotDeck.fallback`. Port the exact validation + `DeckError` cases
  (`fileNotFound`, `noDeckFound`, `invalidDeckSize(expected,actual)`,
  `invalidCardData(cardId,reason)`, `loadFailed`, `notFound`).
- `getCurrentDeck(): TarotDeck` — first deck (by `defaultDeckId`) or fallback.
- `getRandomCard(deck): TarotCard?` — via the RNG interface.

**`CardRepository : CardRepositoryProtocol`** (reference browser)
- Loads cards once; `getAllCards()` sorted by `suit.sortOrder` then `number`;
  `getCards(suit)`; `getCard(id)`; `getSuits()` (5, sorted). Fallback to the
  single "Fool" card on load failure.

A **name→drawable-resId map** should be generated (codegen or a small hand-kept
map) so `CardImage` can resolve art without runtime reflection; the asset epic
owns this.

---

## 8. Core algorithms (port exactly)

### 8.1 Draw + no-repeat (CSPRNG)
```
drawnThisSession: MutableSet<String>   // card ids
fun selectRandomCard(deck): TarotCard? {
    if (drawnThisSession.size >= deck.cards.size) drawnThisSession.clear()
    val available = deck.cards.filterNot { it.id in drawnThisSession }
    val pick = available.randomOrNull(secureRandom) ?: deck.cards.randomOrNull(secureRandom)
    pick?.let { drawnThisSession += it.id }
    return pick
}
```
Use `SecureRandom` behind `RandomGeneratorProtocol`. `randomOrNull(secureRandom)`
= pick `secureRandom.nextInt(size)`. After a successful draw, add the id to the
session set. Resetting when the set covers the deck reproduces the original's
"each of 78 appears once, then reshuffle" guarantee.

### 8.2 Save to history
On draw, persist a `CardPull{ id=UUID, date=now, cardName, deckName,
cardImageName=card.imageName, cardDescription=card.upright, note=null }`.

### 8.3 Storage monitoring + pruning
- `StorageMonitor.isNearCapacity()`: `used / total > 0.80`. Compute `total` and
  `free` from `StatFs(filesDir.path)` (`blockCountLong * blockSizeLong`, etc.);
  `used = total - free`. Return false if `total <= 0`. Return 0 on any error
  (never throw) — match the original's silent-zero behavior.
- After a draw, if near capacity → storage-warning dialog (informational, OK).
- On History load, if near capacity → "Delete Oldest 50?" prune dialog; confirm
  → delete oldest 50 via `oldest(50)` then `deleteByIds`.

### 8.4 Suspense delay
`delay(AppConstants.MIN_DRAW_DURATION_MS = 500)` inside the draw coroutine,
cancellable (so navigating away aborts cleanly). Original value: 500ms
(`minimumDrawDuration = 500_000_000 ns`).

---

## 9. Note input rules (`NoteInputSanitizer` — port exactly)

- `MAX_CHARACTERS = 500`.
- `sanitize(input)`:
  1. Trim leading/trailing whitespace & newlines.
  2. Remove control characters **except** newline (`\n`) and tab (`\t`).
  3. Truncate to 500 chars.
  4. Collapse runs of **3+ newlines** to exactly 2 (`\n{3,}` → `\n\n`).
- `isValid(input)`: non-empty after trim **and** length ≤ 500.
- `remainingCharacters(input)`: `max(0, 500 - input.length)`.
- Saving: sanitize; if result is empty → store `note = null`; else store
  sanitized. Editing fetches the pull by id, updates `note`, persists, reloads.

---

## 10. ViewModels (state + behavior)

Each is an Android `ViewModel` exposing `StateFlow` of an immutable UI-state
data class; methods mutate via `viewModelScope`. Inject interfaces + DAO.

### 10.1 `CardDrawViewModel`
State: `currentCard: TarotCard?`, `currentCardPull: CardPull?`,
`isDrawing: Bool`, `showsStorageWarning: Bool`, `errorMessage: String?`.
Behavior: `drawCard()` (suspense delay → cancellation check → select → save →
storage check → haptic → clear loading; set `errorMessage` on failure),
`dismissCard()`, `acknowledgeStorageWarning()`. Holds the session
`drawnThisSession` set (§8.1).

### 10.2 `HistoryViewModel`
State: `pulls: List<CardPull>` (≤100), `selectedPull`, `showsPruningAlert`,
`showsNoteEditor`, `editingNote: String`, `isEditingExistingNote: Bool`,
`isInEditMode: Bool`, `selectedPullIds: Set<String>`.
Behavior: `loadHistory()` (recent 100, date desc), `deletePull(p)`,
`checkStorageAndPruneIfNeeded()`, `pruneOldestPulls(50)`, note CRUD
(`startAddingNote`, `saveNote`, `deleteNote`, `dismissNoteEditor`), multi-select
(`enterEditMode`, `exitEditMode`, `toggleSelection`, `isSelected`,
`deleteMultiplePulls(ids)`), `clearAllHistory()`. `maxPullsToDisplay = 100`.

### 10.3 `CardReferenceViewModel`
State: `suits: List<Suit>`, `selectedSuit`, `cardsInSuit`, `selectedCard`.
Behavior: `loadSuits()`, `selectSuit(s)` (filter+sort), `selectCard`,
`deselectCard`, `cardCount(suit)`.

### 10.4 `DeckSelectionViewModel` (hidden, flag-gated)
State: `availableDecks`, `selectedDeckId`, `errorMessage`. Behavior:
`loadDecks()`, `selectDeck(id)`. Surfaced in UI **only** when
`FeatureFlags.MULTI_DECK_ENABLED == true` (default **false**).

### 10.5 "Draw a card" quick action (App Intent analogue)
The original ships an `AppIntent` ("Draw Tarot Card") + `AppShortcutsProvider`
(Siri phrases) that draws in the background and speaks the card + upright.
Wear OS has no Siri intents; map this to:
- **Primary:** a **Tile** (`DrawCardTileService`) showing a DRAW button; tapping
  draws (reusing `CardDrawViewModel`'s logic via a shared use-case), persists the
  pull, and deep-links into `CardDisplayScreen`.
- **Optional:** a **complication** / app shortcut that launches straight into a
  draw. Background "draw without opening" parity is satisfied by the Tile
  performing the draw + save and rendering the result inline.
The draw/save logic MUST be extracted into a shared use-case so the Activity,
Tile, and tests all share one code path (the original shares
`sharedModelContainer` for exactly this reason).

---

## 11. Theming, layout & accessibility

- **Theme** (`Theme.kt`): port the palette — primary gradient **purple→blue**
  (top-left→bottom-right), **black** card background. Typography: title ~32sp
  bold serif, card name ~20sp semibold serif, body ~14sp regular. Spacing scale
  8/16/24dp. Use Wear `MaterialTheme` with a custom color/typography set.
- **Card aspect ratio:** 11:19 portrait — enforce with `aspectRatio(11f/19f)`.
- **Responsive sizing:** use `BoxWithConstraints` to reproduce the
  percentage-of-screen sizing of the DRAW button/title across round + square and
  small/large Wear devices. Account for the system time/inset (Wear `TimeText`).
- **Image placeholder:** when a drawable can't be resolved, render a
  purple/blue gradient box (11:19) with an icon + the card name (port of
  `CardImageView`'s fallback).
- **Accessibility:** every interactive element gets a `contentDescription`/
  semantics label (e.g. DRAW = "Draw a tarot card", card image = "Tarot card:
  <name>"). History rows merge semantics into one element. Verify with
  TalkBack. This is parity work, not optional.

---

## 12. Configuration constants (`AppConstants` / `FeatureFlags`)

| Constant | Value | Notes |
|---|---|---|
| `MAX_HISTORY_ITEMS` | 500 | hard cap on stored pulls |
| `STORAGE_WARNING_THRESHOLD` | 0.80 | 80% used |
| `MIN_DRAW_DURATION_MS` | 500 | suspense delay |
| `DEFAULT_DECK_ID` | `"rider-waite-smith"` | the only deck in v1 |
| `MAX_PULLS_TO_DISPLAY` | 100 | history query cap |
| `NOTE_MAX_CHARACTERS` | 500 | note limit |
| `FeatureFlags.MULTI_DECK_ENABLED` | `false` | hides deck selection |

---

## 13. Testing strategy

TDD is mandatory (Red→Green→Refactor), same as the original. Mirror the test
suites:

- **Unit (JUnit5 + MockK + Turbine):**
  - Models: `displayNumber`/`fullDisplayName` mappings for all 78 cards; suit
    counts/sort order; `CardPull.hasNote`/`truncatedNote`.
  - `NoteInputSanitizer`: trim, control-char stripping (keep `\n`/`\t`), 500
    truncation, `\n{3,}`→`\n\n`, `isValid`, `remainingCharacters` (table tests).
  - `RandomGenerator`: distribution sanity + no-repeat-until-exhausted invariant
    (statistical fairness test like the original's).
  - `StorageMonitor`: threshold math at boundaries (0, 79%, 80%, 81%, total=0).
  - Repositories: JSON loads 1 deck × 78 cards; validation throws/falls back on
    malformed data (bad count, empty field, missing file); sort orders.
  - ViewModels: draw saves a pull + sets `currentCard`; no-repeat across N draws;
    storage warning toggles at threshold; history load caps at 100; prune deletes
    oldest 50; note save sanitizes + nulls empty; multi-delete; clear-all.
- **Compose UI tests (androidTest):** DRAW shows a card; preview→detail
  navigation; add/edit/delete note; history empty state; edit-mode multi-delete;
  reference suit→list→detail navigation; keyword chips render.
- **Asset integrity test:** every `imageName` in the JSON resolves to a drawable
  (the "78 present" gate).
- **Coverage gate:** Kover ≥ overall floor (≥50%, target 60%+), with the
  per-layer targets in §5.

---

## 14. Build, CI & quality gates

- **Gradle (Kotlin DSL)**, version catalog in `gradle/libs.versions.toml`.
- **Quality scripts** (`scripts/*.sh`, invoked by CLAUDE.md + CI):
  `format.sh` → `ktlintFormat`; `lint.sh` → `ktlintCheck` + `detekt` + Android
  Lint; `test.sh` → `./gradlew test` (+ `connectedCheck` where an emulator is
  available); `typecheck.sh` → Kotlin compile; `check-all.sh` → the lot +
  coverage. Until the Gradle skeleton lands (Epic 1), scripts no-op with a clear
  "not yet scaffolded" message so pre-commit/CI stay green.
- **CI (`.github/workflows/ci.yml`):** JDK 17 + Gradle cache; run `ktlint`,
  `detekt`, unit tests + Kover; assemble debug APK; (optional) a Wear emulator
  matrix for instrumented tests. Pre-commit job (generic hooks + ktlint +
  detect-secrets).
- **Pre-commit:** generic hooks (trailing-whitespace, EOF, yaml/json,
  large-files, detect-private-key), **ktlint**, **detect-secrets** (baseline),
  shellcheck for `scripts/`.
- **The Ralph loop** (`/loop /ralph-tick`) drives implementation issue-by-issue;
  `iteration-trigger.yml` posts the verdict/auto-merge nudge. CI's job name must
  stay **"CI"** so `iteration-trigger.yml`'s `workflow_run` filter matches.

---

## 15. Wear OS-specific concerns & risks

- **Standalone app:** declare `<uses-feature android:name="android.hardware.type.watch">`
  and `<meta-data ... standalone value="true">` so it installs without a phone.
- **Memory:** 78 full-res card PNGs can be heavy on a watch. Load on demand,
  size images to the displayed bounds, and avoid decoding all 78 at once
  (the reference list should use small thumbnails). Validate on a low-end
  Galaxy Watch.
- **Round vs square + chin/inset:** test layouts on round, square, and
  small-screen Wear targets; use `TimeText`/`ScalingLazyColumn` idioms.
- **Pager vs SwipeDismiss:** Wear's swipe-to-dismiss gesture can conflict with a
  horizontal pager — verify gesture handling; prefer Wear Compose `HorizontalPager`
  which is designed for this.
- **Haptics permission:** `<uses-permission android:name="android.permission.VIBRATE"/>`.
- **No background Siri analogue:** the App Intent maps to a Tile/complication
  (§10.5); set expectations that "hands-free voice draw" is not 1:1.
- **Data/UUID coupling:** the JSON ids are strings; decode as `String` (not
  `UUID`) to avoid format-validation failures the original tolerates.

---

## 16. Decomposition guidance (epics — to be expanded by `decompose`)

Suggested epic shape (tracer-code ordering — skeleton first, demoable at every
step). The `spec-decomposition` skill will turn these into sequenced issues.

1. **Epic: Project skeleton & CI** — Gradle module, Wear Compose dependency,
   manifest (standalone watch), empty 3-page pager that builds + launches; CI
   green (ktlint/detekt/test/assemble); quality scripts real. *Bootstrap note:
   like the original's manual Xcode skeleton, this epic may be landed by hand
   before starting Ralph, then Ralph picks up from Epic 2.*
2. **Epic: Data layer** — JSON + 78 images imported; `TarotCard`/`TarotDeck`,
   serialization, `DeckRepository`/`CardRepository` with validation + fallbacks;
   asset-integrity test; Room `CardPull`/DAO/DB with resilient init.
3. **Epic: Draw experience** — `RandomGenerator`, no-repeat algorithm,
   `CardDrawViewModel`, DrawButton, suspense delay, haptics, preview + display
   screens, save-to-history.
4. **Epic: History** — list/detail, HistoryRow, multi-select delete, clear-all,
   storage monitor + prune, `HistoryViewModel`.
5. **Epic: Notes** — `NoteInputSanitizer`, NoteEditor, note CRUD wired into draw
   + history detail.
6. **Epic: Reference browser** — `CardReferenceViewModel`, suit list, card list,
   reference detail with upright/reversed/keywords (FlowRow chips).
7. **Epic: Theming, accessibility & responsive layout** — Theme, semantics
   labels, round/square/small-screen passes.
8. **Epic: Quick-draw surfaces** — Tile (and optional complication) reusing the
   shared draw use-case.
9. **Epic (deferred/flag-gated): Multi-deck** — DeckSelection UI behind
   `MULTI_DECK_ENABLED`.

Each issue must carry: tracer-code sequencing, 6-component prompt body,
stay-green Done-Done gates, and the max-quality anti-bypass clause.

---

## 17. Definition of done (the port is "done" when…)

- All §6 screens exist and match the original's behavior and flows.
- All §8/§9 algorithms reproduce the original's outputs (verified by tests).
- 78 cards load offline from bundled resources; zero network calls anywhere.
- History persists across launches; storage warning + prune work at the 80%
  threshold; notes sanitize + persist per §9.
- CSPRNG no-repeat invariant holds; suspense delay + haptic on draw.
- Reference browser shows all 78 cards with upright/reversed/keywords.
- CI green; coverage ≥ floor; ktlint/detekt clean; the Tile draws + deep-links.
- Multi-deck remains hidden (flag off) but code-complete behind the flag.

---

## Appendix A — Source-of-truth file map (original → port)

| Original (Swift) | Port (Kotlin) |
|---|---|
| `WristArcanaApp.swift` (sharedModelContainer, resilient init) | `WristArcanaApp.kt` + `WristArcanaDatabase.kt` |
| `Views/MainView.swift` (TabView .page) | `ui/WristArcanaRoot.kt` (HorizontalPager) |
| `Views/DrawCardView.swift` | `ui/draw/DrawCardScreen.kt` |
| `Views/CardPreviewView.swift` | `ui/draw/CardPreviewScreen.kt` |
| `Views/CardDisplayView.swift` | `ui/draw/CardDisplayScreen.kt` |
| `Views/HistoryView.swift` | `ui/history/HistoryScreen.kt` |
| `Views/HistoryDetailView.swift` | `ui/history/HistoryDetailScreen.kt` |
| `Views/NoteEditorView.swift` | `ui/note/NoteEditorScreen.kt` |
| `Views/CardReferenceView.swift` | `ui/reference/CardReferenceScreen.kt` |
| `Views/CardListView.swift` | `ui/reference/CardListScreen.kt` |
| `Views/CardReferenceDetailView.swift` | `ui/reference/CardReferenceDetailScreen.kt` |
| `Views/DeckSelectionView.swift` (hidden) | `ui/.../DeckSelectionScreen.kt` (flag-gated) |
| `ViewModels/*ViewModel.swift` | `viewmodel/*ViewModel.kt` |
| `Models/CardPull.swift` (@Model) | `data/db/CardPull.kt` (@Entity) + DAO |
| `Models/TarotCard.swift` / `TarotDeck.swift` | `data/model/TarotCard.kt` / `TarotDeck.kt` |
| `Models/DeckRepository.swift` / `CardRepository.swift` | `data/repo/*Repository.kt` |
| `Utilities/RandomGenerator.swift` | `util/RandomGenerator.kt` (SecureRandom) |
| `Utilities/StorageMonitor.swift` | `util/StorageMonitor.kt` (StatFs) |
| `Utilities/NoteInputSanitizer.swift` | `util/NoteInputSanitizer.kt` |
| `Utilities/Extensions/Date+Formatting.swift` | `util/DateFormatting.kt` (java.time) |
| `Configuration/AppConstants.swift` / `Theme.swift` | `config/AppConstants.kt` + `FeatureFlags.kt` + `Theme.kt` |
| `Components/CTAButton.swift` | `ui/components/DrawButton.kt` |
| `Components/CardImageView.swift` | `ui/components/CardImage.kt` |
| `Components/HistoryRow.swift` | `ui/components/HistoryRow.kt` |
| `Components/FlowLayout.swift` | `ui/components/FlowRow.kt` (Compose FlowRow) |
| `AppIntents/DrawCardIntent.swift` + `AppShortcutsProvider.swift` | `tile/DrawCardTileService.kt` (+ optional complication) |
| `Resources/DecksData.json` | `res/raw/decks_data.json` (verbatim) |
| `Resources/Assets.xcassets/RiderWaite/*` | `res/drawable-*/<imageName>.png` (78) |

## Appendix B — Open questions to resolve during decomposition
- Single high-res `drawable-nodpi` bucket vs per-density buckets (memory test on
  a real Galaxy Watch decides).
- Hilt vs manual DI (default manual; revisit only if wiring the Tile + Activity
  + tests gets unwieldy).
- `res/raw` vs `assets/` for the JSON (raw is simpler with kotlinx.serialization).
- Exact Wear navigation primitive (HorizontalPager vs SwipeDismissableNavHost +
  pager) — prototype in Epic 1.
