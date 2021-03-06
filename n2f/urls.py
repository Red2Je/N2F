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
from django.urls import path, include
from main import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('', views.void, name='void'),
    path('error/', views.error, name='error'),
    path('formReport/', views.createExpenseReport, name='formReport'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('serviceHistoric/', views.sHistoric, name='serviceHistoric'),
    path('clientHistoric/', views.cHistoric, name='clientHistoric'),
    # path('download/<str:filename>', views.download_file, name='download'),
    path('download/<str:filename>/', views.download_file, name='download'),

    path('Refund/', views.createRefundRequest, name='RefundRequest'),
    path('ConsultRefund/', views.createConsultRefund, name='ConsultRequest'),
    path('Advance/', views.createAdvanceRequest, name='AdvanceRequest'),
    path('ConsultAdvance/', views.createConsultAdvance, name='ConsultAdvanceRequest'),
    path('Mileage/', views.createMileageExpense, name='MileageRequest'),
    path('ConsultMileage/', views.createConsultMileage, name='ConsultMileageRequest'),
    path('CreateMission/', views.createMission, name='createMission'),


    path('validation/', views.valid, name='validation'),

    path('Refund/<int:refId>/', views.modifyRefund, name='ModifyRefund'),
    path('Advance/<int:advId>/', views.modifyAdvance, name='ModifyAdvance'),
    path('Mileage/<int:milId>/', views.modifyMileage, name='ModifyMileage'),
    path('ConsultRefund/<int:refId>/', views.consultRefund, name='Consult'),
    path('ConsultAdvance/<int:advId>/', views.consultAdvance, name='ConsultAdvance'),
    path('ConsultMileage/<int:milId>/', views.consultMileage, name='ConsultMileage'),
]

urlpatterns+=staticfiles_urlpatterns()
