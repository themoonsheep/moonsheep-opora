import pbclient
from django.conf import settings


def create_initial_task(url):
    from moonsheep.settings import PYBOSSA_BASE_URL, PYBOSSA_API_KEY
    pbclient.set('endpoint', PYBOSSA_BASE_URL)
    pbclient.set('api_key', PYBOSSA_API_KEY)
    return pbclient.create_task(
        project_id=settings.PYBOSSA_PROJECT_ID,
        info={
            'type': 'opora.tasks.FindTableTask',
            'url': url,
        },
        n_answers=1
    )


def create_ready_task():
    create_initial_task('http://gahp.net/wp-content/uploads/2017/09/sample.pdf')
