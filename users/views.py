from django.shortcuts import render, redirect
from .forms import *
from entries.models import Post
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
@csrf_protect
def register(request):
    logout(request)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('blog_view')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile_view(request, *args, **kwargs):
    print(dir(request.user.userprofile))
    posts = Post.objects.filter(author=request.user).order_by('-date')[:4]
    return render(request, "users/profile.html", {
        'posts': posts
    })


@csrf_protect
@login_required
def edit_view(request):
    print(dir(request))
    if request.method == 'POST':
        usr_form = UserUpdateForm(request.POST, instance=request.user)
        prof_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if usr_form.is_valid() and prof_form.is_valid():
            usr_form.save()
            prof_form.save()
            return redirect('profile_view')
    else:
        usr_form = UserUpdateForm(instance=request.user)
        prof_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'usr_form': usr_form, 'prof_form': prof_form
    }

    return render(request, 'users/update_profile.html', context)
