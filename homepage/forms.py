from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    age = forms.IntegerField()
    resume = forms.FileField()
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES)
    education_course_name = forms.CharField(max_length=200, required=False)
    certifications = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    most_recent_job = forms.CharField(max_length=100, required=False)
    linkedin_url = forms.CharField(max_length=200, required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    Applying_For = forms.CharField(max_length=100)
    years_of_experience = forms.IntegerField()
    previous_company = forms.CharField(max_length=200)


    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'password', 'age', 'resume', 'gender', 'education_course_name', 'certifications', 'most_recent_job', 'linkedin_url', 'Applying_For', 'years_of_experience', 'previous_company')

