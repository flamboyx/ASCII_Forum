from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Author, Category, Tred, Comment, Reply
from .forms import TredForm


def home(request):
    forums = Category.objects.all().order_by("board")

    author = ''
    if request.user.is_authenticated:
        user = request.user
        author = Author.objects.filter(user=user).first()

    context = {
        "forums": forums,
        "author": author,
        "title": 'ASCII Forum',
    }

    return render(request, "home.html", context)


def treds(request, slug):
    category = get_object_or_404(Category, slug=slug)
    treds = Tred.objects.filter(category=category)

    author = ''
    if request.user.is_authenticated:
        user = request.user
        author = Author.objects.filter(user=user).first()

    context = {
        "treds": treds,
        "category": category,
        "author": author,
        "titles": category.board + ' - ' + category.title,
    }

    return render(request, "treds.html", context)


def replies(request, category, tred):
    category = get_object_or_404(Category, slug=category)
    tred = get_object_or_404(Tred, slug=tred)
    author = Author.objects.get(user=request.user)

    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        image = request.FILES.get("comment-image")
        new_comment, created = Comment.objects.get_or_create(created_by=author, content=comment, image=image)
        tred.comments.add(new_comment.id)

    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        image = request.FILES.get("reply-image")
        comment_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.filter(id=comment_id).first()
        new_reply, created = Reply.objects.get_or_create(created_by=author, content=reply, image=image)
        comment_obj.replies.add(new_reply.id)

    author = ''
    if request.user.is_authenticated:
        user = request.user
        author = Author.objects.filter(user=user).first()

    context = {
        "tred": tred,
        "category": category,
        "author": author,
        "title": category.title + ' - ' + tred.title,
    }

    return render(request, "replies.html", context)


@login_required
def create_tred(request, slug):
    category = get_object_or_404(Category, slug=slug)

    context = {
        "category": category,
    }

    form = TredForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        copy_post = request.POST.copy()
        copy_post['category'] = category
        if form.is_valid():
            author = Author.objects.get(user=request.user)
            new_tred = form.save(commit=False)
            new_tred.started_by = author
            new_tred.category = category
            new_tred.save()

            return redirect('treds', category.slug)

    context.update({
        "form": form,
        "title": "Создать тред"
    })

    return render(request, "create_tred.html", context)


def search_result(request):

    return render(request, "search.html")
