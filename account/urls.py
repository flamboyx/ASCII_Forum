from django.urls import path
from .views import signup, login, update_profile, logout

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('update/', update_profile, name='update'),
    path('logout/', logout, name='logout'),
]
