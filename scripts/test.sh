#!/usr/bin/env bash
# scripts/test.sh - Unit tests + coverage (Kover). Extra args pass through to Gradle.
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

if [ ! -x ./gradlew ]; then
  echo "ℹ️  Gradle not scaffolded yet (plans/SPEC.md Epic 1). Skipping tests. (exit 0)"
  exit 0
fi

./gradlew testDebugUnitTest koverXmlReport "$@"
echo "✓ Tests passed"
