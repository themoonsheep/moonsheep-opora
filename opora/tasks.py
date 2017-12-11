import datetime

from moonsheep.tasks import AbstractTask
from moonsheep.verifiers import *

from .forms import FindTableForm, GetTransactionIdsForm, GetDonationForm, GetReturnForm
from .models import PoliticalParty, Report, TransactionBase, Donation, Return, Payee


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
    task_template = 'tasks/find_table.html'
    task_form = FindTableForm

    verify_page = EqualsVerifier

    def verify_party_name(self, values):
        return values[0], 1

    def save_verified_data(self, verified_data):
        pass
        # party, created = PoliticalParty.objects.get_or_create(
        #     name=verified_data['party_name'],
        #     legal_id=verified_data['party_legal_id']
        # )
        # Report.objects.get_or_create(
        #     date=datetime.datetime.strptime(verified_data['date'], "%Y-%m-%d"),
        #     party=party,
        #     page_start=verified_data['page_start'],
        #     page_end=verified_data['page_end']
        # )

    def after_save(self, verified_data):
        pass
        # start = verified_data['page_start']
        # end = verified_data['page_end']
        # for page in range(start, end + 1):
        #     params = {
        #         'url': self.url,
        #         'page': page,
        #         'transaction_type': self.transaction_type,
        #         'money_destination': self.money_destination,
        #         'legal_identification': self.legal_identification
        #     }
        #     self.create_new_task(GetTransactionIdsTask, params)

    # # def get_presenter(self):
    #     # return None
    #     return presenter.PDFViewer()


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
    task_template = 'tasks/get_transaction_ids.html'
    task_form = GetTransactionIdsForm

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
        for transaction_id in verified_data['transaction_ids'].split(','):
            if self.transaction_type == TransactionBase.CASH_CONTRIBUTION:
                Donation.objects.get_or_create(
                    bank_document_id=transaction_id,
                    page=self.page
                )
            else:
                Return.objects.get_or_create(
                    bank_document_id=transaction_id,
                    page=self.page
                )

    def after_save(self, verified_data):
        for transaction_id in verified_data['transaction_ids'].split(','):
            params = {
                'url': self.url,
                'transaction_id': transaction_id,
                'page': self.page,
                'transaction_type': self.transaction_type,
                'money_destination': self.money_destination,
                'legal_identification': self.legal_identification
            }
            if self.transaction_type == TransactionBase.CASH_CONTRIBUTION:
                self.create_new_task(GetDonationTask, params)
            else:
                self.create_new_task(GetReturnTask, params)


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
    task_template = 'tasks/get_donation.html'
    task_form = GetDonationForm

    def __init__(self, **kwargs):
        super(GetDonationTask, self).__init__(**kwargs)
        self.transaction_id = kwargs.get('info').get('transaction_id')
        self.page = kwargs.get('info').get('page')
        self.transaction_type = kwargs.get('info').get('transaction_type')
        self.money_destination = kwargs.get('info').get('money_destination')
        self.legal_identification = kwargs.get('info').get('legal_identification')

    def save_verified_data(self, verified_data):
        # TODO: finish & test
        payee = Payee.objects.get_or_create(
            name=verified_data['payee_name'],
            identification=verified_data['payee_identification'],
            address=verified_data['payee_address']
        )
        transaction = Donation.objects.get(pk=self.transaction_id)
        transaction.account_type = verified_data['account_type']
        transaction = Donation.objects.get(pk=self.transaction_id)
        transaction.account_type = verified_data['account_type']
        transaction.receipt_date = verified_data['receipt_date']
        transaction.amount = verified_data['amount']
        transaction.payee = payee
        transaction.save()
        transaction.report.finished = True
        transaction.report.save()


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
    task_template = 'tasks/get_return.html'
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
        payee = Payee.objects.get_or_create(
            name=verified_data['payee_name'],
            identification=verified_data['payee_identification'],
            address=verified_data['payee_address']
        )
        transaction = Return.objects.get(pk=self.transaction_id)
        transaction.date = verified_data['date']
        transaction.document_id = verified_data['document_id']
        transaction.explanation = verified_data['explanation']
        transaction.amount_to_payee = verified_data['amount_to_payee']
        transaction.amount_to_state_budget = verified_data['amount_to_state_budget']
        transaction.receipt_date = verified_data['receipt_date']
        transaction.amount = verified_data['amount']
        transaction.payee = payee
        transaction.save()
        transaction.report.finished = True
        transaction.report.save()
