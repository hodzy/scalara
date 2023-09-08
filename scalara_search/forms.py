from django import forms


class SearchForm(forms.Form):
    file_key = forms.CharField(max_length=50, required=False)
    ersteller = forms.CharField(max_length=50, required=False)
    name = forms.CharField(max_length=50, required=False)
    other = forms.CharField(max_length=50, required=False)