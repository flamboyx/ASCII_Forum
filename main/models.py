from django.db import models
from pytils.translit import slugify
from django.contrib.auth import get_user_model
from django.utils.timesince import timesince
from django_resized import ResizedImageField
from django.shortcuts import reverse
from tinymce.models import HTMLField

User = get_user_model()


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    name = models.CharField(max_length=150, unique=True, default=user.name, verbose_name='Псевдоним')
    points = models.IntegerField(default=0)
    avatar = ResizedImageField(size=[100, 100], quality=100, upload_to='avatars', default=None, null=True, blank=True, verbose_name='Аватар')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    slug = models.SlugField(max_length=10, unique=True, blank=True)
    title = models.CharField(max_length=50, unique=True)
    board = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.board)
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("treds", kwargs={
            "slug": self.slug,
        })

    @property
    def num_treds(self):
        return Tred.objects.filter(category=self).count()

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'


class Reply(models.Model):
    created_by = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:100]

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Comment(models.Model):
    created_by = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)

    def __str__(self):
        return self.content[:100]

    @property
    def num_replies(self):
        return self.replies.count()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Tred(models.Model):
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    title = models.CharField(max_length=200)
    started_by = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tred, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("replies", kwargs={
            "tred": self.slug,
            "category": self.category.slug
        })

    @property
    def num_comments(self):
        return self.comments.count()

    class Meta:
        verbose_name = 'Тред'
        verbose_name_plural = 'Треды'
