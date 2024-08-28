# settings/__init__.py

import os

ENVIRONMENT = os.getenv('DJANGO_ENV', 'local')

if ENVIRONMENT == 'production':
    from .pro import *
else:
    from .local import *
