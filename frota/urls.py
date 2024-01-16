from django.urls import path
from frota import views


app_name = 'entrega'
urlpatterns = [
    path('entrega/<int:entrega_id>/', views.entrega, name='entrega'),
    path('update-status/', views.update_entrega_status, name='update_entrega_status'),
    path('selected_entregas/', views.selected_entregas, name='selected_entregas'),
    path('contact/rota/', views.rota, name='rota'),
    path('entrega/detalhe/', views.detalhamento, name='detalhamento'),
    path('remover/<int:entrega_id>/', views.remove_ent, name='remover'),
    path('finalizar/<int:entrega_id>/', views.finalizar_entrega, name='finalizar_entrega'),
    path('insucesso/<int:entrega_id>/', views.insucesso, name='insucesso'),
    path('entrega/', views.index_entrega, name='index_entrega'),
    path('entrega/create/', views.create_entrega, name='create_entrega'),
    path('export_to_excel', views.export_to_excel, name='export_to_excel'),
    path('entrega/user/login', views.login_entrega, name='login_entrega'),
    path('entrega/user/logout', views.logout_entrega, name='logout_entrega'),
    
]