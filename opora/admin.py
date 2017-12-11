from django.contrib import admin

from .models import (
    PoliticalParty, Report, TransactionPages, Donation, Return, Payee
)


@admin.register(PoliticalParty)
class PoliticalPartyAdmin(admin.ModelAdmin):
    list_display = ['name', 'legal_id']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['date', 'party']


@admin.register(TransactionPages)
class TransactionPagesAdmin(admin.ModelAdmin):
    list_display = ['report', 'page_start', 'page_end']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    pass


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    pass


@admin.register(Payee)
class PayeeAdmin(admin.ModelAdmin):
    pass
