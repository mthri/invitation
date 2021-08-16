from os import name
from django.urls import path

from . import views

app_name = 'payment'
urlpatterns = [
    path('verify', views.verify, name='verify'),
    path('pay/<int:authority>', views.pay, name='pay')
]