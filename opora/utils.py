import pbclient
from django.conf import settings


def create_initial_task(url):
    from moonsheep.moonsheep_settings import PYBOSSA_BASE_URL, PYBOSSA_API_KEY
    pbclient.set('endpoint', PYBOSSA_BASE_URL)
    pbclient.set('api_key', PYBOSSA_API_KEY)
    pbclient.create_task(
        project_id=settings.PYBOSSA_PROJECT_ID,
        info={
            'type': 'opora.tasks.FindTableTask',
            'url': url,
        },
        n_answers=1
    )


def create_ready_task():
    create_initial_task('http://sccg.sk/~cernekova/Benesova_Digital%20Image%20Processing%20Lecture%20Objects%20tracking%20&%20motion%20detection.pdf')
