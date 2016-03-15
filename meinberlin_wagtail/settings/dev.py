from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gy$z^$s1k*u=okx%5kqx*lg-u$l*yp6()pq(=yi(a)5bs35e30'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADHOCRACY_URL = 'http://arrow'

try:
    from .local import *
except ImportError:
    pass
