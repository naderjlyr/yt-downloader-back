from django.urls import path
from downloads import views

urlpatterns = [
    path('download_links', views.DownloadVideo.as_view()),
    path('download/<str:path>', views.download),
]
