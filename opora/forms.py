from django import forms


class FindTableForm(forms.Form):
    # Find report date
    # Find party name
    # Find party legal ID
    page = forms.IntegerField(label='Page number')


class GetTransactionIdsForm(forms.Form):
    pass


class GetTransactionForm(forms.Form):
    pass
