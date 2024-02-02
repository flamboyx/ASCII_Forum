from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as ln, authenticate, logout as lt
from django.contrib.auth.decorators import login_required
from pytils.translit import slugify

from main.models import Author
from .forms import UpdateForm


def signup(request):
    context = {}

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            ln(request, new_user)
            return redirect("update")

    context.update({
        "form": form,
        "title": "Регистрация",
    })

    return render(request, "account/signup.html", context)


def login(request):
    context = {}

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=name, password=password)
            if user is not None:
                ln(request, user)
                return redirect("home")

    context.update({
        "form": form,
        "title": "Вход",
    })

    return render(request, "account/login.html", context)


@login_required
def update_profile(request):
    name_changed = True
    context = {}

    form = UpdateForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        author = Author.objects.filter(user=request.user).first()

        if not author:
            copy_post = request.POST.copy()
            copy_post['name'] = request.user.username
            form = UpdateForm(copy_post, request.FILES or None)

            if form.is_valid():
                update_profile = form.save(commit=False)
                update_profile.user = request.user
                update_profile.save()
                return redirect("home")

        else:
            if request.POST['name'] == '':
                copy_post = request.POST.copy()
                copy_post['name'] = author.name + '1'
                form = UpdateForm(copy_post, request.FILES or None)
                name_changed = False

            else:
                form = UpdateForm(request.POST, request.FILES or None)

            if form.is_valid():
                update_profile = form.save(commit=False)
                if not name_changed:
                    author.name = update_profile.name[:-1]
                else:
                    author.name = update_profile.name
                    request.user.username = update_profile.name
                if update_profile.avatar:
                    author.avatar = update_profile.avatar
                author.save()
                request.user.save()
                return redirect("home")

    context.update({
        "form": form,
        "title": "Обновить профиль",
    })

    return render(request, "account/update.html", context)


@login_required
def logout(request):
    lt(request)
    return redirect("home")