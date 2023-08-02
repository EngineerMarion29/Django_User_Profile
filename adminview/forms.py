from django import forms

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()
    #resume_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'type': 'file'}))