from django.shortcuts import render, redirect
from homepage.forms import UserProfileForm
from .models import UserProfile

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
            form.save()
            if '_addanother' in request.POST:
                return redirect('regandlogin:reg_user')
            else:
                return redirect('admin_view:users')  # Redirect to a list view of user profiles
    else:
        form = UserProfileForm()

    return render(request, 'homepage/Registration.html', {'form': form})



@login_required
@user_passes_test(lambda user: user.is_superuser)
def users_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('admin_view:list'))
            else:
                return HttpResponse("Account not Active")
        else:
            return HttpResponse("Invalid user login details supplied")
    else:
        return render(request, 'homepage/userlogin.html', {})