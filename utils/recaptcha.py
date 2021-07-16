import requests

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import CharField, Form

from utils.config import CONFIG


class reCaptcha(CharField):

    __RECAPTCH_API = 'https://www.google.com/recaptcha/api/siteverify'

    def validate(self, value: str) -> None:
        if CONFIG['RECAPTCHA_ENABLE']:
            data = {
                'secret': CONFIG['RECAPTCHA_V3_SECRET_KEY'],
                'response': value
            }
            r = requests.post(self.__RECAPTCH_API, data=data)
            result = r.json()
            if result['success']:
                if CONFIG['RECAPTCHA_V3_SCORE'] > result['score']:
                    raise ValidationError(_('شما توسط reCaptcha ربات تشخیص داده شده اید'))
            else:
                raise ValidationError(_('خطا در کپچا'))


        return super().validate(value)

class reCaptchaForm(Form):
    captcha = reCaptcha()
