from django.urls import path
from .views import index, download_video_view, termos_uso, instagram_download_view, instagram_page, download_progress, politica_privacidade, contato, facebook, download_video_facebook, youtube
from django.conf import settings
from django.conf.urls.static import static
from .views import facebook, download_video_facebook

urlpatterns = [
    path('', index, name='index'),
    path('download/', download_video_view, name='download_video'),
    path('progress/<str:task_id>/', download_progress, name='download_progress'),
    path('instagram/', instagram_page, name='instagram_page'),
    path('instagram-download/', instagram_download_view, name='instagram_download'),
    path('youtube/', youtube, name='youtube'),
    path('facebook/', facebook, name='facebook'),
    path('facebook/download/', download_video_facebook, name='download_video_facebook'),
    path('termos-de-uso/', termos_uso, name='termos'),
    path('politica-de-privacidade/', politica_privacidade, name='politica_privacidade'),
    path('contato/', contato, name='contato'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)