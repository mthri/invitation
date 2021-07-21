import re
from django.core import exceptions

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from jsonschema.exceptions import SchemaError, ValidationError as JSONValidationError
from jsonschema import Draft7Validator
from dashboard.json_schema import template_field


def is_phone_number(phone: str) -> bool:
    pattern = re.compile(r'09(1[0-9]|3[1-9]|2[0-9])-?[0-9]{3}-?[0-9]{4}')
    if re.match(pattern, phone):
        return True
    else:
        return False

def is_email_address(email: str):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

# this validator used for model field
def validate_mobile(value):
    pattern = re.compile(r'09(1[0-9]|3[1-9]|2[0-9])-?[0-9]{3}-?[0-9]{4}')
    if not re.match(pattern, value):
        raise ValidationError(
            _('شماره تلفن %(value)s صحیح نمی‌باشد'),
            params={'value': value},
        )

def validate_draft7(value):
    try:
        Draft7Validator.check_schema(value)
    except SchemaError:
        raise ValidationError(_('مقدار صحیح نمی‌باشد'))

def validate_template(value):
    # first validate draft7 format then schema validation
    validate_draft7(value)
    try:
        Draft7Validator(template_field).validate(value)
    except JSONValidationError:
        raise ValidationError(_('قالب فیلد ها صحیح نمی‌باشد'))
