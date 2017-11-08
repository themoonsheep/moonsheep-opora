# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from moonsheep.views import TaskView


class HomeView(TemplateView):
    template_name = 'home.html'


class IntroView(TemplateView):
    template_name = 'intro.html'


class MissionView(TemplateView):
    template_name = 'mission.html'


class TranscriptionView(TaskView):
    pass
