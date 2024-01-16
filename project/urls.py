
from django.contrib import admin
from django.urls import path, include   
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('pesquisa_satisfacao.urls')),
    path('', include('sacs.urls')),
    path('', include('frota.urls')),
    path('', include('posto_condor.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)