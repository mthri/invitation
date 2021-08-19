from datetime import timedelta
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from utils.generic_view import DataTableView
from django.db.models import F, Count, Value as V

from dashboard.mixins import PremissionMixin, JsonValidatorMixin
from utils.response import SuccessJsonResponse, BadJsonResponse
from .json_schema import create_payment
from utils.config import CONFIG
from utils.time import format_date
from payment.models import Invoice



class GetInvoice(PremissionMixin, DataTableView):
    http_method_names = ['post']
    result_args = ('id', 'status', 'amount', 
                  'description', 'authority')
    result_kwargs = {'shippingDate': F('shipping_date'),
                     'referenceId': F('reference_id'),
                     'createAt': F('created_at')}

    search_on = ('description', )

    def post(self, request, *args, **kwargs):
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        
        self.queryset = Invoice.get_by_user(request.user)

        if start_date and start_date.strip():
            start_date = format_date(start_date) + timedelta(days=-1)
            self.queryset = self.queryset.filter(created_at__gte=start_date)
        if end_date and end_date.strip():
            end_date = format_date(end_date)
            self.queryset = self.queryset.filter(created_at__lte=end_date)

        return super().post(request, *args, **kwargs)

class CreateInvoice(PremissionMixin, JsonValidatorMixin, View):
    http_method_names = ['post']
    json_body_schema = create_payment

    def post(self, request, *args, **kwargs):
        amount:int = int(self.json_body['amount'])
        description:str = self.json_body['description']
        customer = request.user

        redirect_url, status = Invoice.create_invoice(customer=customer, 
                                                      amount=amount, 
                                                      description=description)

        if status:
            return SuccessJsonResponse({'redirect': redirect_url})
        else:
            return BadJsonResponse({'message': redirect_url})