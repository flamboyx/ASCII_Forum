from django.shortcuts import render


def home(request):
    return render(request, "home.html", {})


def treds(request):
    return render(request, "treds.html", {})


def replies(request):
    return render(request, "replies.html", {})