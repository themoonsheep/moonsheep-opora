# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import reverse
from django.views.generic import FormView

from moonsheep.views import TaskView

from .forms import NewTaskForm
from .models import Report


class TranscriptionView(TaskView):
    def get_success_url(self):
        return reverse('transcription')


class NewTaskFormView(FormView):
    template_name = 'new-task.html'
    form_class = NewTaskForm

    def get_success_url(self):
        return reverse('new-task')

    def form_valid(self, form):
        import pbclient
        from moonsheep.moonsheep_settings import PYBOSSA_BASE_URL, PYBOSSA_API_KEY
        pbclient.set('endpoint', PYBOSSA_BASE_URL)
        pbclient.set('api_key', PYBOSSA_API_KEY)
        pbclient.create_task(
            project_id=settings.PYBOSSA_PROJECT_ID,
            info={
                # 'type': form.cleaned_data.get('task_class'),
                'type': 'opora.tasks.FindTableTask',
                'url': form.cleaned_data.get('url'),
            },
            n_answers=1
        )
        return super(NewTaskFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NewTaskFormView, self).get_context_data(**kwargs)
        context['reports'] = Report.objects.all()
        return context
