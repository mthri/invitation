from django.shortcuts import redirect
from django.http import Http404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required


from .models import *

@login_required
def verify(request):
    if request.GET.get('Status') == 'OK':
        authority = int(request.GET['Authority'])
        result, status = Invoice.paid_invoice(authority)
        
    return redirect('transactions')

@login_required
def pay(request, authority):
    redirect_url = zarinpal.payment_url(authority)
    invoice = Invoice.get_unpaid_invoice(authority=authority)
    if not invoice:
        raise Http404
    
    invoice.shipping_date = now()
    invoice.status = Invoice.StatusChoices.UNPAID
    invoice.save()

    return redirect(redirect_url)

@login_required
def create_invoice(request):
    pass
    
