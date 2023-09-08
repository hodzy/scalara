from django import forms


class UploadFileForm(forms.Form):
    ersteller = forms.CharField(max_length=50)
    name = forms.CharField(max_length=50)
    other = forms.CharField(max_length=50)
    file = forms.FileField()