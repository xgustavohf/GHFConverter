from django.urls import path
from .views import index, download_video_view, termos_uso
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('download/', download_video_view, name='download_video'),
    path('termos-de-uso/', termos_uso, name='termos')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)