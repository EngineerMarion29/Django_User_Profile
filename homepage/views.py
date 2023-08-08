from django.shortcuts import render, redirect
from homepage.forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User

from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


@login_required
@user_passes_test(lambda user: user.is_superuser)
def reg_user(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = User.objects.create_user(
                username=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user_profile = form.save(commit=False)
            user_profile.user = new_user
            user_profile.save()
            if '_addanother' in request.POST:
                return redirect('regandlogin:reg_user')
            else:
                return redirect('admin_view:users')  # Redirect to a list view of user profiles
    else:
        form = UserProfileForm()

    return render(request, 'homepage/Registration.html', {'form': form})



@login_required
def users_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect(reverse('admin_view:list'))
                else:
                    profile_id = user.userprofile.id
                    return HttpResponseRedirect(reverse('admin_view:view_prof', args=[profile_id]))
            else:
                return HttpResponse("Account not Active")
        else:
            return HttpResponse("Invalid user login details supplied")
    else:
        return render(request, 'homepage/userlogin.html', {})


def self_service_reg(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new User instance for the new employee candidate
            if form.is_valid():
                new_user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                user_profile = form.save(commit=False)
                user_profile.user = new_user
                user_profile.save()
            return "Thanks for Submitting your application"
    else:
        form = UserProfileForm()

    return render(request, 'homepage/Registration.html', {'form': form})