from django import forms


class FindTableForm(forms.Form):
    page = forms.IntegerField(label='Page number')
    report_date = forms.CharField(label='Report date', widget=forms.SelectDateWidget)
    party_name = forms.CharField(label='Party name')
    party_legal_id = forms.CharField(label='Party legal ID')


class GetTransactionIdsForm(forms.Form):
    transaction_ids = forms.CharField(label='Transaction IDs')


class GetTransactionForm(forms.Form):
    transaction_date = forms.DateField(label='Transaction date')
    transaction_value = forms.DecimalField(label='Transaction value')
    transaction_donor = forms.CharField(label='Transaction donor')
