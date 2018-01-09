from django import forms

from moonsheep.forms import MultipleRangeField

from .models import TransactionPages


class FindTableForm(forms.Form):
    party_name = forms.CharField(label="Party name")
    party_legal_id = forms.CharField(label="Party legal ID")
    date = forms.CharField(label="Report date", widget=forms.SelectDateWidget)

    class Meta:
        localized_fields = '__all__'

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
            self.fields['total_funds_{0}'.format(idx)] = \
                forms.CharField(label="Total received funds", required=False)

    def clean(self):
        cleaned_data = super(FindTableForm, self).clean()

        for md, tt, li in TransactionPages.iterations():
            idx = '{0}{1}{2}'.format(md, tt, li)
            page_start = cleaned_data.get("page_start_{0}".format(idx))
            page_end = cleaned_data.get("page_end_{0}".format(idx))
            total_funds = cleaned_data.get("total_funds_{0}".format(idx))
            no_pages = cleaned_data.get("no_pages_{0}".format(idx))
            if bool(page_start and page_end and total_funds) == bool(no_pages):
                if bool(page_start and page_end and total_funds):
                    message = \
                        "Don't provide no pages and page start, page end and total funds for form {0}.".format(idx)
                else:
                    message = \
                        "Provide no pages or provide page start, page end and total funds for form {0}.".format(idx)
                raise forms.ValidationError(message)
            elif bool(page_start) != bool(page_end) or bool(page_start) != bool(total_funds):
                if not bool(page_start):
                    message = "Provide page start for form {0}.".format(idx)
                elif not bool(page_end):
                    message = "Provide page end for form {0}.".format(idx)
                elif not bool(total_funds):
                    message = "Provide total funds for form {0}.".format(idx)
                raise forms.ValidationError(message)
            if bool(page_start and page_end) and page_end < page_start:
                raise forms.ValidationError("Last page must be greater or equal than first page.")

        return cleaned_data


class GetTransactionIdsForm(forms.Form):
    transaction_ids = MultipleRangeField(label="Transaction IDs")

    class Meta:
        localized_fields = '__all__'


class GetTransactionForm(forms.Form):
    receipt_date = forms.CharField(label="Receipt date", widget=forms.SelectDateWidget)
    amount = forms.CharField(label="Transaction amount")
    # payee
    payee_name = forms.CharField(label="Payee name")
    payee_identification = forms.CharField(label="Payee identification", required=False)
    payee_address = forms.CharField(label="Payee address")

    class Meta:
        localized_fields = '__all__'


class GetDonationForm(GetTransactionForm):
    account_type = forms.CharField(label="Account type")

    class Meta:
        localized_fields = '__all__'


class GetReturnForm(GetTransactionForm):
    date = forms.CharField(label="Return date", widget=forms.SelectDateWidget)
    document_id = forms.CharField(label="Return document ID")
    explanation = forms.CharField(label="Return explanation")
    amount_to_payee = forms.CharField(label="Return amount to payee")
    amount_to_state_budget = forms.CharField(label="Return amount to state budget")

    class Meta:
        localized_fields = '__all__'
