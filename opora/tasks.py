from moonsheep.tasks import AbstractTask
from moonsheep.verifiers import UnorderedSetVerifier

from .forms import FindTableForm, GetTransactionIdsForm, GetTransactionForm


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

    def save_verified_data(self, outcome, confidence, verified_data):
        # TODO map verified data to models/Report and models/Party
        pass

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

    verify_ids_list = UnorderedSetVerifier('ids') # Verifier must need to know on which field to operate


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
