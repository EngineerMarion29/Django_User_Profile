from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from homepage.models import UserProfile
import os

from adminview.models import Record
from django.contrib.auth.models import User
from datetime import date
from django.utils.timezone import datetime, timedelta
import csv
from django.shortcuts import render
from .forms import UploadCSVForm
from django.db.models import Q


def profile_admin(request):
    if request.method == 'GET':
        emp = request.user
        views = Record.objects.filter(user=emp)
        if views.exists():
            return render(request, 'adminview/profile_admin.html')

        return render(request, 'adminview/profile_admin.html')

from django.db.models import Q
from .models import UserProfile
from .forms import UserProfileForm  # Import your new form

def user_profile_list(request):
    query = request.GET.get('q')
    education_query = request.GET.get('education')
    recent_job_query = request.GET.get('recent_job')
    years_of_experience_query = request.GET.get('years_of_experience')
    previous_company_query = request.GET.get('previous_company')

    profiles = UserProfile.objects.all()

    if query:
        profiles = profiles.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__email__icontains=query) |
            Q(age__icontains=query) |
            Q(gender__icontains=query)
        )

    if education_query:
        profiles = profiles.filter(education_course_name__icontains=education_query)

    if recent_job_query:
        profiles = profiles.filter(most_recent_job__icontains=recent_job_query)

    if years_of_experience_query:
        profiles = profiles.filter(years_of_experience=years_of_experience_query)

    if previous_company_query:
        profiles = profiles.filter(previous_company__icontains=previous_company_query)

    return render(request, 'adminview/user_profile_list.html', {'profiles': profiles})



def delete_user_profiles(request):
    if request.method == 'POST':
        selected_profiles = request.POST.getlist('selected_profiles')
        print(selected_profiles)
        if 'delete_all' in request.POST:
            # Delete all profiles
            UserProfile.objects.all().delete()
        else:
            # Delete selected profiles
            print("It's being deleted")
            UserProfile.objects.filter(id__in=selected_profiles).delete()

    return redirect('admin_view:list')
#--------

def profile_details_def(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    return render(request, 'adminview/profile_details.html', {'profile': profile})
#-------------



def bulk_upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            resume_files = request.FILES.getlist('resume')
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            reader = csv.DictReader(decoded_file.splitlines())
            for row in reader:
                user = User.objects.create(
                    username=row['email'],  # Assuming email will be used as username
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )

                user_profile = UserProfile.objects.create(
                    user=user,
                    age=int(row['age']),
                    gender=row['gender'],
                    education_course_name=row['education_course_name'],
                    certifications=row['certifications'],
                    most_recent_job=row['most_recent_job'],
                    years_of_experience=int(row['years_of_experience']),
                    previous_company=row['previous_company'],
                    Applying_For=row['Applying_For'],
                    linkedin_url=row['linkedin_url'],
                    resume=row['resume']
                )

                resume_file = request.FILES.get('resume')
                if resume_file:
                    resume_file_name = os.path.basename(resume_file.name)
                    user_profile.resume.save(resume_file_name, resume_file)

                # You can perform additional processing or validations here if required
            return render(request, 'adminview/upload_success.html')
    else:
        form = UploadCSVForm()
    return render(request, 'adminview/upload_csv.html', {'form': form})


import csv
from django.http import HttpResponse
from .models import UserProfile

def export_user_profiles_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_profiles.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email Address', 'Age', 'Gender', 'Education Course Name',
                     'Certifications', 'Most Recent Job', 'LinkedIn URL', 'Years of Experience', 'Previous Company',
                     'Resume'])

    user_profiles = UserProfile.objects.all()
    for profile in user_profiles:
        writer.writerow([
            profile.user.first_name,
            profile.user.last_name,
            profile.user.email,
            profile.age,
            profile.get_gender_display(),
            profile.education_course_name,
            profile.certifications,
            profile.most_recent_job,
            profile.linkedin_url,
            profile.years_of_experience,
            profile.previous_company,
            profile.resume.name,
        ])

    return response