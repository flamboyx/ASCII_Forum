from django.urls import path
from .views import home, treds, replies

urlpatterns = [
    path('', home, name='home'),
    path('<slug>/', treds, name='treds'),
    path('<category>/replies/<tred>/', replies, name='replies'),
]
