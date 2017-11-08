# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _


class PoliticalParty(models.Model):
    """
    Political party
    """
    name = models.CharField(verbose_name=_('name'), max_length=100)
    legal_id = models.PositiveIntegerField(verbose_name=_('local id'), unique=True) # is it really unique?

    def __str__(self):
        return self.name

    @property
    def moonsheep_tasks(self):
        return {
            'name': {
                'level': 1,
                'widget': 'text'
            },
            'legal_id': {
                'level': 1,
                'widget': 'number'
            }
        }


class Report(models.Model):
    """
    The whole document to transcript
    """
    report_date = models.DateField(verbose_name=_('report date'), null=True, blank=True)
    # Party that is referred in report. This field will be copied to created Transactions
    party = models.ForeignKey(
        to='opora.PoliticalParty', verbose_name=_('related parties'), null=True, blank=True, on_delete=models.PROTECT
    )

    # pages range
    document_page_start = models.PositiveIntegerField(
        verbose_name=_('document first page containing table'), null=True, blank=True
    )
    document_page_end = models.PositiveIntegerField(
        verbose_name=_('document last page containing table'), null=True, blank=True
    )

    finished = models.BooleanField(verbose_name=_('object completely translated'), default=False)

    # transaction_set

    def __str__(self):
        return self.report_date

    @property
    def moonsheep_tasks(self):
        return {
            'report_date': {
                'level': 1,
                'widget': 'date'
            },
            'party': {
                'level': 1,
                'widget': 'Party'
            },
            'document_page_start': {
                'level': 1,
                'widget': 'number'
            },
            'document_page_end': {
                'level': 1,
                'widget': 'number'
            }
        }


class Transaction(models.Model):
    """
    Noted transaction in documents. Filled by volunteers in 3rd stage.
    """
    CASH_CONTRIBUTION, RETURN_LAW_VIOLATION, RETURN_ERROR = range(1, 4)
    TRANSACTION_TYPES = (
        (CASH_CONTRIBUTION, _('cash contribution')),
        (RETURN_LAW_VIOLATION, _('return in law violation')),
        (RETURN_ERROR, _('return in error'))
    )

    POLITICAL_PARTY_ACCOUNT, ELECTION_FUND = range(1, 3)
    MONEY_DESTINATIONS = (
        (POLITICAL_PARTY_ACCOUNT, _('political party account')),
        (ELECTION_FUND, _('election fund'))
    )

    # maybe should be nullable
    transaction_type = models.PositiveIntegerField(verbose_name=_('transaction type'), default=CASH_CONTRIBUTION)
    money_destination = models.PositiveIntegerField(verbose_name=_('money destination'), default=MONEY_DESTINATIONS)

    report = models.ForeignKey(to='opora.Report', verbose_name=_('report'), on_delete=models.PROTECT)

    # ID of transaction from table in document
    local_id = models.PositiveIntegerField(verbose_name=_('our id')) # TODO: is it unique?
    # Page number containing table with transaction in document
    page_number = models.PositiveIntegerField(verbose_name=_('page number containing table with transaction'))
    # Party that transaction concerns. Field copied from the Report.
    party = models.ForeignKey(
        to='opora.PoliticalParty', verbose_name=_('related parties'), null=True, blank=True, on_delete=models.PROTECT
    )

    # Fields to be filled by volunteers
    receipt_date = models.DateField(verbose_name=_('receipt date'), null=True, blank=True)
    # account_type
    # bank_document_id
    payee = models.ForeignKey(
        to='opora.Payee', verbose_name=_('payee name'), null=True, blank=True, on_delete=models.PROTECT
    )
    amount = models.DecimalField(verbose_name=_('amount'), max_digits='12', decimal_places='2')
    total_funds_received = models.DecimalField(
        verbose_name=_('total funds received'), max_digits='12', decimal_places='2'
    )

    def __str__(self):
        if self.local_id:
            return self.local_id
        else:
            return 'no local id, pk: {}'.format(self.pk)

    @property
    def moonsheep_tasks(self):
        return {
            'local_id': {
                'level': 2,
                'widget': 'number'
            },
            'receipt_date': {
                'level': 3,
                'widget': 'date'
            },
            'payee': {
                'level': 3,
                'widget': 'Payee'
            },
            'amount': {
                'level': 3,
                'widget': 'number'
            }
        }


class Payee(models.Model):
    """
    Draft of payee model. Needs to be extended for legal entitees and individuals
    """
    name = models.CharField(verbose_name=_('name'), max_length=100)

    def __str__(self):
        return self.name

    @property
    def moonsheep_tasks(self):
        return {
            'name': {
                'level': 3,
                'widget': 'text'
            }
        }
