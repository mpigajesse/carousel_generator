# Security Policy

## Supported Versions

| Version | Support          |
|---------|------------------|
| latest  | Security updates |

---

## Reporting a Vulnerability

If you discover a security vulnerability, **do not open a public issue**.

Contact the maintainer privately:

- **Email:** jesse@africacentred.tech
- **Subject:** `[SECURITY] carousel-generator — <brief description>`

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (optional)

You will receive an acknowledgment within **48 hours** and a resolution timeline within **7 days**.

---

## Security Architecture

### Authentication

- Single secret password (`APP_PASSWORD` env var) — no username
- Constant-time comparison via `secrets.compare_digest()` (prevents timing attacks)
- Flask session with 30-day lifetime
- Session cookies: `HttpOnly`, `SameSite=Lax`, `Secure` in production

### Rate Limiting

- `/login` endpoint: **10 requests/minute**, **30 requests/hour** per IP (flask-limiter)

### Input Validation

| Surface | Protection |
|---------|-----------|
| `?next=` redirect param | Rejects any URL with netloc, scheme, or `//` |
| Job ID / path params | `Path.relative_to()` containment check — path traversal blocked |
| Markdown upload | `secure_filename()` + case-insensitive extension check |
| Markdown content | 500 KB size cap before parsing (YAML bomb protection) |
| File uploads | `MAX_CONTENT_LENGTH = 2 MB` (Flask) |
| Fenced code `lang` attr | Allowlist `[a-zA-Z0-9_\-+#]` — injected into Playwright HTML |
| Markdown hyperlinks | `javascript:`, `data:`, `vbscript:` schemes redirected to `#` |

### Output / XSS Prevention

- Toast messages rendered via `document.createTextNode()` — never `innerHTML`
- `esc()` helper encodes `&`, `"`, `'`, `<`, `>` (safe for attribute and text contexts)
- YAML parsed with `yaml.safe_load()` only

### HTTP Security Headers

Every response includes:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

### Secret Management

- `APP_PASSWORD` and `SECRET_KEY` are loaded exclusively from environment variables (`.env` via python-dotenv)
- `.env` is listed in `.gitignore` — never committed
- If `SECRET_KEY` is unset, a random ephemeral key is generated with a `RuntimeWarning`
- If `APP_PASSWORD` is unset, the app runs in open mode with a `RuntimeWarning`

### Error Handling

- API endpoints return generic error messages to clients
- Full stack traces are written to server logs only (`app.logger.exception`)

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `APP_PASSWORD` | Yes (prod) | Single access password — leave empty to disable auth (dev only) |
| `SECRET_KEY` | Yes (prod) | Flask session signing key — generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `FLASK_DEBUG` | No | Set to `1` to enable debug mode (never in production) |
| `FLASK_ENV` | No | Set to `production` to enable `Secure` cookie flag |

---

## Security Checklist for Deployment

- [ ] `APP_PASSWORD` set to a strong random value
- [ ] `SECRET_KEY` set to a 32-byte random hex string
- [ ] `FLASK_DEBUG` **not** set (or set to `0`)
- [ ] `FLASK_ENV=production` set (enables `Secure` cookie flag)
- [ ] App served behind HTTPS (required for `Secure` cookie flag)
- [ ] `static/generated/` not publicly accessible without auth (serve via `/api/library/` routes)
- [ ] Log output monitored for `RuntimeWarning` at startup

---

## Out of Scope

The following are known limitations and are not considered vulnerabilities:

- **No CSRF protection** on API endpoints — the app is single-user and API calls require session auth
- **In-memory job store** — jobs are lost on server restart by design
- **No multi-user isolation** — the app is designed for private single-user use

---

© 2026 Africa Centred Technology. Tous droits réservés.
