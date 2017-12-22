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
from django.views.generic import TemplateView

from .api import (
    ReportList, ReportDetail, PoliticalPartyList, PoliticalPartyDetail,
    ReturnList, ReturnDetail, DonationList, DonationDetail
)
from .tasks import *
from .views import TranscriptionView


api_urlpatterns = [
    url(r'^report/$', ReportList.as_view(), name='report-list'),
    url(r'^report/(?P<pk>\d+)/$', ReportDetail.as_view(), name='report-detail'),
    url(r'^political-party/$', PoliticalPartyList.as_view(), name='political-party-list'),
    url(r'^political-party/(?P<pk>\d+)/$', PoliticalPartyDetail.as_view(), name='political-party-detail'),
    url(r'^return/$', ReturnList.as_view(), name='return-list'),
    url(r'^return/(?P<pk>\d+)/$', ReturnDetail.as_view(), name='return-detail'),
    url(r'^donation/$', DonationList.as_view(), name='donation-list'),
    url(r'^donation/(?P<pk>\d+)/$', DonationDetail.as_view(), name='donation-detail'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^moonsheep/', include('moonsheep.urls')),

    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='home'),
    url(r'^api/', include(api_urlpatterns)),
    url(r'^transcription/$', TranscriptionView.as_view(), name='transcription'),
    url(r'^thank-you/$', TemplateView.as_view(template_name='thankyou.html'), name='thank-you'),
]
