# 3ING Security: Django & Django-Axes Defense Suite

A Security-by-Design Django implementation providing robust brute-force protection, credential stuffing mitigation, rate limiting, and automated security event auditing using **`django-axes`**.

---

## 🛡️ Key Features

- **Brute-Force & Credential Stuffing Defense**:
  - Protected endpoints using `@method_decorator(axes_dispatch)`.
  - Configured lockout parameters: `["username", "ip_address"]`.
  - Configurable failure threshold (default: 5 failed attempts) and cool-off period (10 minutes).
  - Immediate HTTP 403 response on lockout.
- **High-Performance In-Memory Cache Handler**:
  - Uses `axes.handlers.cache.AxesCacheHandler` with dedicated `axes_cache` backend to ensure minimal latency overhead on authentication routes.
- **Security Event Signals & Context-Aware Logging**:
  - Custom `user_login_failed` and `user_locked_out` signal receivers.
  - Tracking of repeated lockout attempts per IP within a 24-hour window.
  - Webhook alerting support (`SECURITY_ALERT_WEBHOOK_URL`) for SIEM/SOC integration.
  - Structured audit trail logging to `security_audit.log` via `SecurityEventContextFilter`.
- **Security Auditing & Attack Simulation Tooling**:
  - `core/audit_routes.py`: Dynamic route risk classification (HIGH, MEDIUM, LOW, NONE).
  - `core/discover_routes.py`: Automated discovery and audit registry for agent-facing endpoints.
  - `core/management/commands/security_log_summary.py`: CLI summary of failed logins, lockouts, and suspicious IPs.
  - `baseline_attack.py`: Sequential attack simulation verifying 401 Unauthorized -> 403 Forbidden transitions.
  - `stress_test.py`: Concurrency and burst attack simulation.
  - `latency_audit.py`: Latency benchmarking comparing protected vs. unprotected endpoints.

---

## 📁 Project Structure

```text
.
├── Pipfile
├── Pipfile.lock
├── manage.py
├── baseline_attack.py          # Sequential brute-force testing script
├── latency_audit.py            # Latency benchmarking suite
├── stress_test.py              # Concurrent brute-force stress tester
├── agents/                     # Agent API endpoints & views
│   ├── apps.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py                # Protected APIViews (AgentLoginView, TokenObtainView, etc.)
└── core/                       # Core Django project configuration
    ├── apps.py
    ├── asgi.py
    ├── audit_routes.py         # URL route risk classification tool
    ├── discover_routes.py      # Route discovery script
    ├── logging_filters.py      # Security log context filter
    ├── security_recovery.py    # Lockout reset helper
    ├── settings.py             # Axes and Django settings
    ├── signals.py              # Security signal listeners & webhook dispatcher
    ├── urls.py
    ├── wsgi.py
    └── management/
        └── commands/
            └── security_log_summary.py   # Audit log analyzer command
```

---

## 🚀 Quickstart

### 1. Prerequisites & Environment Setup

Using `pipenv`:

```bash
pipenv install
pipenv shell
```

Or using standard `pip`:

```bash
pip install django django-axes redis djangorestframework django-redis requests httpx
```

### 2. Apply Migrations

```bash
python manage.py migrate
```

### 3. Start the Server

```bash
python manage.py runserver
```

---

## 🔍 Security Audit & Simulation Commands

### Route Risk Registry
Audit and classify all agent-facing routes by threat level:
```bash
python core/audit_routes.py
```

### Brute-Force Baseline Simulation
Simulate sequential brute-force attempts and verify axes lockout enforcement:
```bash
python baseline_attack.py
```

### Concurrency Stress Test
Test resilience under concurrent attack traffic:
```bash
python stress_test.py
```

### Latency Benchmark
Measure overhead added by the security middleware:
```bash
python latency_audit.py
```

### Security Log Summary
Inspect security events recorded in the audit log:
```bash
python manage.py security_log_summary
```

---

## ⚙️ Configuration Reference

Key axes settings in [core/settings.py](core/settings.py):

| Setting | Value | Description |
|---|---|---|
| `AXES_HANDLER` | `axes.handlers.cache.AxesCacheHandler` | In-memory RAM cache tracking |
| `AXES_CACHE` | `'axes_cache'` | Dedicated cache partition |
| `AXES_LOCKOUT_PARAMETERS` | `["username", "ip_address"]` | Composite lockout identifier |
| `AXES_FAILURE_LIMIT` | `5` | Maximum failed attempts before lockout |
| `AXES_COOLOFF_TIME` | `10 minutes` | Duration of lockout |
| `AXES_RESET_ON_SUCCESS` | `True` | Resets failure counter upon valid login |
| `AXES_HTTP_RESPONSE_CODE` | `403` | Status code returned on lockout |
