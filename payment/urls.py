from os import name
from django.urls import path

from . import views, ajax_views

app_name = 'payment'
urlpatterns = [
    path('verify', views.verify, name='verify'),
    path('pay/<int:authority>', views.pay, name='pay')
]

urlpatterns += [
    path('ajax/invoice/all', ajax_views.GetInvoice.as_view(), name='ajax_invoice_get_all'),
    path('ajax/invoice/add', ajax_views.CreateInvoice.as_view(), name='ajax_invoice_add')
]