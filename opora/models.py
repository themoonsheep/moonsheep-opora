from django.core import validators
from django.db import models
from django.utils.translation import ugettext as _
from moonsheep.registry import document


class PoliticalParty(models.Model):
    """
    Political party
    """
    name = models.CharField(verbose_name=_("name"), max_length=100)
    legal_id = models.PositiveIntegerField(verbose_name=_("local id"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "political parties"


@document(on_import_create=['opora.tasks.FindTableTask'])
class Report(models.Model):
    """
    The whole document to transcript
    """
    # initial data
    url = models.URLField(verbose_name=_("report URL"), unique=True, max_length=2048)
    progress = models.DecimalField(decimal_places=3, max_digits=6, default=0,
                                   validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])

    # TODO in the API return only those reports that have been verified (those with set date)

    # task 1
    # TODO would be good to distinguish required/null on document creation (when we want to create "empty" document vs required one cross-checked (when we want to enforce rules)
    date = models.DateField(verbose_name=_("report date"), null=True)
    # Party that is referred in report. This field will be copied to created Transactions
    party = models.ForeignKey(
        to="opora.PoliticalParty", verbose_name=_("related parties"), on_delete=models.PROTECT, null=True
    )

    finished = models.BooleanField(verbose_name=_("object completely translated"), default=False)

    def __str__(self):
        return f"{self.date}" if self.date else str(self.id)

    class Meta:
        unique_together = ['date', 'party']


class TransactionPages(models.Model):
    POLITICAL_PARTY_ACCOUNT, ELECTION_FUND = range(1, 3)
    MONEY_DESTINATIONS = (
        (POLITICAL_PARTY_ACCOUNT, _('political party account')),
        (ELECTION_FUND, _('election fund'))
    )

    CASH_CONTRIBUTION, RETURN_LAW_VIOLATION, RETURN_ERROR = range(1, 4)
    TRANSACTION_TYPES = (
        (CASH_CONTRIBUTION, _('cash contribution')),
        (RETURN_LAW_VIOLATION, _('return in law violation')),
        (RETURN_ERROR, _('return in error'))
    )

    INDIVIDUAL, LEGAL_ENTITY = range(1, 3)
    LEGAL_IDENTIFICATIONS = (
        (INDIVIDUAL, _('individual')),
        (LEGAL_ENTITY, _('legal entity'))
    )

    # task 1
    report = models.ForeignKey(to="opora.Report", verbose_name=_("report"), on_delete=models.PROTECT)
    # pages range
    page_start = models.PositiveIntegerField(
        verbose_name=_("document first page containing table"), null=True, blank=True
    )
    page_end = models.PositiveIntegerField(
        verbose_name=_("document last page containing table"), null=True, blank=True
    )

    money_destination = models.PositiveIntegerField(
        verbose_name=_('money destination'), choices=MONEY_DESTINATIONS
    )
    transaction_type = models.PositiveIntegerField(
        verbose_name=_('transaction type'), choices=TRANSACTION_TYPES
    )
    legal_identification = models.SmallIntegerField(
        verbose_name=_("legal identification"), choices=LEGAL_IDENTIFICATIONS
    )
    # task 2
    total_funds = models.PositiveIntegerField(verbose_name=_("total funds received"), null=True, blank=True)

    class Meta:
        unique_together = ['report', 'money_destination', 'transaction_type', 'legal_identification']

    def __str__(self):
        return "{0} {1} {2}".format(
            self.get_money_destination_display(),
            self.get_transaction_type_display(),
            self.get_legal_identification_display()
        )

    class Meta:
        verbose_name_plural = "transaction pages"

    @staticmethod
    def iterations():
        import itertools
        return list(itertools.product(
            range(1, 1 + max(TransactionPages.MONEY_DESTINATIONS)[0]),
            range(1, 1 + max(TransactionPages.TRANSACTION_TYPES)[0]),
            range(1, 1 + max(TransactionPages.LEGAL_IDENTIFICATIONS)[0])
        ))


class TransactionBase(models.Model):
    """
    Noted transaction in documents. Filled by volunteers in 3rd stage.
    """
    money_destination = models.PositiveIntegerField(
        verbose_name=_('money destination'), choices=TransactionPages.MONEY_DESTINATIONS
    )
    transaction_type = models.PositiveIntegerField(
        verbose_name=_('transaction type'), choices=TransactionPages.TRANSACTION_TYPES
    )

    # task 2
    bank_document_id = models.CharField(verbose_name=_("bank document ID"), max_length=50, null=True, blank=True)
    # Page number containing table with transaction in document
    page = models.PositiveIntegerField(
        verbose_name=_("page number containing table with transaction"), null=True, blank=True
    )
    report = models.ForeignKey(
        to="opora.Report", verbose_name=_("report"), on_delete=models.PROTECT, null=True, blank=True
    )

    # task 3
    receipt_date = models.DateField(verbose_name=_("receipt date"), null=True, blank=True)
    amount = models.DecimalField(
        verbose_name=_("donation amount"), null=True, blank=True, decimal_places=2, max_digits=10
    )
    payee = models.ForeignKey(
        to="opora.Payee", verbose_name=_("payee"), null=True, blank=True, on_delete=models.PROTECT
    )

    class Meta:
        abstract = True

    @property
    def party(self):
        return self.report.party


class Donation(TransactionBase):
    """

    """
    # task 3
    account_type = models.CharField(verbose_name=_("account type"), max_length=50, null=True, blank=True)

    def __str__(self):
        return "Donation {0}".format(self.pk)


class Return(TransactionBase):
    """

    """
    # task 3
    date = models.DateField(verbose_name=_("return date"), null=True, blank=True)
    document_id = models.CharField(verbose_name=_("return document id"), max_length=50, null=True, blank=True)
    explanation = models.TextField(verbose_name=_("return explanation"), null=True, blank=True)
    amount_to_payee = models.DecimalField(
        verbose_name=_("return amount to payee"), null=True, blank=True, decimal_places=2, max_digits=10
    )
    amount_to_state_budget = models.DecimalField(
        verbose_name=_("return amount to state budget"), null=True, blank=True, decimal_places=2, max_digits=10
    )

    def __str__(self):
        return "Restoration {0}".format(self.pk)


class Payee(models.Model):
    """
    Draft of payee model. Needs to be extended for legal entitees and individuals
    """
    # task 2
    legal_identification = models.SmallIntegerField(
        verbose_name=_("legal identification"), choices=TransactionPages.LEGAL_IDENTIFICATIONS
    )
    # task 3
    name = models.CharField(verbose_name=_("payee name (first name + last name + name of the father)"), max_length=200)
    identification = models.CharField(
        verbose_name=_("payee ID or Passport number"), max_length=100, null=True, blank=True
    )
    address = models.CharField(verbose_name=_("payee Address"), max_length=200)

    def __str__(self):
        return self.name
