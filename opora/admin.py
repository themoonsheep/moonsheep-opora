from django.contrib import admin

from .models import (
    PoliticalParty, Report, Transaction, Payee
)


@admin.register(PoliticalParty)
class PoliticalPartyAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(Payee)
class PayeeAdmin(admin.ModelAdmin):
    pass
