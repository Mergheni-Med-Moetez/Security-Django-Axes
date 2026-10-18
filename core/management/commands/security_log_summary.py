import re
from collections import Counter
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


LOG_PATTERN = re.compile(
    r"event=(?P<event>\S+) ip=(?P<ip>\S+) user=(?P<user>\S+) reason=(?P<reason>\S+)"
)


class Command(BaseCommand):
    help = 'Parse security_audit.log and print failed attempts and lockout metrics.'

    def handle(self, *args, **options):
        log_path = Path(settings.BASE_DIR) / 'security_audit.log'
        if not log_path.exists():
            self.stdout.write(self.style.WARNING('security_audit.log not found'))
            return

        failed_by_ip = Counter()
        lockouts_by_ip = Counter()
        reasons = Counter()

        with log_path.open('r', encoding='utf-8') as log_file:
            for line in log_file:
                match = LOG_PATTERN.search(line)
                if not match:
                    continue

                event = match.group('event')
                ip = match.group('ip')
                reason = match.group('reason')

                if 'failed_login_attempt' in line:
                    failed_by_ip[ip] += 1
                if event.endswith('security.events') and 'user_locked_out' in line:
                    lockouts_by_ip[ip] += 1
                reasons[reason] += 1

        self.stdout.write('Top failed login IPs:')
        for ip, count in failed_by_ip.most_common(10):
            self.stdout.write(f'  {ip}: {count}')

        self.stdout.write('Top lockout IPs:')
        for ip, count in lockouts_by_ip.most_common(10):
            self.stdout.write(f'  {ip}: {count}')

        self.stdout.write('Top lockout reasons:')
        for reason, count in reasons.most_common(10):
            self.stdout.write(f'  {reason}: {count}')
