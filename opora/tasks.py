import datetime
import random

from django.shortcuts import get_object_or_404
from django.utils.decorators import classproperty
from django.contrib.staticfiles.templatetags.staticfiles import static

from moonsheep.tasks import AbstractTask, register_task
from moonsheep.verifiers import *

from .forms import FindTableForm, GetTransactionIdsForm, GetDonationForm, GetReturnForm
from .models import TransactionPages, PoliticalParty, Report, Donation, Return, Payee

EXAMPLE_URL = static('examples/3кв_PDF_.pdf')


@register_task()
class FindTableTask(AbstractTask):
    """
    Choose pages containing crucial tables and get metadata (party, date)
    """
    template_name = 'tasks/find_table.html'
    task_form = FindTableForm

    @classproperty
    def mocked_params(self) -> dict:
        return {
            'url': EXAMPLE_URL,
        }

    def verify_party_name(self, values):
        return values[0], 1

    def save_verified_data(self, verified_data):
        party, created = PoliticalParty.objects.get_or_create(
            name=verified_data['party_name'],
            legal_id=verified_data['party_legal_id']
        )
        report, created = Report.objects.get_or_create(
            date=verified_data['date'],
            party=party,
            url=self.params['url']
        )
        for md, tt, li in TransactionPages.iterations():
            idx = "{0}{1}{2}".format(md, tt, li)
            if not verified_data['no_pages_{0}'.format(idx)]:
                TransactionPages(
                    report=report,
                    page_start=verified_data['page_start_{0}'.format(idx)],
                    page_end=verified_data['page_end_{0}'.format(idx)],
                    total_funds=verified_data['total_funds_{0}'.format(idx)],
                    money_destination=md,
                    transaction_type=tt,
                    legal_identification=li
                ).save()

    def after_save(self, verified_data):
        party = PoliticalParty.objects.get( # TODO optimize , do it in save_verified_data, do we need to separate this function?
            name=verified_data['party_name'],
            legal_id=verified_data['party_legal_id']
        )
        report = Report.objects.get(
            date=verified_data['date'],
            party=party
        )
        for tp in TransactionPages.objects.filter(report=report):
            for page in range(tp.page_start, tp.page_end + 1):
                params = {
                    'url': self.params['url'],
                    'page': page,
                    'transaction_type': tp.transaction_type,
                    'money_destination': tp.money_destination,
                    'legal_identification': tp.legal_identification
                }
                GetTransactionIdsTask.create(params)


@register_task()
class GetTransactionIdsTask(AbstractTask):
    """
    List IDs of transactions on a page X
    """
    template_name = 'tasks/get_transaction_ids.html'
    task_form = GetTransactionIdsForm

    @classproperty
    def mocked_params(cls) -> dict:
        return random.choice([
            {
                'url': EXAMPLE_URL,
                'page': 46,
                'money_destination': TransactionPages.POLITICAL_PARTY_ACCOUNT,
                'transaction_type': TransactionPages.CASH_CONTRIBUTION,
                'legal_identification': TransactionPages.INDIVIDUAL,
            },
            {
                'url': EXAMPLE_URL,
                'page': 74,
                'money_destination': TransactionPages.POLITICAL_PARTY_ACCOUNT,
                'transaction_type': TransactionPages.CASH_CONTRIBUTION,
                'legal_identification': TransactionPages.LEGAL_ENTITY,
            }
        ])

    def verify_ids_list(self, task_runs):
        # Custom implementation that checks for equality of unordered list
        # task_runs[0]['ids'] == task_runs[x]['ids']

        # return [1,2,3,10]
        return task_runs, 1

    # verify_ids_list = UnorderedSetVerifier('ids')  # Verifier must need to know on which field to operate

    def save_verified_data(self, verified_data):
        report = get_object_or_404(Report, url=self.url)
        for transaction_id in verified_data['transaction_ids']:
            if self.transaction_type == TransactionPages.CASH_CONTRIBUTION:
                Donation.objects.get_or_create(
                    report=report,
                    bank_document_id=transaction_id,
                    page=self.params['page'],
                    transaction_type=self.params['transaction_type'],
                    money_destination=self.params['money_destination'],
                )
            else:
                Return.objects.get_or_create(
                    report=report,
                    bank_document_id=transaction_id,
                    page=self.params['page'],
                    transaction_type=self.params['transaction_type'],
                    money_destination=self.params['money_destination']
                )

    def after_save(self, verified_data):
        for transaction_id in verified_data['transaction_ids']:
            params = {
                'url': self.params['url'],
                'transaction_id': transaction_id,
                'page': self.params['page'],
                'transaction_type': self.params['transaction_type'],
                'money_destination': self.params['money_destination'],
                'legal_identification': self.params['legal_identification']
            }
            if self.transaction_type == TransactionPages.CASH_CONTRIBUTION:
                GetDonationTask.create(params)
            else:
                GetReturnTask.create(params)


