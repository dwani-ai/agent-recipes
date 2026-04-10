#!/bin/sh
set -e
# Generate /etc/nginx/adk-auth.conf before nginx loads main config.
# For production on a public GCP VM, set BASIC_AUTH_PASSWORD (and BASIC_AUTH_USER).

AUTH_USER="${BASIC_AUTH_USER:-adk}"
AUTH_FILE="/etc/nginx/adk-auth.conf"
HTPASSWD="/etc/nginx/.htpasswd"

if [ -n "${BASIC_AUTH_PASSWORD:-}" ]; then
  if ! command -v openssl >/dev/null 2>&1; then
    echo "adk-auth: openssl not found; install openssl in the nginx image." >&2
    exit 1
  fi
  HASH="$(openssl passwd -apr1 "$BASIC_AUTH_PASSWORD")"
  printf '%s:%s\n' "$AUTH_USER" "$HASH" > "$HTPASSWD"
  chmod 600 "$HTPASSWD" 2>/dev/null || true
  {
    printf '%s\n' 'auth_basic "ADK Web";'
    printf '%s\n' "auth_basic_user_file $HTPASSWD;"
  } > "$AUTH_FILE"
  echo "adk-auth: HTTP Basic Auth enabled for user '$AUTH_USER'."
elif [ "${ALLOW_UNAUTHENTICATED_ACCESS:-}" = "true" ]; then
  printf '%s\n' 'auth_basic off;' > "$AUTH_FILE"
  echo "adk-auth: WARNING — no BASIC_AUTH_PASSWORD; ALLOW_UNAUTHENTICATED_ACCESS=true (not for public internet)." >&2
else
  echo "adk-auth: Set BASIC_AUTH_PASSWORD (and optionally BASIC_AUTH_USER) for a public deployment." >&2
  echo "adk-auth: For local testing only, set ALLOW_UNAUTHENTICATED_ACCESS=true" >&2
  exit 1
fi
