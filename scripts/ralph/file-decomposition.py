#!/usr/bin/env python3
"""One-shot: file the SPEC decomposition (9 epics + 32 children) to GitHub.

Deterministic order: create labels -> file epics -> substitute epic numbers ->
file children in dependency order (substituting each child's number across all
remaining bodies) -> push fully-resolved child bodies -> rewrite epic checklists.
"""
import re
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "git-issues"

# label -> (description, color)
LABELS = {
    "epic": ("Tracks a workstream from a SPEC", "5319e7"),
    "spec-decomposition": ("Issue filed from a SPEC decomposition", "0e8a16"),
    "skeleton": ("Tracer-code skeleton issue (wire surfaces with stubs)", "c5def5"),
    "core": ("Core feature issue (replace a stub with real logic)", "1d76db"),
    "edges": ("Edge cases, validation, error paths", "fbca04"),
    "polish": ("Polish: logging, metrics, docs, perf, a11y", "bfdadc"),
    "future-work": ("Deferred — Ralph picker skips this", "cccccc"),
    "multi-deck": ("Multi-deck feature (flag-gated)", "d4c5f9"),
    "build": ("Gradle/build system", "e99695"),
    "ci": ("Continuous integration", "e99695"),
    "ui": ("Compose UI", "fef2c0"),
    "data": ("Data layer (models/repos/persistence)", "0052cc"),
    "assets": ("Image/asset pipeline", "fef2c0"),
    "persistence": ("Room database", "0052cc"),
    "draw": ("Draw experience", "b60205"),
    "history": ("Reading history", "006b75"),
    "notes": ("Reading notes", "5319e7"),
    "reference": ("Reference browser", "0e8a16"),
    "theming": ("Theme/layout/responsive", "fbca04"),
    "accessibility": ("Accessibility/TalkBack", "fbca04"),
    "tile": ("Wear OS Tile / quick-draw", "1d76db"),
}

# (file, title, labels)
EPICS = [
    ("EPIC_01_skeleton-ci.md", "epic: Project skeleton & CI", "epic,spec-decomposition,skeleton"),
    ("EPIC_02_data-layer.md", "epic: Data layer", "epic,spec-decomposition,data"),
    ("EPIC_03_draw-experience.md", "epic: Draw experience", "epic,spec-decomposition,draw"),
    ("EPIC_04_history.md", "epic: History", "epic,spec-decomposition,history"),
    ("EPIC_05_notes.md", "epic: Notes", "epic,spec-decomposition,notes"),
    ("EPIC_06_reference-browser.md", "epic: Reference browser", "epic,spec-decomposition,reference"),
    ("EPIC_07_theming-a11y-responsive.md", "epic: Theming, accessibility & responsive layout", "epic,spec-decomposition,theming"),
    ("EPIC_08_quick-draw-tile.md", "epic: Quick-draw surfaces (Tile)", "epic,spec-decomposition,tile"),
    ("EPIC_09_multi-deck-deferred.md", "epic: Multi-deck (deferred, flag-gated)", "epic,spec-decomposition,future-work,multi-deck"),
]

