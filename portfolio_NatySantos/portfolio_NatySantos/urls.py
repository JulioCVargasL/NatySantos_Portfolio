"""
URL configuration for portfolio_NatySantos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *
from . import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/admin/'), name='logout'),
    path('', index, name='home'),
    path('contact', views.contact, name='contact'),
    path('nathySantos/', nathySantos, name='nathySantos'),
    path('portfolio/menuPortfolio/', menuPortfolio, name='menuPortfolio'),
    path('calendar', calendar, name='calendar'),
    path('portfolio/weddings.html', weddings, name='weddings'),
    path("portfolio/15yearsOld.html", yearsOld_15, name="15yearsOld"),
    path('portfolio/timeEvents.html', timeEvents, name='timeEvents'),
    path('portfolio/<slug:category_slug>/', views.portfolio_dynamic_view, name= 'dynamic_portfolio'),
    path('', include('admin_NathySantos.urls')),
    path('admin-panel/', include('admin_NathySantos.urls'))
]
