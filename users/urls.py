from django.urls import path
from . import views
from .views import LogoutView

urlpatterns = [
    path('', views.LoginInterfaceView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]