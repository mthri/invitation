from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from utils.generic_view import DataTableView
from django.urls import reverse

from dashboard.mixins import PremissionMixin, JsonValidatorMixin
from utils.response import SuccessJsonResponse, BadJsonResponse
from .json_schema import create_payment
from utils.config import CONFIG

from payment.models import Invoice



class GetInvoice(PremissionMixin, DataTableView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        pass

class CreateInvoice(PremissionMixin, JsonValidatorMixin, View):
    http_method_names = ['post']
    json_body_schema = create_payment

    def post(self, request, *args, **kwargs):
        amount:int = self.json_body['amount']
        description:str = self.json_body['description']
        customer = request.user

        redirect_url, status = Invoice.create_invoice(customer=customer, 
                                                      amount=amount, 
                                                      description=description)

        if status:
            return SuccessJsonResponse({'redirect': redirect_url})
        else:
            return BadJsonResponse({'message': redirect_url})