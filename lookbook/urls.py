"""security URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from lookbook_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    # Any other views in your app
    path('create_lookbook/', views.create_lookbook, name='create_lookbook'),
    path('display/<int:lookbook_id>/', views.display, name='display'),
    path('profile/', views.profile, name='profile'),  # User profile page
    path('my_lookbooks/', views.my_lookbooks, name='my_lookbooks'),
    path('all_lookbooks/', views.all_lookbooks, name='all_lookbooks'),
    path('', views.all_lookbooks, name='all_lookbooks'),
    path('edit_lookbook/<int:lookbook_id>/', views.edit_lookbook, name='edit_lookbook'),
]

