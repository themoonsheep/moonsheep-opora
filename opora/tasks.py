from moonsheep.tasks import AbstractTask
from moonsheep.verifiers import UnorderedSetVerifier


class FindTableTask(AbstractTask):
    """
    Choose pages containing crucial tables and get metadata (party, date)
    """
    template_name = 'find_table.html'

    def save_verified_data(self, outcome, confidence, verified_data):
        # TODO map verified data to models/Report and models/Party
        pass

    def get_presenter(self):
        return None
        # return presenter.PDFViewer()


class GetTransactionIdsTask(AbstractTask):
    """
    List IDs of transactions on a page X
    """
    template_name = 'get_transaction_ids.html'

    def verify_ids_list(self, task_runs):
        # Custom implementation that checks for equality of unordered list
        # task_runs[0]['ids'] == task_runs[x]['ids']

        # return [1,2,3,10]
        pass

    verify_ids_list = UnorderedSetVerifier('ids') # Verifier must need to know on which field to operate


class GetTransactionTask(AbstractTask):
    """
    Get transaction idY
    """
    template_name = 'get_transaction.html'
