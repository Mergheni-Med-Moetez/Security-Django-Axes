import logging


class SecurityEventContextFilter(logging.Filter):
    """Ensure security formatter fields always exist on log records."""

    def filter(self, record):
        record.client_ip = getattr(record, 'client_ip', '-')
        record.username = getattr(record, 'username', '-')
        record.lockout_reason = getattr(record, 'lockout_reason', '-')
        return True
