import datetime

from moonsheep.tasks import AbstractTask
from moonsheep.verifiers import *

from .forms import FindTableForm, GetTransactionIdsForm, GetTransactionForm
from .models import PoliticalParty, Report, Transaction, Payee


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
        party, created = PoliticalParty.objects.get_or_create(
            name=verified_data['party_name'],
            legal_id=verified_data['party_legal_id']
        )
        Report.objects.get_or_create(
            report_date=datetime.datetime.strptime(verified_data['report_date'], "%Y-%m-%d"),
            party=party,
            document_page_start=verified_data['page']
        )

    def after_save(self, verified_data):
        self.create_new_task(GetTransactionTask, **verified_data)

    def get_presenter(self):
        return None
        # return presenter.PDFViewer()


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

    def verify_ids_list(self, task_runs):
        # Custom implementation that checks for equality of unordered list
        # task_runs[0]['ids'] == task_runs[x]['ids']

        # return [1,2,3,10]
        pass

    verify_ids_list = UnorderedSetVerifier('ids')  # Verifier must need to know on which field to operate

    # def save_verified_data(self, verified_data):
    #     # TODO: finish & test
    #     for transaction_id in verified_data['transaction_ids']:
    #         Transaction.objects.get_or_create(
    #             local_id=transaction_id
    #         )


class GetTransactionTask(AbstractTask):
    """
    Get transaction idY
    PyBossa task structure:
    {
        "url": "https://epf.org.pl/pl/wp-content/themes/epf/images/logo-epanstwo.png",
        "party": "1",
        "type": "opora.tasks.GetTransactionTask",
        "page": "1",
        "record_id": "1"
    }
    """
    task_template = 'tasks/get_transaction.html'
    task_form = GetTransactionForm

    # def save_verified_data(self, verified_data):
    #     # TODO: finish & test
    #     transaction = Transaction.objects.get(pk=1)
    #     transaction.receipt_date = verified_data['transaction_date']
    #     transaction.amount = verified_data['transaction_value']
    #     transaction.payee = verified_data['transaction_donor']
    #     transaction.save()

