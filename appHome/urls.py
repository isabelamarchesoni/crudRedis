from django.urls import path
from . import views

urlpatterns = [
    path('tarefa/criar/', views.criar_tarefa, name='criar_tarefa'),  
    path('tarefa/ler/<int:id_tarefa>/', views.ler_tarefa, name='ler_tarefa'),  
    path('tarefa/atualizar/<int:id_tarefa>/', views.atualizar_tarefa, name='atualizar_tarefa'),  
    path('tarefa/deletar/<int:id_tarefa>/', views.deletar_tarefa, name='deletar_tarefa'),  
    path('tarefa/listar/', views.listar_tarefas, name='listar_tarefas'), 
    path('', views.home, name='home'),
]