from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UpdateForm


def signup(request):
    context = {}

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("update")

    context.update({
        "form": form,
        "title": "Signup",

    })

    return render(request, "account/signup.html", context)


def signin(request):
    context = {}

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=name, password=password)
            if user is not None:
                return redirect("home")

    context.update({
        "form": form,
        "title": "Signin",
    })

    return render(request, "account/signin.html", context)


@login_required
def update_profile(request):
    context = {}

    user = request.user
    form = UpdateForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            update_profile = form.save(commit=False)
            update_profile.user = user
            update_profile.save()
            return redirect("home")

    context.update({
        "form": form,
        "title": "Update",
    })

    return render(request, "account/update.html", context)
