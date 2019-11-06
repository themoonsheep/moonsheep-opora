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
    ordering = ['-date'] # TODO index


@admin.register(TransactionPages)
class TransactionPagesAdmin(admin.ModelAdmin):
    list_display = [
        'report', 'page_start', 'page_end',
        'total_funds',
        'money_destination', 'transaction_type', 'legal_identification'
    ]


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = [
        'money_destination', 'transaction_type',
        'bank_document_id', 'page', 'report',
        'receipt_date', 'amount', 'payee', 'account_type'
    ]


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = [
        'money_destination', 'transaction_type',
        'bank_document_id', 'page', 'report',
        'receipt_date', 'amount', 'payee',
        'date', 'document_id', 'explanation',
        'amount_to_payee', 'amount_to_state_budget'
    ]


@admin.register(Payee)
class PayeeAdmin(admin.ModelAdmin):
    pass
