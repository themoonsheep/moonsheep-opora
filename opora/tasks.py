import datetime
import random

from django.shortcuts import get_object_or_404

from moonsheep.tasks import AbstractTask, register_task
from moonsheep.verifiers import *

from .forms import FindTableForm, GetTransactionIdsForm, GetDonationForm, GetReturnForm
from .models import TransactionPages, PoliticalParty, Report, Donation, Return, Payee


@register_task()
class FindTableTask(AbstractTask):
    """
    Choose pages containing crucial tables and get metadata (party, date)
    PyBossa task structure:
    {
        "url": "https://epf.org.pl/pl/wp-content/themes/epf/images/logo-epanstwo.png",
        "party": "",
        "type": "opora.tasks.FindTableTask",
        "page": "",
        "record_id": ""
    }
    """
    template_name = 'tasks/find_table.html'
    task_form = FindTableForm

    def create_mocked_task(self, data):
        data['info'].update({
            'url': 'https://nazk.gov.ua/sites/default/files/docs/2017/3/3_kv/2/Agrarna_partija/3%20%EA%E2%E0%F0%F2%E0%EB%202017%20%D6%C0%20%C0%CF%D3%20%97%20%E7%E0%F2%E5%F0%F2%E8%E9.pdf',
        })

        return data

    def verify_party_name(self, values):
        return values[0], 1

    def save_verified_data(self, verified_data):
        party, created = PoliticalParty.objects.get_or_create(
            name=verified_data['party_name'],
            legal_id=verified_data['party_legal_id']
        )
        report, created = Report.objects.get_or_create(
            date=datetime.datetime.strptime(verified_data['date'], "%Y-%m-%d"),
            party=party,
            url=self.url
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
            date=datetime.datetime.strptime(verified_data['date'], "%Y-%m-%d"),
            party=party
        )
        for tp in TransactionPages.objects.filter(report=report):
            for page in range(tp.page_start, tp.page_end + 1):
                params = {
                    'url': self.url,
                    'page': page,
                    'transaction_type': tp.transaction_type,
                    'money_destination': tp.money_destination,
                    'legal_identification': tp.legal_identification
                }
                self.create_new_task(GetTransactionIdsTask, params)


@register_task()
class GetTransactionIdsTask(AbstractTask):
    """
    List IDs of transactions on a page X
    PyBossa task structure:
    {
        "url": "https://epf.org.pl/pl/wp-content/themes/epf/images/logo-epanstwo.png",
        "party": "1",
        "type": "opora.tasks.GetTransactionIdsTask",
        "page": "1",
        "record_id": ""
    }
    """
    template_name = 'tasks/get_transaction_ids.html'
    task_form = GetTransactionIdsForm

    def create_mocked_task(self, data):
        data['info'].update(random.choice([
            {
                'url': 'https://nazk.gov.ua/sites/default/files/docs/2017/3/3_kv/2/Agrarna_partija/3%20%EA%E2%E0%F0%F2%E0%EB%202017%20%D6%C0%20%C0%CF%D3%20%97%20%E7%E0%F2%E5%F0%F2%E8%E9.pdf',
                'page': 46,
                'money_destination': TransactionPages.POLITICAL_PARTY_ACCOUNT,
                'transaction_type': TransactionPages.CASH_CONTRIBUTION,
                'legal_identification': TransactionPages.INDIVIDUAL,
            },
            {
                'url': 'https://nazk.gov.ua/sites/default/files/docs/2017/3/3_kv/2/Agrarna_partija/3%20%EA%E2%E0%F0%F2%E0%EB%202017%20%D6%C0%20%C0%CF%D3%20%97%20%E7%E0%F2%E5%F0%F2%E8%E9.pdf',
                'page': 74,
                'money_destination': TransactionPages.POLITICAL_PARTY_ACCOUNT,
                'transaction_type': TransactionPages.CASH_CONTRIBUTION,
                'legal_identification': TransactionPages.LEGAL_ENTITY,
            }
        ]))

        return data

    def __init__(self, **kwargs):
        super(GetTransactionIdsTask, self).__init__(**kwargs)
        self.page = kwargs.get('info').get('page')
        self.transaction_type = kwargs.get('info').get('transaction_type')
        self.money_destination = kwargs.get('info').get('money_destination')
        self.legal_identification = kwargs.get('info').get('legal_identification')

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
                    page=self.page,
                    transaction_type=self.transaction_type,
                    money_destination=self.money_destination,
                )
            else:
                Return.objects.get_or_create(
                    report=report,
                    bank_document_id=transaction_id,
                    page=self.page,
                    transaction_type=self.transaction_type,
                    money_destination=self.money_destination
                )

    def after_save(self, verified_data):
        for transaction_id in verified_data['transaction_ids']:
            params = {
                'url': self.url,
                'transaction_id': transaction_id,
                'page': self.page,
                'transaction_type': self.transaction_type,
                'money_destination': self.money_destination,
                'legal_identification': self.legal_identification
            }
            if self.transaction_type == TransactionPages.CASH_CONTRIBUTION:
                self.create_new_task(GetDonationTask, params)
            else:
                self.create_new_task(GetReturnTask, params)


