from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import CustomUser, Profile


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        user  = form.save(commit=False)
        user.username = email
        user.email    = email
        user.save()
        login(request, user)
        return redirect('profile_setup')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    form  = LoginForm(request.POST or None)
    error = None
    if request.method == 'POST':
        if form.is_valid():
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user     = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                # If profile not set up yet, go to setup
                if not hasattr(user, 'profile') or not user.profile.setup_done:
                    return redirect('profile_setup')
                return redirect('home')
            else:
                error = 'Invalid email or password.'
        else:
            error = 'Please enter a valid college email.'
    return render(request, 'accounts/login.html', {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_setup_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            p = form.save(commit=False)
            p.setup_done = True
            p.save()
            messages.success(request, f'Welcome to COER Marketplace, {p.full_name.split()[0]}! 🎉')
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_setup.html', {'form': form})


@login_required
def edit_profile_view(request):
    profile = request.user.profile
    year_choices = ['1st Year', '2nd Year', '3rd Year', '4th Year', 'Post-Grad']
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully! ✅')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'profile': profile,
        'year_choices': year_choices,
    })
