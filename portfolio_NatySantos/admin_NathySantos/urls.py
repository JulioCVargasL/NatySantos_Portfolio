# admin_NathySantos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categorias/crear/', views.create_category, name='create_category'),
    path('categorias/editar/<int:pk>/', views.edit_category, name='edit_category'),
    path('categorias/eliminar/<int:pk>/', views.delete_category, name='delete_category'),
    path('categorias/imagenes/<int:pk>/', views.manage_category_images, name='manage_images'),
    path('clientes/', views.clientes_list, name='clientes_list')
]