import json

from django.contrib.auth.mixins import AccessMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest

from jsonschema.validators import Draft7Validator
from jsonschema.exceptions import ValidationError as JsonValidationError

class PremissionMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class JsonValidatorMixin(object):
    json_body_schema = None

    #TODO check content type must be a json
    def dispatch(self, request:HttpRequest, *args, **kwargs):
        if not self.json_body_schema:
            raise AttributeError('Please set `json_body_schema`')
        try:
            self.json_body = json.loads(request.body.decode('utf8'))
            Draft7Validator(self.json_body_schema).validate(self.json_body)
            return super().dispatch(request, *args, **kwargs)
        except JsonValidationError:
            return HttpResponseBadRequest()
