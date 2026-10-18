import os
import sys
from collections import Counter

import django
from django.urls import get_resolver

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

HIGH_RISK_KEYWORDS = ['auth', 'login', 'token', 'execute', 'trigger', 'export']
MEDIUM_RISK_KEYWORDS = ['upload', 'data']
EXCLUDE_KEYWORDS = ['health', 'docs', 'schema', 'admin']


def classify_route(route):
    url = str(route.pattern)
    if any(keyword in url for keyword in EXCLUDE_KEYWORDS):
        return 'NONE'
    if any(keyword in url for keyword in HIGH_RISK_KEYWORDS):
        return 'HIGH'
    if any(keyword in url for keyword in MEDIUM_RISK_KEYWORDS):
        return 'MEDIUM'
    return 'LOW'


def audit_urls(resolver=None, prefix=''):
    resolver = resolver or get_resolver()
    results = []

    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'url_patterns'):
            results.extend(audit_urls(pattern, prefix + str(pattern.pattern)))
        else:
            full_url = '/' + prefix + str(pattern.pattern)
            risk = classify_route(pattern)
            name = getattr(pattern, 'name', 'unnamed')
            results.append((full_url, risk, name))
    return results


if __name__ == '__main__':
    routes = audit_urls()
    print('RISK REGISTRY - Agent-Facing API Endpoints')
    print('-' * 72)
    print(f"{'URL':<44} {'RISK':<8} NAME")
    print('-' * 72)

    for url, risk, name in sorted(routes, key=lambda item: item[1]):
        print(f'{url:<44} {risk:<8} {name}')

    counts = Counter(level for _, level, _ in routes)
    print('\nSummary:')
    for level in ['HIGH', 'MEDIUM', 'LOW', 'NONE']:
        print(f'  {level}: {counts.get(level, 0)} endpoints')
