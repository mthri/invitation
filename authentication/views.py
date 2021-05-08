from django.shortcuts import render, redirect, HttpResponse
from django.utils.http import is_safe_url
from django.contrib.auth import authenticate, get_user_model, logout
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.utils.decorators import method_decorator
from .forms import LoginForm

#TODO create log and redirect to blog
class Login(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if not form.is_valid() or not form.authenticate_user(request):
            return render(request, 'dashboard/login.html', context={'login_failed':True})


        redirect_to = request.GET.get('next', '/')
        if redirect_to and is_safe_url(url=redirect_to, allowed_hosts=request.get_host()):
            return redirect(redirect_to)
        else:
            return redirect('/')

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/login.html')

def Logout(request):
    logout(request)
    return redirect('/')
