from .base import *
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = [
#    'moonsheep-opora.herokuapp.com',
    '*'
]

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'set it'

DATABASES = {'default': dj_database_url.config()}

# moonsheep settings
MOONSHEEP_DEVELOPMENT_MODE = True # TODO
