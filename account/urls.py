from django.urls import path
from .views import signup, signin, update_profile

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('update/', update_profile, name='update'),
]
