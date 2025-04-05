from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse_lazy

class LoginInterfaceView(LoginView):
    template_name = 'users/login.html'

class LogoutInterfaceView(View):
    def get(self, request):
        logout(request)  # Logs out the user
        return redirect('/')  # Redirect to login page
