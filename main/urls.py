from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home, treds, replies

urlpatterns = [
    path('', home, name='home'),
    path('<slug>/', treds, name='treds'),
    path('<category>/replies/<tred>/', replies, name='replies'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
