from django import forms
from homepage.forms import UserProfileForm
class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()
    #resume_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'type': 'file'}))