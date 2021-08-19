from .validators import is_phone_number
from .config import CONFIG

def send_sms(phone, message):
    if not is_phone_number(phone):
        raise ValueError(f'{phone} is not valid phone number')

    if CONFIG['FAKE_SMS']:
        return None

    #TODO implement sms request statucter
    #TODO log sms