#!/usr/bin/env bash
# scripts/format.sh - Auto-format Kotlin with ktlint
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

if [ ! -x ./gradlew ]; then
  echo "ℹ️  Gradle not scaffolded yet (plans/SPEC.md Epic 1). Nothing to format. (exit 0)"
  exit 0
fi

./gradlew ktlintFormat
echo "✓ Formatted"
