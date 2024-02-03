from django.urls import path
from .views import home, treds, replies, create_tred, search_result

urlpatterns = [
    path('', home, name='home'),
    path('<slug>/', treds, name='treds'),
    path('<category>/replies/<tred>/', replies, name='replies'),
    path('<slug>/create_tred/', create_tred, name='create_tred'),
    path('search', search_result, name='search_result'),
]
