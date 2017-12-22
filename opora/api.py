from rest_framework import generics, status

from .models import (
    Report, PoliticalParty, Return, Donation
)
from .serializers import (
    ReportSerializer, PoliticalPartySerializer, ReturnSerializer, DonationSerializer
)


class ReportMixin(object):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportList(ReportMixin, generics.ListAPIView):
    pass


class ReportDetail(ReportMixin, generics.RetrieveAPIView):
    pass


class PoliticalPartyMixin(object):
    queryset = PoliticalParty.objects.all()
    serializer_class = PoliticalPartySerializer


class PoliticalPartyList(PoliticalPartyMixin, generics.ListAPIView):
    pass


class PoliticalPartyDetail(PoliticalPartyMixin, generics.RetrieveAPIView):
    pass


class ReturnMixin(object):
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer


class ReturnList(ReturnMixin, generics.ListAPIView):
    pass


class ReturnDetail(ReturnMixin, generics.RetrieveAPIView):
    pass


class DonationMixin(object):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer


class DonationList(DonationMixin, generics.ListAPIView):
    pass


class DonationDetail(DonationMixin, generics.RetrieveAPIView):
    pass
