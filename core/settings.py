"""
Django settings for core project.
"""

import os
from pathlib import Path
from datetime import timedelta
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)3hffs0_)zq5dr39tkf^w1$)jdcb)c8#j(l1pk%om79+-ejvn&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# --- APPLICATION DEFINITION ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes', 
    'rest_framework',
    'agents',               # Mahdi's new app
    'core.apps.CoreConfig', # Mahdi's core config
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'axes.middleware.AxesMiddleware',  # Must be directly after Auth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# --- DATABASE ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- CACHE CONFIGURATION (Sprint 2: Concurrency Support) ---
# We use a dedicated axes_cache to avoid mixing security data with general cache.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    },
    'axes_cache': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'axes-security-gate',
    }
}

# --- PASSWORD VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- SECURITY-BY-DESIGN CONFIGURATION (AXES) ---

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Optimized for high-speed RAM tracking
AXES_HANDLER = 'axes.handlers.cache.AxesCacheHandler'
AXES_CACHE = 'axes_cache'

AXES_LOCKOUT_PARAMETERS = ["username", "ip_address"]
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=10)
AXES_RESET_ON_SUCCESS = True
AXES_ENABLE_ACCESS_FAILURE_LOG = True
AXES_HTTP_RESPONSE_CODE = 403

SECURITY_ALERT_WEBHOOK_URL = os.getenv('SECURITY_ALERT_WEBHOOK_URL', '')
SECURITY_SUSPICIOUS_IP_LOCKOUT_THRESHOLD = int(
    os.getenv('SECURITY_SUSPICIOUS_IP_LOCKOUT_THRESHOLD', '3')
)

# --- ADVANCED LOGGING ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'security_context': {
            '()': 'core.logging_filters.SecurityEventContextFilter',
        },
    },
    'formatters': {
        'security': {
            'format': '[{asctime}] {levelname} event={name} ip={client_ip} user={username} reason={lockout_reason} message="{message}"',
            'style': '{',
        },
    },
    'handlers': {
        'axes_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'security_audit.log',
            'formatter': 'security',
            'filters': ['security_context'],
        },
        'security_console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'security',
            'filters': ['security_context'],
        },
    },
    'loggers': {
        'axes': {
            'handlers': ['axes_file', 'security_console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Disables Axes during automated tests
if 'test' in sys.argv:
    AXES_ENABLED = False