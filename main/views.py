from django.shortcuts import render, get_object_or_404
from .models import Author, Category, Tred


def home(request):
    forums = Category.objects.all().order_by("board")

    context = {
        "forums": forums,
    }

    return render(request, "home.html", context)


def treds(request, slug):
    category = get_object_or_404(Category, slug=slug)
    treds = Tred.objects.filter(category=category)

    context = {
        "treds": treds,
        "category": category,
    }

    return render(request, "treds.html", context)


def replies(request, category, tred):
    category = get_object_or_404(Category, slug=category)
    tred = get_object_or_404(Tred, slug=tred)

    context = {
        "tred": tred,
        "category": category,
    }

    return render(request, "replies.html", context)
