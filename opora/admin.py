from django.contrib import admin

from .models import (
    PoliticalParty, Report, Transaction, Payee
)


@admin.register(PoliticalParty)
class PoliticalPartyAdmin(admin.ModelAdmin):
    list_display = ['name', 'legal_id']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_date', 'party', 'document_page_start']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(Payee)
class PayeeAdmin(admin.ModelAdmin):
    pass
