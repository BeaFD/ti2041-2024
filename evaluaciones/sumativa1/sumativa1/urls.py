
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls')),
    path('', RedirectView.as_view(url='/productos/consulta', permanent=True))
]