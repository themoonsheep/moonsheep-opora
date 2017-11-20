# -*- coding: utf-8 -*-
from django.urls import reverse
from django.views.generic import TemplateView

from moonsheep.views import TaskView


class HomeView(TemplateView):
    template_name = 'home.html'


class IntroView(TemplateView):
    template_name = 'intro.html'


class MissionView(TemplateView):
    template_name = 'mission.html'


class TranscriptionView(TaskView):
    template_name = 'transcription.html'

    def get_success_url(self):
        return reverse('transcription')
