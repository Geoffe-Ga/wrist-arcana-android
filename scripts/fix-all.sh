#!/usr/bin/env bash
# scripts/fix-all.sh - Auto-fix what tooling can (ktlint format)
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

if [ ! -x ./gradlew ]; then
  echo "ℹ️  Gradle not scaffolded yet (plans/SPEC.md Epic 1). Nothing to fix. (exit 0)"
  exit 0
fi

./gradlew ktlintFormat
echo "✓ Auto-fixes applied"
