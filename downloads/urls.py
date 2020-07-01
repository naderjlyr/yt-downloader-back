from django.urls import path
from downloads import views

urlpatterns = [
    path('get_link', views.get_link),
    path('download_links', views.download_links),
]