@register_task()
class GetDonationTask(AbstractTask):
    """
    Transcribe donation information of a given transaction id
    """
    template_name = 'tasks/get_donation.html'
    task_form = GetDonationForm

    @classproperty
    def mocked_params(self) -> dict:
        return random.choice([
            {
                'url': EXAMPLE_URL,
                'page': 46,
                'transaction_id': random.choice(['@2PL293649', '@2PL293627', '@2PL270721', '5820345SB', '5820344SB', '5820343SB', '5820342SB', '5820341SB', '5820340SB', '5820339SB', '5820328SB', '5820337SB', '5820336SB']),
                'money_destination': TransactionPages.POLITICAL_PARTY_ACCOUNT,
                'transaction_type': TransactionPages.CASH_CONTRIBUTION,
                'legal_identification': TransactionPages.INDIVIDUAL,
            },
            {
                'url': EXAMPLE_URL,
                'page': 74,
                'transaction_id': random.choice([353, 20, 203, 257, 754, 12404, 16]),
                'money_destination': TransactionPages.POLITICAL_PARTY_ACCOUNT,
                'transaction_type': TransactionPages.CASH_CONTRIBUTION,
                'legal_identification': TransactionPages.LEGAL_ENTITY,
            }
        ])

    def save_verified_data(self, verified_data):
        # TODO: finish & test
        payee, created = Payee.objects.get_or_create(
            legal_identification=self.params['legal_identification'],
            name=verified_data['payee_name'],
            identification=verified_data['payee_identification'],
            address=verified_data['payee_address']
        )
        report = Report.objects.get(
            url=self.url
        )
        transaction = Donation.objects.get(
            report=report,
            bank_document_id=self.params['transaction_id'],
            transaction_type=self.params['transaction_type'],
            money_destination=self.params['money_destination'],
            page=self.params['page'],
        )
        transaction.account_type = verified_data['account_type']
        transaction.receipt_date = verified_data['receipt_date']
        transaction.amount = verified_data['amount']
        transaction.payee = payee
        transaction.save()

        # If there are no more TransactionTasks then this report should be considered as complete
        # TODO but do we want to flag it here? and check every time? why bother?
        # if deleted, delete the field as well
        # report.finished = True
        # report.save()


@register_task()
class GetReturnTask(AbstractTask):
    """
    Get donation of transaction idY
    """
    template_name = 'tasks/get_return.html'
    task_form = GetReturnForm

    @classproperty
    def mocked_params(self) -> dict:
        return {
            'url': EXAMPLE_URL,
            'page': 46,
            'transaction_id': random.choice(
                ['@2PL293649', '@2PL293627', '@2PL270721', '5820345SB', '5820344SB', '5820343SB', '5820342SB',
                 '5820341SB', '5820340SB', '5820339SB', '5820328SB', '5820337SB', '5820336SB']),
            'money_destination': TransactionPages.POLITICAL_PARTY_ACCOUNT,
            'transaction_type': TransactionPages.RETURN_LAW_VIOLATION,
            'legal_identification': TransactionPages.INDIVIDUAL,
        }

    def save_verified_data(self, verified_data):
        # TODO: finish & test
        payee, created = Payee.objects.get_or_create(
            legal_identification=self.params['legal_identification'],
            name=verified_data['payee_name'],
            identification=verified_data['payee_identification'],
            address=verified_data['payee_address']
        )
        report = Report.objects.get(
            url=self.params['url']
        )
        transaction = Return.objects.get(
            report=report,
            bank_document_id=self.params['transaction_id'],
            transaction_type=self.params['transaction_type'],
            money_destination=self.params['money_destination'],
            page=self.params['page'],
        )
        transaction.date = verified_data['date']
        transaction.document_id = verified_data['document_id']
        transaction.explanation = verified_data['explanation']
        transaction.amount_to_payee = verified_data['amount_to_payee']
        transaction.amount_to_state_budget = verified_data['amount_to_state_budget']
        transaction.receipt_date = verified_data['receipt_date']
        transaction.amount = verified_data['amount']
        transaction.payee = payee
        transaction.save()

        # If there are no more TransactionTasks then this report should be considered as complete
        # TODO but do we want to flag it here? and check every time? why bother?
        # if deleted, delete the field as well
        # report.finished = True
        # report.save()
