# admin_NathySantos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crear_categoria/', views.create_category, name='crear_categoria'),
]