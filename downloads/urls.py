from django.urls import path
from downloads import views

urlpatterns = [
    path('download_links/<video_link>', views.DownloadVideo.as_view({'post': 'generate_url'})),
    path('download_links/<video_link>/<format_id>', views.DownloadVideo.as_view({'post': 'generate_url'})),
    path('youtube_query', views.DownloadVideo.as_view({'post': 'youtube_query'})),
    path('youtube_auto_suggest', views.DownloadVideo.as_view({'get': 'youtube_auto_suggest'})),
]
