# -*- coding: utf-8 -*-
from django.urls import reverse

from moonsheep.views import TaskView


class TranscriptionView(TaskView):
    def get_success_url(self):
        return reverse('transcription')
