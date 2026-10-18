import logging
from importlib import import_module

import httpx
from django.conf import settings
from django.contrib.auth.signals import user_login_failed
from django.core.cache import cache
from django.dispatch import Signal, receiver

try:
    axes_signals = import_module('axes.signals')
    user_locked_out = getattr(axes_signals, 'user_locked_out')
except Exception:  # noqa: BLE001
    # Allows local tooling to run even when django-axes is not installed.
    user_locked_out = Signal()

security_logger = logging.getLogger('security.events')


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    username = credentials.get('username') if credentials else None
    client_ip = request.META.get('REMOTE_ADDR', '-') if request else '-'

    key = f'security:failed_login:{client_ip}'
    failed_count = cache.get(key, 0) + 1
    cache.set(key, failed_count, timeout=3600)

    security_logger.warning(
        'failed_login_attempt',
        extra={
            'client_ip': client_ip,
            'username': username or '-',
            'lockout_reason': 'invalid_credentials',
        },
    )


@receiver(user_locked_out)
def on_user_locked_out(sender, request, username, ip_address, **kwargs):
    client_ip = ip_address or (request.META.get('REMOTE_ADDR', '-') if request else '-')
    username = username or '-'

    lockout_metric_key = f'security:lockout_count:{client_ip}'
    lockout_count = cache.get(lockout_metric_key, 0) + 1
    cache.set(lockout_metric_key, lockout_count, timeout=24 * 3600)

    suspicious = lockout_count >= settings.SECURITY_SUSPICIOUS_IP_LOCKOUT_THRESHOLD
    reason = 'repeated_lockouts' if suspicious else 'lockout_threshold_reached'

    security_logger.error(
        'user_locked_out',
        extra={
            'client_ip': client_ip,
            'username': username,
            'lockout_reason': reason,
        },
    )

    if suspicious:
        security_logger.error(
            f'suspicious_ip_behavior detected: lockouts={lockout_count}',
            extra={
                'client_ip': client_ip,
                'username': username,
                'lockout_reason': 'suspicious_ip_behavior',
            },
        )

    webhook_url = settings.SECURITY_ALERT_WEBHOOK_URL
    if webhook_url:
        payload = {
            'event': 'user_locked_out',
            'ip_address': client_ip,
            'username': username,
            'lockout_count_24h': lockout_count,
            'reason': reason,
        }
        try:
            httpx.post(webhook_url, json=payload, timeout=3.0)
        except Exception as exc:  # noqa: BLE001
            security_logger.exception(
                f'webhook_alert_failed: {exc}',
                extra={
                    'client_ip': client_ip,
                    'username': username,
                    'lockout_reason': 'webhook_delivery_failure',
                },
            )
