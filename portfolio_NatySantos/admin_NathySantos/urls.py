# admin_NathySantos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categorias/crear/', views.create_category, name='create_category'),
    path('categorias/editar/<int:pk>/', views.edit_category, name='edit_category'),
    path('categorias/eliminar/<int:pk>/', views.delete_category, name='delete_category'),
    path('categorias/imagenes/<int:pk>/', views.manage_category_images, name='manage_images'),
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/nuevo/', views.cliente_create, name='cliente_create'),
    path('clientes/editar/<int:pk>/', views.cliente_edit, name='cliente_edit'),
    path('clientes/eliminar/<int:pk>/', views.cliente_delete, name='cliente_delete'),
    path('clientes/<int:cliente_id>/nueva-sesion/', views.Evento, name='crear_evento'),
    path('clientes/<int:cliente_id>/nueva_sesion/', views.crear_evento, name='crear_evento'),
    path('tipo-evento/nuevo', views.tipo_evento_create, name='tipo_evento_create'),
    path('api/tipo-eventos/', views.api_tipo_eventos, name='api_tipo_eventos'),
    path('api/tipo-eventos/delete/<int:pk>/', views.delete_tipo_evento, name='delete_tipo_evento'),
]