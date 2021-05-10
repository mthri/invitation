from django.shortcuts import render, redirect, HttpResponse
from django.utils.http import is_safe_url
from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model, logout
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from .forms import LoginForm, ChangePasswordForm

#TODO create log and redirect to blog
class Login(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if not form.is_valid() or not form.authenticate_user(request):
            return render(request, settings.LOGIN_TEMPLATE, context={'login_failed':True})


        redirect_to = request.GET.get('next', '/')
        if redirect_to and is_safe_url(url=redirect_to, allowed_hosts=request.get_host()):
            return redirect(redirect_to)
        else:
            return redirect('/')

    def get(self, request, *args, **kwargs):
        return render(request, settings.LOGIN_TEMPLATE)

class ChangePassword(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({}, status=200)
            else:  
                return redirect(settings.LOGIN_URL)
        
        if request.is_ajax():
            return JsonResponse(dict(form.errors.get_json_data()), status=400)

        return redirect(settings.LOGIN_URL)


def Logout(request):
    logout(request)
    return redirect('/')

def register(request):
    return render(request, 'dashboard/register.html')
