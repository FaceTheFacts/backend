#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
scan_args=("$@")

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'USAGE'
Usage: scripts/scan-secrets.sh [gitleaks detect options]

Runs gitleaks against this repository. Uses a local gitleaks binary when
available, otherwise falls back to Docker if the daemon is running.
USAGE
  exit 0
fi

if command -v gitleaks >/dev/null 2>&1; then
  exec gitleaks detect --source "$repo_root" --redact --verbose "${scan_args[@]}"
fi

if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  exec docker run --rm -v "$repo_root:/repo" zricethezav/gitleaks:latest detect --source=/repo --redact --verbose "${scan_args[@]}"
fi

echo "gitleaks or a running Docker daemon is required for secret scanning." >&2
exit 1
