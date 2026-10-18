import os
import sys

import django
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

SENSITIVE_KEYWORDS = ['login', 'auth', 'execute', 'submit', 'token', 'admin', 'trigger', 'export']


def extract_sensitive_routes(urlpatterns, base=''):
    sensitive = []
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            path = base + str(pattern.pattern)
            if any(keyword in path.lower() for keyword in SENSITIVE_KEYWORDS):
                sensitive.append(path)
        elif isinstance(pattern, URLResolver):
            sensitive.extend(extract_sensitive_routes(pattern.url_patterns, base + str(pattern.pattern)))
    return sensitive


if __name__ == '__main__':
    resolver = get_resolver()
    routes = sorted(set(extract_sensitive_routes(resolver.url_patterns)))

    print('API discovery completed')
    print(f'Found {len(routes)} potentially sensitive routes:')
    for route in routes:
        print(f' - /{route}')

    print('\nRecommendation: verify axes protection on each sensitive route.')
