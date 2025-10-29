#!/usr/bin/env bash
# Run lint and build checks for the clevel-sales-guy project.
#
# Usage examples:
#   scripts/clevel-sales-guy-verify.sh lint
#   scripts/clevel-sales-guy-verify.sh build
#   scripts/clevel-sales-guy-verify.sh all
#
# When run with `all` (or no explicit command), lint runs first, then build.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_DIR="${ROOT_DIR}/clevel-sales-guy"

if [[ ! -d "${PROJECT_DIR}" ]]; then
  echo "Project directory not found at ${PROJECT_DIR}" >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required to run these checks." >&2
  exit 1
fi

run_lint() {
  echo "→ Running npm run lint in clevel-sales-guy"
  (cd "${PROJECT_DIR}" && npm run lint)
}

run_build() {
  echo "→ Running npm run build in clevel-sales-guy"
  (cd "${PROJECT_DIR}" && npm run build)
}

run_all() {
  run_lint
  run_build
}

if [[ $# -eq 0 ]]; then
  run_all
  exit 0
fi

for task in "$@"; do
  case "${task}" in
    lint)
      run_lint
      ;;
    build)
      run_build
      ;;
    all)
      run_all
      ;;
    *)
      echo "Unknown task: ${task}" >&2
      echo "Supported tasks: lint, build, all" >&2
      exit 1
      ;;
  esac
done
