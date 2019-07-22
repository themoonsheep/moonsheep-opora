"""opora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from .tasks import *
from .views import TranscriptionView
from .tasks import *  # Keep it to make Moonsheep aware of defined tasks

from moonsheep.api import AppApi

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^moonsheep/', include('moonsheep.urls')),

    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='home'),
    url(r'^transcription/$', TranscriptionView.as_view(), name='transcription'),
    url(r'^thank-you/$', TemplateView.as_view(template_name='thankyou.html'), name='thank-you'),

    url(r'^api/opora/', AppApi('opora').urls),
    url(r'^api-auth/', include('rest_framework.urls'))
]


# DEV-DEBUG
from django.conf import settings
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

