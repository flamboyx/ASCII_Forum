from django.urls import path
from .views import home, treds, replies
urlpatterns = [
    path('', home, name='home'),
    path('treds/', treds, name='treds'),
    path('replies/', replies, name='replies'),
]