"""
Default settings for testing
USED BY TRAVIS
"""
import sys

from .base import *  # @UnusedWildImport # NOQA

DEBUG = False

SECRET_KEY = 'BLAH BLAH BLAH'

# Show all console output
LOGGING['handlers']['console']['level'] = 'INFO'
LOGGING['loggers']['eggplant']['level'] = 'INFO'

# Use SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.sqlite',
    }
}

SITE_ID = 1
DOMAIN = 'localhost'
DEFAULT_HTTP_PROTOCOL = 'http'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'username'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[Eggplant]'
EMAIL_TIMEOUT = 5
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'info@localhost'
SERVER_EMAIL = 'django@localhost'

ADMINS = ()

os.environ['RECAPTCHA_TESTING'] = 'True'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--verbosity=2',
    '--stop',
    '--with-yanc',
    # '--cover-branches',
    # '--with-coverage',
    # '--cover-erase',
    # '--cover-package=eggplant',
    'eggplant',
]

for arg in sys.argv:
    if arg.startswith('--tests='):
        NOSE_ARGS = [
            '--verbosity=2',
            '--stop',
            '--with-yanc',
        ]
        break
