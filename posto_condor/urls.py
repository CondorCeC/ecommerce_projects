from django.urls import path
from posto_condor import views


app_name = 'posto'
urlpatterns = [
    path('iniciar/', views.iniciar_avaliacao, name='iniciar_avaliacao'),
    path('listar/<str:cargo>/', views.listar_usuarios_por_cargo, name='listar_usuarios'),
    path('avaliar/<int:userposto_id>/', views.avaliar_usuario, name='avaliar_usuario'),
    path('avaliacoes/', views.listar_avaliacoes, name='listar_avaliacoes'),
    path('avaliacoes/<int:userposto_id>/', views.ver_avaliacao, name='ver_avaliacao'),
    path('posto/index/', views.index_posto, name='index_posto'),
    path('posto/user/login', views.login_posto, name='login_posto'),
    path('posto/user/logout', views.logout_posto, name='logout_posto'),
    path('api/autopostoav/', views.AutoPostoListAv.as_view(), name='AutoPostoList-listav'),
    path('exportar/avaliacoes/excel/', views.exportar_avaliacoes_para_excel, name='exportar_avaliacoes_excel'),

]