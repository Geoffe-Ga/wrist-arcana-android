#!/usr/bin/env bash
# scripts/typecheck.sh - Kotlin compile check (the JVM analogue of a type check)
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

if [ ! -x ./gradlew ]; then
  echo "ℹ️  Gradle not scaffolded yet (plans/SPEC.md Epic 1). Skipping compile check. (exit 0)"
  exit 0
fi

./gradlew compileDebugKotlin compileDebugUnitTestKotlin
echo "✓ Kotlin compiles"
