from django import forms

class FindTableForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

    def clean(self):
        # TODO