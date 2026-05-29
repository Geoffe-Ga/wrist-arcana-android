#!/usr/bin/env bash
# scripts/lint.sh - ktlint + detekt + Android Lint
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

if [ ! -x ./gradlew ]; then
  echo "ℹ️  Gradle not scaffolded yet (plans/SPEC.md Epic 1). Skipping lint. (exit 0)"
  exit 0
fi

./gradlew ktlintCheck detekt lintDebug
echo "✓ Lint passed"
