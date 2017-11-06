class AbstractTask():
    def get_form(self):
        """
        Returns form for a this task

        Algorithm:
        1. Get actual (implementing) class name, ie. FindTableTask
        2. Try to return if exists 'forms/find_table.html'
        3. Otherwise return `forms/FindTableForm`
        4. Otherwise return error suggesting to implement 2 or 3
        :return: path to the template (string) or Django's Form class
        """
        # TODO
        pass

    def get_presenter(self, task_data):
        """
        Returns presenter based on task data. Default presenter depends on the url MIME Type
        :return:
        """
        task_data['url']
        mimetype = 'pdf' # compute mimetype from url extension

        if "exists moonsheep.presenters.{mimetype}":
            return "moonsheep.presenters.{mimetype}"
        raise "PresenterNotDefined()"

    # TODO think how to serve this data
    def save_verified_data(self, outcome, confidence, verified_data):
        """

        :param outcome: yes/partly
        :param confidence: tolerance
        :param verified_data:
        :return:
        """
        raise NotImplementedError()

    # TODO to implement verify_data let's copy how django forms do it: django.forms.forms.BaseForm#full_clean


class UnorderedSetVerifier:
    def __init__(self, field_name):
        self.field_name = field_name

    def __call__(self, *args, **kwargs):
        # return [1,2,3,4]
        # pass


# # Flow 2. Serve form for a given task  (to implement in Moonsheep Controller)
# task_type = 'find_table'
# task = FindTableTask()
# task.get_form() ->
# task.get_presenter(pybossa.task_data)
#
# # Flow 4. Verify task runs of a given task
# # input
# task_type = 'find_table'
# task_runs = []
# # logic
# task = FindTableTask()
# task.full_verify(task_runs) # it generates cl.verified_data or throws some errors
#     try:
#         verified_data = self.verify() # if it's overriden
#
# task.verified_data # aka self.cleaned_data = {}
# task.save_verified_data() # saves to the model


### MOONSHEEP ABOVE
### OPORA BELOW


class FindTableTask(AbstractTask):
    """
    Choose pages containing crucial tables and get metadata (party, date)
    """
    def save_verified_data(self, outcome, confidence, verified_data):
        # TODO map verified data to models/Report and models/Party
        pass

    def get_presenter(self):
        return presenter.PDFViewer()


class GetTransactionIdsTask(AbstractTask):
    """
    List IDs of transactions on a page X
    """
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
    pass
