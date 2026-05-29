#!/usr/bin/env bash
# scripts/check-all.sh - Run all quality checks (local dev + CI single source).
# Ported from the watchOS repo's run-tests gate to Gradle/Wear OS.
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

if [ ! -x ./gradlew ]; then
  echo "ℹ️  Gradle wrapper (./gradlew) not found — the Wear OS module is not"
  echo "    scaffolded yet. See plans/SPEC.md → Epic 1 (Project skeleton & CI)."
  echo "    Skipping ktlint/detekt/tests until the Gradle project lands. (exit 0)"
  exit 0
fi

echo "=== ktlint + detekt + Android Lint ==="
./gradlew ktlintCheck detekt lintDebug

echo "=== Unit tests + coverage (Kover) ==="
./gradlew testDebugUnitTest koverVerify

echo "✓ All quality checks passed!"
