## Epic Summary

Build the reading-history experience: a most-recent-first list with detail view,
multi-select batch delete, clear-all, and storage-aware pruning at the 80%
threshold. Covers SPEC §6.2 (history flow), §8.3 (storage/prune), §10.2
(`HistoryViewModel`).

## Scope

**In scope:**
- `HistoryViewModel`: state (`pulls` ≤100, `selectedPull`, `isInEditMode`, `selectedPullIds`, `showsPruningAlert`, …) + `loadHistory()` recent 100 date desc.
- `HistoryScreen` (list of `HistoryRow`, empty state "No Readings Yet" + sparkles), `HistoryDetailScreen` (image/name/date/meaning).
- `HistoryRow` component (thumbnail + name + date + truncated note + note indicator).
- `StorageMonitorProtocol` + `StatFs` impl (threshold math, silent-zero on error) + prune ("Delete Oldest 50?" → `oldest(50)` → `deleteByIds`).
- Multi-select edit mode (enter/exit, toggle, isSelected, `deleteMultiplePulls`), "Delete N items", clear-all with destructive confirmation.

**Out of scope:**
- Note add/edit/delete from `HistoryDetailScreen` (Epic 5 wires note CRUD here).
- Theming/a11y polish (Epic 7).

## Success Criteria

The epic is done when:

- [ ] History shows the most-recent 100 pulls (date desc); empty state renders when none.
- [ ] Multi-select edit mode selects rows and batch-deletes; clear-all wipes with a destructive confirm.
- [ ] On load, if storage ≥80% used, the prune dialog appears and confirming deletes the oldest 50.
- [ ] `StorageMonitor` boundary math passes at 0 / 79% / 80% / 81% / total=0 (never throws).
- [ ] Child issues closed; VM 95–100%, StorageMonitor 95–100% (§5).

## Child Issues

- [ ] #24 — Add HistoryViewModel + HistoryScreen list/empty-state skeleton
- [ ] #25 — Wire loadHistory(100) + HistoryRow + HistoryDetailScreen
- [ ] #26 — Add StorageMonitor (StatFs) + prune oldest-50 flow
- [ ] #27 — Add multi-select edit mode, batch delete, and clear-all

## Sequencing Notes

- **Blocks:** Epic 5 (note CRUD into history detail).
- **Unblocked by:** Epic 2 (DAO + `CardPull`); benefits from Epic 3 having produced pulls but does not hard-depend on it (can seed fixtures).
- Parallel-safe with Epic 6.

## SPEC Reference

[`plans/SPEC.md`](../plans/SPEC.md) §6.2 (lines 254–270), §8.3 (lines 413–420), §10.2 (lines 457–465), §12 constants (lines 513–524).

## Labels

`epic`, `spec-decomposition`, `history`
