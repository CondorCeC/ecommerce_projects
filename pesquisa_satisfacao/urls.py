
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from pesquisa_satisfacao import views
app_name = 'NPS'
urlpatterns = [


    path('', views.index, name='index'),
    path('pesquisa/<str:pedido>/<str:data_pedido>/', views.nps, name='nps'),
    path('emailcondor/', views.envio, name='email'),
    path('api/feedback/', views.FeedbackList.as_view(), name='feedback-list'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)