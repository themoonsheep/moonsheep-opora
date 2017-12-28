from django import forms

from moonsheep.forms import MultipleRangeField

from .models import TransactionPages


class NewTaskForm(forms.Form):
    url = forms.URLField(label="Report URL")
    # task_class = forms.CharField()


class FindTableForm(forms.Form):
    party_name = forms.CharField(label="Party name")
    party_legal_id = forms.CharField(label="Party legal ID")
    date = forms.CharField(label="Report date", widget=forms.SelectDateWidget)

    def __init__(self, *args, **kwargs):
        super(FindTableForm, self).__init__(*args, **kwargs)
        for md, tt, li in TransactionPages.iterations():
            idx = '{0}{1}{2}'.format(md, tt, li)
            self.fields['no_pages_{0}'.format(idx)] = \
                forms.BooleanField(label="No pages", required=False)
            self.fields['page_start_{0}'.format(idx)] = \
                forms.IntegerField(label="First page number", required=False)
            self.fields['page_end_{0}'.format(idx)] = \
                forms.IntegerField(label="Last page number", required=False)

    def clean(self):
        cleaned_data = super(FindTableForm, self).clean()

        for md, tt, li in TransactionPages.iterations():
            idx = '{0}{1}{2}'.format(md, tt, li)
            page_start = cleaned_data.get("page_start_{0}".format(idx))
            page_end = cleaned_data.get("page_end_{0}".format(idx))
            no_pages = cleaned_data.get("no_pages_{0}".format(idx))
            if bool(page_start and page_end) == bool(no_pages):
                if bool(page_start and page_end):
                    message = "Don't provide no pages and page start and page end for form {0}.".format(idx)
                else:
                    message = "Provide no pages or provide page start and page end for form {0}.".format(idx)
                raise forms.ValidationError(message)
            elif bool(page_start) != bool(page_end):
                if bool(page_start):
                    message = "Provide page end for form {0}.".format(idx)
                else:
                    message = "Provide page start for form {0}.".format(idx)
                raise forms.ValidationError(message)
            if bool(page_start and page_end) and page_end < page_start:
                raise forms.ValidationError("Last page must be greater or equal than first page.")

        return cleaned_data


class GetTransactionIdsForm(forms.Form):
    transaction_ids = MultipleRangeField(label="Transaction IDs")
    total_funds = forms.IntegerField(label="Total received funds")


class GetTransactionForm(forms.Form):
    receipt_date = forms.CharField(label="Receipt date", widget=forms.SelectDateWidget)
    amount = forms.IntegerField(label="Transaction amount")
    # payee
    payee_name = forms.CharField(label="Payee name")
    payee_identification = forms.CharField(label="Payee identification")
    payee_address = forms.CharField(label="Payee address")


class GetDonationForm(GetTransactionForm):
    account_type = forms.CharField(label="Account type")


class GetReturnForm(GetTransactionForm):
    date = forms.CharField(label="Return date", widget=forms.SelectDateWidget)
    document_id = forms.CharField(label="Return document ID")
    explanation = forms.CharField(label="Return explanation")
    amount_to_payee = forms.IntegerField(label="Return amount to payee")
    amount_to_state_budget = forms.IntegerField(label="Return amount to state budget")
