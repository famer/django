from .base import *

DEBUG = True

DATABASES['default']['HOST'] = 'localhost'

# email settings

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'your-email@example.com'