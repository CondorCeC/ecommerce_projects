from django.urls import path
from sacs import views


app_name = 'contact'
urlpatterns = [
    path('search/', views.search, name='search'),
    path('search2/', views.search2, name='search2'),
    path('sacs/index/', views.index, name='index'),
    path('sacs/<int:contact_id>/', views.contact, name='contact'),
    path('sacs/loja/<int:contact_id>/', views.iniciar, name='iniciar'),
    path('sacs/create/', views.create, name='create'),
    path('sacs/<int:contact_id>/delete', views.delete, name='delete'),
    path('sacs/<int:contact_id>/update', views.update, name='update'),
    path('sacs/<int:contact_id>/completed', views.completed, name='completed'),
    path('user/create', views.register, name='register'),
    path('user/login', views.login_view, name='login'),
    path('user/logout', views.logout_view, name='logout'),
    path('user/update', views.user_update, name='user_update'),
]
