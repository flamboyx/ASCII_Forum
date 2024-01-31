import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.timesince import timesince
from django_resized import ResizedImageField
from tinymce.models import HTMLField


class CustomUserManager(UserManager):
    def _create_user(self, name, password, **extra_fields):

        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, password, **extra_fields)

    def create_superuser(self, name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    points = models.IntegerField(default=0)
    avatar = ResizedImageField(size=[100, 100], quality=100, upload_to='avatars', default=None, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    board = models.CharField(max_length=10)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Tred(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    started_by = models.ForeignKey(User, related_name='treds', on_delete=models.CASCADE)
    content = HTMLField()
    category = models.ForeignKey(Category, related_name='treds', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
