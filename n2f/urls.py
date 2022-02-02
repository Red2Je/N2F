"""n2f URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('void/', views.void, name = 'void'),
<<<<<<< HEAD
    path('form/', views.createExpenseline),
    path('formReport/', views.createExpenseReport),
    path('login/', views.login),
    path('logoutPage/', views.logoutPage),
    path('serviceHistoric/', views.sHistoric),
=======
    path('form/', views.createExpenseline, name='form'),
    path('formReport/', views.createExpenseReport, name='formReport'),
    path('login/', views.login, name='login'),
    path('logoutPage/', views.logoutPage, name='logout'),
>>>>>>> 8377e1a051dbb37aeb940fc55b8904ad9137c50d

]
