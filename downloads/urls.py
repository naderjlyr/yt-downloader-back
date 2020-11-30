from django.urls import path

from downloads import views
from downloads.view.youtube import youtube_views

urlpatterns = [
    path('download_links', youtube_views.DownloadVideo.as_view({'post': 'generate_youtube_url'})),
    path('youtube_query', youtube_views.DownloadVideo.as_view({'post': 'youtube_query'})),
    path('youtube_auto_suggest', youtube_views.DownloadVideo.as_view({'get': 'youtube_auto_suggest'})),
    path('search', views.SearchPost.as_view({'get': 'search'})),
]