# epic_key -> ordered list of (file, title, labels)
CHILDREN = {
    "EPIC_01": [
        ("EPIC_01_ISSUE_01_gradle-module-skeleton.md", "feat(build): Wire Gradle Wear module, manifest, and MainActivity skeleton", "spec-decomposition,skeleton,build"),
        ("EPIC_01_ISSUE_02_three-page-pager.md", "feat(ui): Add 3-page HorizontalPager (Reference/Draw/History) with placeholders", "spec-decomposition,core,ui"),
        ("EPIC_01_ISSUE_03_real-quality-scripts.md", "chore(build): Wire real ktlint/detekt/Android Lint/Kover quality scripts", "spec-decomposition,core,build"),
        ("EPIC_01_ISSUE_04_ci-real-tasks.md", "ci: Run real quality tasks + assembleDebug + coverage gate in CI", "spec-decomposition,core,ci"),
    ],
    "EPIC_02": [
        ("EPIC_02_ISSUE_01_domain-models.md", "feat(data): Add TarotCard/Suit/TarotDeck models, DeckError, and repo interfaces", "spec-decomposition,skeleton,data"),
        ("EPIC_02_ISSUE_02_deck-repository-json.md", "feat(data): Load DecksData.json and implement DeckRepository with validation+fallback", "spec-decomposition,core,data"),
        ("EPIC_02_ISSUE_03_card-repository.md", "feat(data): Implement CardRepository (sorted getAll/getCards/getCard/getSuits)", "spec-decomposition,core,data"),
        ("EPIC_02_ISSUE_04_card-images-resid-map.md", "feat(data): Import 78 card images + name->resId map + asset-integrity test", "spec-decomposition,core,data,assets"),
        ("EPIC_02_ISSUE_05_room-cardpull-dao-db.md", "feat(data): Add Room CardPull entity/DAO/DB with resilient init", "spec-decomposition,core,data,persistence"),
    ],
    "EPIC_03": [
        ("EPIC_03_ISSUE_01_rng-viewmodel-skeleton.md", "feat(draw): Add RandomGenerator + CardDrawViewModel state + DrawCardScreen skeleton", "spec-decomposition,skeleton,draw"),
        ("EPIC_03_ISSUE_02_no-repeat-algorithm.md", "feat(draw): Implement CSPRNG no-repeat selection algorithm", "spec-decomposition,core,draw"),
        ("EPIC_03_ISSUE_03_suspense-haptic-save.md", "feat(draw): Add suspense delay, haptic, and save-to-history on draw", "spec-decomposition,core,draw"),
        ("EPIC_03_ISSUE_04_preview-display-screens.md", "feat(draw): Add CardPreviewScreen + CardDisplayScreen with preview->detail nav", "spec-decomposition,core,draw,ui"),
        ("EPIC_03_ISSUE_05_storage-warning-error.md", "feat(draw): Add post-draw storage warning dialog and error surfacing", "spec-decomposition,edges,draw"),
    ],
    "EPIC_04": [
        ("EPIC_04_ISSUE_01_history-skeleton.md", "feat(history): Add HistoryViewModel + HistoryScreen list/empty-state skeleton", "spec-decomposition,skeleton,history"),
        ("EPIC_04_ISSUE_02_load-history-row-detail.md", "feat(history): Wire loadHistory(100) + HistoryRow + HistoryDetailScreen", "spec-decomposition,core,history"),
        ("EPIC_04_ISSUE_03_storage-monitor-prune.md", "feat(history): Add StorageMonitor (StatFs) + prune oldest-50 flow", "spec-decomposition,core,history"),
        ("EPIC_04_ISSUE_04_multiselect-clear-all.md", "feat(history): Add multi-select edit mode, batch delete, and clear-all", "spec-decomposition,edges,history"),
    ],
    "EPIC_05": [
        ("EPIC_05_ISSUE_01_sanitizer-editor.md", "feat(notes): Add NoteInputSanitizer + NoteEditorScreen with live counter", "spec-decomposition,skeleton,notes"),
        ("EPIC_05_ISSUE_02_note-crud-draw.md", "feat(notes): Wire note add/edit persistence into the draw flow", "spec-decomposition,core,notes"),
        ("EPIC_05_ISSUE_03_note-crud-history-detail.md", "feat(notes): Wire note add/edit/delete into HistoryDetailScreen", "spec-decomposition,core,notes"),
    ],
    "EPIC_06": [
        ("EPIC_06_ISSUE_01_reference-skeleton.md", "feat(reference): Add CardReferenceViewModel + suit list screen skeleton", "spec-decomposition,skeleton,reference"),
        ("EPIC_06_ISSUE_02_card-list.md", "feat(reference): Add CardListScreen (cards sorted by number)", "spec-decomposition,core,reference"),
        ("EPIC_06_ISSUE_03_reference-detail-flowrow.md", "feat(reference): Add CardReferenceDetailScreen + FlowRow keyword chips", "spec-decomposition,core,reference,ui"),
    ],
    "EPIC_07": [
        ("EPIC_07_ISSUE_01_theme-palette.md", "feat(theming): Implement Theme.kt palette + typography across screens", "spec-decomposition,core,theming"),
        ("EPIC_07_ISSUE_02_responsive-placeholder.md", "feat(theming): Add responsive BoxWithConstraints sizing + CardImage placeholder", "spec-decomposition,core,theming"),
        ("EPIC_07_ISSUE_03_accessibility.md", "feat(a11y): Add accessibility semantics + TalkBack pass", "spec-decomposition,polish,accessibility"),
    ],
    "EPIC_08": [
        ("EPIC_08_ISSUE_01_shared-usecase-tile-shell.md", "feat(tile): Extract shared DrawUseCase + DrawCardTileService shell", "spec-decomposition,skeleton,tile"),
        ("EPIC_08_ISSUE_02_tile-draw-deeplink.md", "feat(tile): Tile draws+saves via use-case and deep-links to CardDisplay", "spec-decomposition,core,tile"),
        ("EPIC_08_ISSUE_03_complication-shortcut.md", "feat(tile): Add optional complication / app shortcut quick-draw", "spec-decomposition,polish,tile"),
    ],
    "EPIC_09": [
        ("EPIC_09_ISSUE_01_deck-selection-flag-gated.md", "feat(multi-deck): Add DeckSelection VM+screen behind MULTI_DECK_ENABLED", "spec-decomposition,skeleton,future-work,multi-deck"),
        ("EPIC_09_ISSUE_02_wire-deck-selection.md", "feat(multi-deck): Wire deck selection into draw/reference (flag-gated)", "spec-decomposition,core,future-work,multi-deck"),
    ],
}

