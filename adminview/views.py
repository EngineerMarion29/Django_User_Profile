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


#def user_profile_list(request):
#    if request.method == 'GET':
#        profiles = UserProfile.objects.all()
#        return render(request, 'adminview/user_profile_list.html', {'profiles': profiles})


def user_profile_list(request):
    query = request.GET.get('q')
    profiles = UserProfile.objects.all()
    if query:
        profiles = profiles.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email_address__icontains=query) |
            Q(age__icontains=query) |
            Q(position__icontains=query) |
            Q(years_of_experience__icontains=query) |
            Q(previous_company__icontains=query) |
            Q(gender__icontains=query)
        )
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
                UserProfile.objects.create(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email_address=row['email_address'],
                    age=int(row['age']),
                    position=row['position'],
                    years_of_experience=int(row['years_of_experience']),
                    previous_company=row['previous_company'],
                    resume=row['resume'],
                    gender=row['gender']
                )

                # Prompt for resume file upload
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
    writer.writerow(['First Name', 'Last Name', 'Email Address', 'Age', 'Position', 'Years of Experience',
                     'Previous Company', 'Resume', 'Gender'])

    user_profiles = UserProfile.objects.all()
    for profile in user_profiles:
        writer.writerow([profile.first_name, profile.last_name, profile.email_address, profile.age,
                         profile.position, profile.years_of_experience, profile.previous_company,
                         profile.resume.name, profile.gender])

    return response