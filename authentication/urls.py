from django.urls import path

from . import views

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout, name='logout'),
    path('password/change', views.ChangePassword.as_view(), name='change_password'),

]
