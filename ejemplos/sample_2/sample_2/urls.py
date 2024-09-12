
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('exampleapp/', include('exampleapp.urls')),
    path('admin/', admin.site.urls),
]
