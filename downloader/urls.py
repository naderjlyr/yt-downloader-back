from django.contrib import admin
from django.urls import path, include

import downloads

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('downloads.urls')),
]
