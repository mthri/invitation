import re

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def is_phone_number(phone:str)-> bool:
    pattern = re.compile(r'09(1[0-9]|3[1-9]|2[0-9])-?[0-9]{3}-?[0-9]{4}')
    if re.match(pattern, phone):
        return True
    else: 
        return False

def is_email_address(email:str):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

