from .base import *

DEBUG = True

SECRET_KEY = 'whateva'

# moonsheep settings
MOONSHEEP_TASK_SOURCE = 'pybossa'

# if pybossa is selected
# PYBOSSA_URL = 'https://crowdcrafting.org/'
# PYBOSSA_PROJECT_ID = 5115
PYBOSSA_API_KEY = os.environ.get('PYBOSSA_API_KEY')

INSTALLED_APPS += ['django_extensions']

# MOONSHEEP_TASK_SOURCE = 'random'
# MOONSHEEP_DEVELOPMENT_MODE = True
