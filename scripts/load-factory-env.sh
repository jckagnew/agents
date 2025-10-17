#!/usr/bin/env bash

# Usage:
#   source scripts/load-factory-env.sh
# or
#   . scripts/load-factory-env.sh
#
# This will export the Supabase observability variables required by the
# software-factory instrumentation for the current shell session.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ROOT_DIR}/.env"

function log() {
  echo "[factory-env] $*"
}

# Helper to read key=value pairs, ignoring comments/blank lines.
function export_from_file() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    return
  fi

  while IFS='=' read -r key value; do
    # strip whitespace
    key="$(echo "$key" | xargs)"
    value="$(echo "$value" | xargs)"

    # skip empty or commented lines
    [[ -z "$key" ]] && continue
    [[ "$key" == \#* ]] && continue

    case "$key" in
      FACTORY_*|EXPO_PUBLIC_FACTORY_*)
        export "$key"="$value"
        ;;
    esac
  done < <(grep -E '^(FACTORY_|EXPO_PUBLIC_FACTORY_)' "$file" 2>/dev/null || true)
}

export_from_file "$ENV_FILE"

# Prompt for missing values (optional but helps when .env is incomplete)
if [[ -z "${FACTORY_SUPABASE_URL:-}" ]]; then
  read -rp "FACTORY_SUPABASE_URL (e.g. https://xxx.supabase.co): " url
  FACTORY_SUPABASE_URL="$url"
  export FACTORY_SUPABASE_URL
fi

if [[ -z "${FACTORY_SUPABASE_SERVICE_KEY:-}" && -z "${FACTORY_SUPABASE_ANON_KEY:-}" ]]; then
  read -rp "FACTORY_SUPABASE_SERVICE_KEY (press enter to skip): " svc
  if [[ -n "$svc" ]]; then
    FACTORY_SUPABASE_SERVICE_KEY="$svc"
    export FACTORY_SUPABASE_SERVICE_KEY
  else
    read -rp "FACTORY_SUPABASE_ANON_KEY (fallback anon key): " anon
    FACTORY_SUPABASE_ANON_KEY="$anon"
    export FACTORY_SUPABASE_ANON_KEY
  fi
fi

# Expo/React Native variables mirror web ones if not set explicitly.
if [[ -z "${EXPO_PUBLIC_FACTORY_SUPABASE_URL:-}" && -n "${FACTORY_SUPABASE_URL:-}" ]]; then
  export EXPO_PUBLIC_FACTORY_SUPABASE_URL="$FACTORY_SUPABASE_URL"
fi

if [[ -z "${EXPO_PUBLIC_FACTORY_SUPABASE_SERVICE_KEY:-}" && -n "${FACTORY_SUPABASE_SERVICE_KEY:-}" ]]; then
  export EXPO_PUBLIC_FACTORY_SUPABASE_SERVICE_KEY="$FACTORY_SUPABASE_SERVICE_KEY"
fi

if [[ -z "${EXPO_PUBLIC_FACTORY_SUPABASE_ANON_KEY:-}" && -n "${FACTORY_SUPABASE_ANON_KEY:-}" ]]; then
  export EXPO_PUBLIC_FACTORY_SUPABASE_ANON_KEY="$FACTORY_SUPABASE_ANON_KEY"
fi

log "Factory Supabase environment variables loaded for this session."