@register_task()
class GetDonationTask(AbstractTask):
    """
    Get donation of transaction idY
    PyBossa task structure:
    {
        "url": "https://epf.org.pl/pl/wp-content/themes/epf/images/logo-epanstwo.png",
        "party": "1",
        "type": "opora.tasks.GetTransactionTask",
        "page": "1",
        "record_id": "1"
    }
    """
    template_name = 'tasks/get_donation.html'
    task_form = GetDonationForm

    def create_mocked_task(self, data):
        data['info'].update(random.choice([
            {
                'url': 'https://nazk.gov.ua/sites/default/files/docs/2017/3/3_kv/2/Agrarna_partija/3%20%EA%E2%E0%F0%F2%E0%EB%202017%20%D6%C0%20%C0%CF%D3%20%97%20%E7%E0%F2%E5%F0%F2%E8%E9.pdf',
                'page': 46,
                'transaction_id': random.choice(['@2PL293649', '@2PL293627', '@2PL270721', '5820345SB', '5820344SB', '5820343SB', '5820342SB', '5820341SB', '5820340SB', '5820339SB', '5820328SB', '5820337SB', '5820336SB']),
                'money_destination': TransactionPages.POLITICAL_PARTY_ACCOUNT,
                'transaction_type': TransactionPages.CASH_CONTRIBUTION,
                'legal_identification': TransactionPages.INDIVIDUAL,
            },
            {
                'url': 'https://nazk.gov.ua/sites/default/files/docs/2017/3/3_kv/2/Agrarna_partija/3%20%EA%E2%E0%F0%F2%E0%EB%202017%20%D6%C0%20%C0%CF%D3%20%97%20%E7%E0%F2%E5%F0%F2%E8%E9.pdf',
                'page': 74,
                'transaction_id': random.choice([353, 20, 203, 257, 754, 12404, 16]),
                'money_destination': TransactionPages.POLITICAL_PARTY_ACCOUNT,
                'transaction_type': TransactionPages.CASH_CONTRIBUTION,
                'legal_identification': TransactionPages.LEGAL_ENTITY,
            }
        ]))

        return data

    def __init__(self, **kwargs):
        super(GetDonationTask, self).__init__(**kwargs)
        self.transaction_id = kwargs.get('info').get('transaction_id')
        self.page = kwargs.get('info').get('page')
        self.transaction_type = kwargs.get('info').get('transaction_type')
        self.money_destination = kwargs.get('info').get('money_destination')
        self.legal_identification = kwargs.get('info').get('legal_identification')

    def save_verified_data(self, verified_data):
        # TODO: finish & test
        payee, created = Payee.objects.get_or_create(
            legal_identification=self.legal_identification,
            name=verified_data['payee_name'],
            identification=verified_data['payee_identification'],
            address=verified_data['payee_address']
        )
        report = Report.objects.get(
            url=self.url
        )
        transaction = Donation.objects.get(
            report=report,
            bank_document_id=self.transaction_id,
            transaction_type=self.transaction_type,
            money_destination=self.money_destination,
            page=self.page,
        )
        transaction.account_type = verified_data['account_type']
        transaction.receipt_date = verified_data['receipt_date']
        transaction.amount = verified_data['amount']
        transaction.payee = payee
        transaction.save()
        report.finished = True
        report.save()


@register_task()
class GetReturnTask(AbstractTask):
    """
    Get donation of transaction idY
    PyBossa task structure:
    {
        "url": "https://epf.org.pl/pl/wp-content/themes/epf/images/logo-epanstwo.png",
        "party": "1",
        "type": "opora.tasks.GetTransactionTask",
        "page": "1",
        "record_id": "1"
    }
    """
    template_name = 'tasks/get_return.html'
    task_form = GetReturnForm

    def __init__(self, **kwargs):
        super(GetReturnTask, self).__init__(**kwargs)
        self.page = kwargs.get('info').get('page')
        self.transaction_id = kwargs.get('info').get('transaction_id')
        self.transaction_type = kwargs.get('info').get('transaction_type')
        self.money_destination = kwargs.get('info').get('money_destination')
        self.legal_identification = kwargs.get('info').get('legal_identification')

    def save_verified_data(self, verified_data):
        # TODO: finish & test
        payee, created = Payee.objects.get_or_create(
            legal_identification=self.legal_identification,
            name=verified_data['payee_name'],
            identification=verified_data['payee_identification'],
            address=verified_data['payee_address']
        )
        report = Report.objects.get(
            url=self.url
        )
        transaction = Return.objects.get(
            report=report,
            bank_document_id=self.transaction_id,
            transaction_type=self.transaction_type,
            money_destination=self.money_destination,
            page=self.page,
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
        report.finished = True
        report.save()
