from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('setting/', views.Setting.as_view(), name='setting')
]
