from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginInterfaceView.as_view(), name='login'),
    path('logout/', views.LogoutInterfaceView.as_view(), name='logout'),
]