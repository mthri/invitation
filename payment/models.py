from typing import Tuple
import uuid
import logging

from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from django_mysql.models import EnumField

from dashboard.models import BasicField
from utils.payment.zp import Zarinpal, ZarinpalError
from utils.config import CONFIG

logger = logging.getLogger(__name__)

User = get_user_model()

zarinpal = Zarinpal(
    merchant_id=CONFIG['ZARINPAL_MERCHANT_ID'], 
    callback_url=CONFIG['PAYMENT_VERIFY_URL'], 
    sandbox=CONFIG['ZARINPAL_IS_SANDBOX']
)

class Invoice(BasicField):

    class Meta:
        verbose_name = _('صورت حساب')
        verbose_name_plural = _('صورت حساب ها')

    class StatusChoices(models.TextChoices):
        PAID = 'P', _('پرداخت شده')
        UNPAID = 'U', _('پرداخت نشده')
        AWAITING_PAYMENT = 'A', _('در انتظار پرداخت')
        CANCELLED = 'C', _('لغو شد')

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name=_('مشتری'), null=True, blank=False)
    status = EnumField(choices=StatusChoices.choices,  verbose_name=_('وضعیت'),
                       default=StatusChoices.AWAITING_PAYMENT)
    amount = models.IntegerField(verbose_name=_('مبلغ'))
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('توضیحات'))
    shipping_date = models.DateTimeField(verbose_name=_('زمان ارسال به درگاه'), blank=True, null=True)
    authority = models.BigIntegerField(verbose_name=_('شناسه پرداخت'), blank=True, null=True)
    reference_id = models.IntegerField(verbose_name=_('شماره پیگیری'), blank=True, null=True)

    @staticmethod
    def get_unpaid_invoice(authority:int = None):
        query = Invoice.objects.all().exclude(reference_id__isnull=False)
        if authority != None:
            query = query.filter(authority=authority).first()
        return query

    @staticmethod
    @transaction.atomic
    def paid_invoice(authority: int) -> Tuple[str, bool]:
        invoice = Invoice.get_unpaid_invoice().filter(authority=authority)
        if not invoice.exists():
            return _(f'صورت حسابی با شناسه {authority} یافت نشد'), False

        invoice = invoice.select_for_update()
        invoice = invoice.first()

        toman_amount = invoice.amount / 10

        try:
            code, message, ref_id = zarinpal.payment_verification(amount=toman_amount, 
                                                                  authority=authority)
        except ZarinpalError as ex:
            invoice.status = Invoice.StatusChoices.CANCELLED
            invoice.save()
            return _('خطا هنگام پرداخت'), False

        if code == 100:
            invoice.reference_id = ref_id
            invoice.status = Invoice.StatusChoices.PAID
            invoice.customer.cash += invoice.amount
            invoice.customer.save()
            invoice.save()
            return _('صورت حساب باموفقیت پرداخت شد'), True

        elif code == 101:
            return _('این صورت حساب قبلا پرداخت شده است'), False

        else:
            return _('خطا نامشخصی رویداده است'), False

    @staticmethod
    def create_invoice(customer:User, amount:int, description:str = _('افزایش موجودی')) -> Tuple[str, bool]:
        '''
        create new invoice and return redirect url (if no have error)
        '''
        #convert rial to toman
        toman_amount = amount / 10
        try:
            redirect_url, authority = zarinpal.payment_request(amount=toman_amount,
                                                               description=description, 
                                                               mobile=customer.phone, 
                                                               email=customer.email)
            Invoice.objects.create(
                customer=customer,
                amount=amount,
                authority=authority,
                description=description
            )
            return reverse('payment:pay', args=(authority, )), True
            
        except ZarinpalError as ex:
            logging.exception(f'when create invoice for user {customer} got: ', ex)
            return _('هنگام ایجاد صورت حساب خطایی رخ داده است'), False

    @staticmethod
    def get_by_user(customer:User):
        return Invoice.objects.filter(customer=customer).exclude(is_deleted=True)

