from django import forms


class FindTableForm(forms.Form):
    party_name = forms.CharField(label="Party name")
    party_legal_id = forms.CharField(label="Party legal ID")
    date = forms.CharField(label="Report date", widget=forms.SelectDateWidget)
    page_start_111 = forms.IntegerField(label="First page number")
    page_end_111 = forms.IntegerField(label="Last page number")
    no_pages_111 = forms.BooleanField(label="No pages")
    page_start_112 = forms.IntegerField(label="First page number")
    page_end_112 = forms.IntegerField(label="Last page number")
    no_pages_112 = forms.BooleanField(label="No pages")
    page_start_113 = forms.IntegerField(label="First page number")
    page_end_113 = forms.IntegerField(label="Last page number")
    no_pages_113 = forms.BooleanField(label="No pages")
    page_start_121 = forms.IntegerField(label="First page number")
    page_end_121 = forms.IntegerField(label="Last page number")
    no_pages_121 = forms.BooleanField(label="No pages")
    page_start_122 = forms.IntegerField(label="First page number")
    page_end_122 = forms.IntegerField(label="Last page number")
    no_pages_122 = forms.BooleanField(label="No pages")
    page_start_123 = forms.IntegerField(label="First page number")
    page_end_123 = forms.IntegerField(label="Last page number")
    no_pages_123 = forms.BooleanField(label="No pages")
    page_start_211 = forms.IntegerField(label="First page number")
    page_end_211 = forms.IntegerField(label="Last page number")
    no_pages_211 = forms.BooleanField(label="No pages")
    page_start_212 = forms.IntegerField(label="First page number")
    page_end_212 = forms.IntegerField(label="Last page number")
    no_pages_212 = forms.BooleanField(label="No pages")
    page_start_213 = forms.IntegerField(label="First page number")
    page_end_213 = forms.IntegerField(label="Last page number")
    no_pages_213 = forms.BooleanField(label="No pages")
    page_start_221 = forms.IntegerField(label="First page number")
    page_end_221 = forms.IntegerField(label="Last page number")
    no_page_221 = forms.BooleanField(label="No pages")
    page_start_222 = forms.IntegerField(label="First page number")
    page_end_222 = forms.IntegerField(label="Last page number")
    no_pages_222 = forms.BooleanField(label="No pages")
    page_start_223 = forms.IntegerField(label="First page number")
    page_end_223 = forms.IntegerField(label="Last page number")
    no_pages_223 = forms.BooleanField(label="No pages")


class GetTransactionIdsForm(forms.Form):
    transaction_ids = forms.CharField(label="Transaction IDs")
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
