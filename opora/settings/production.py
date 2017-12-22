from .base import *
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = [
    'moonsheep-opora.herokuapp.com',
]

DATABASES = {'default': dj_database_url.config()}

# moonsheep settings
MOONSHEEP_TASK_SOURCE = 'pybossa'

# if pybossa is selected
PYBOSSA_URL = 'https://crowdcrafting.org/api/'
PYBOSSA_PROJECT_ID = 5115
PYBOSSA_API_KEY = os.environ.get('PYBOSSA_API_KEY')