SLOT_RE = re.compile(r"^(EPIC_\d+)_ISSUE_(\d+)_")


def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(f"FAILED: {' '.join(cmd)}\n{res.stderr}\n")
        sys.exit(1)
    return res.stdout.strip()


def issue_number(url):
    return url.rstrip("/").split("/")[-1]


def slot_token(child_file):
    m = SLOT_RE.match(child_file)
    return f"{m.group(1)}_ISSUE_{m.group(2)}_NUMBER"


def all_child_files():
    return [DIR / f for epic in CHILDREN.values() for (f, _, _) in epic]


def sub_in_all_children(token, value):
    for p in all_child_files():
        text = p.read_text()
        if token in text:
            p.write_text(text.replace(token, value))


def main():
    # Step A: self-reference -> slot token, per child file
    for ek, items in CHILDREN.items():
        for (f, _, _) in items:
            p = DIR / f
            p.write_text(p.read_text().replace("THIS_ISSUE_NUMBER", slot_token(f)))
    print("A: resolved THIS_ISSUE_NUMBER -> slot tokens")

    # Step B: labels
    for name, (desc, color) in LABELS.items():
        subprocess.run(["gh", "label", "create", name, "--description", desc,
                        "--color", color], capture_output=True, text=True)
    print(f"B: ensured {len(LABELS)} labels")

    # Step C: file epics
    epic_num = {}
    for (f, title, labels) in EPICS:
        url = run(["gh", "issue", "create", "--title", title,
                   "--body-file", str(DIR / f), "--label", labels])
        n = issue_number(url)
        key = f[:7]  # EPIC_0N
        epic_num[key] = n
        print(f"C: {title} -> #{n}")

    # Step D: substitute parent-epic numbers into all child files
    for key, n in epic_num.items():
        sub_in_all_children(f"{key}_NUMBER", n)
    print("D: substituted parent-epic numbers")

    # Step E: file children in dependency order; substitute each number as we go
    child_num = {}      # file -> number
    child_meta = {}     # file -> (epic_key, title)
    for key in CHILDREN:
        for (f, title, labels) in CHILDREN[key]:
            url = run(["gh", "issue", "create", "--title", title,
                       "--body-file", str(DIR / f), "--label", labels])
            n = issue_number(url)
            child_num[f] = n
            child_meta[f] = (key, title)
            sub_in_all_children(slot_token(f), n)  # resolve self + downstream refs
            print(f"E: {title} -> #{n}")

    # Step F: push fully-resolved child bodies (self-close refs now real)
    for f, n in child_num.items():
        run(["gh", "issue", "edit", n, "--body-file", str(DIR / f)])
    print("F: pushed resolved child bodies")

    # Step G: rewrite each epic's Child Issues checklist with real numbers
    for (f, title, labels) in EPICS:
        key = f[:7]
        bullets = []
        for (cf, ctitle, _) in CHILDREN[key]:
            short = ctitle.split(": ", 1)[1] if ": " in ctitle else ctitle
            bullets.append(f"- [ ] #{child_num[cf]} — {short}")
        block = "## Child Issues\n\n" + "\n".join(bullets) + "\n\n"
        p = DIR / f
        text = p.read_text()
        # replace from "## Child Issues" up to the next "## " heading
        new = re.sub(r"## Child Issues\n.*?(?=\n## )", block.rstrip() + "\n", text,
                     count=1, flags=re.DOTALL)
        p.write_text(new)
        run(["gh", "issue", "edit", epic_num[key], "--body-file", str(p)])
        print(f"G: updated checklist for {title} (#{epic_num[key]})")

    # Summary
    print("\n=== FILED ===")
    for (f, title, _) in EPICS:
        key = f[:7]
        print(f"Epic #{epic_num[key]}: {title}")
        for (cf, ctitle, _) in CHILDREN[key]:
            print(f"   #{child_num[cf]}: {ctitle}")


if __name__ == "__main__":
    main()
