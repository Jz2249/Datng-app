from django.shortcuts import render, redirect   

# Create your views here.
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

### TODO email password reset
def something_to_do():
    pass

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")  
    else:
        form = AuthenticationForm(request)
    context =  {"form": form}
    return render(request, "accounts/login.html", context)


def logout_view(request): ###TODO should have options to go to homepage
    if request.method == "POST":
        logout(request)
        return redirect("/login")
    return render(request, "accounts/logout.html")

def register_view(request): ###TODO generate a random user id for the new user
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        messages.success(request, f'You have successfully signed up!')
        return redirect('/login')
    context = {"form" : form}
    return render(request, 'accounts/register.html', context)

@login_required
def profile_view(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid(): # should always validate before save
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account is updated successfully!')
            return redirect('/profile')
    else: # not change anything
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile.html', context)



def account_details(request, id=None):
    if id is not None:
        acc = Profile.objects.get(id=id)
        context = {
            "Account" : acc
        }
        
        return render(request, "accounts/profile.html", context)
    
    
    
    
    
    
    
    
    

    
    
    
