from django import forms
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core import validators

from utils.validators import is_email_address, is_phone_number

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

    def authenticate_user(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        User = get_user_model()

        # authenticate with email address
        if is_email_address(username):
            user = authenticate(request, email=username, password=password)
            if user:
                login(request, user)
                return True
            else:
                return False

        # authenticate with phone number
        elif is_phone_number(username):
            user = User.objects.filter(phone=username)
            if not user.exists():
                return False
            
            user = user.first()
            if authenticate(request, email=user.email, password=password):
                login(request, user)
                return True
            else:
                return False    

        # authenticate with username
        else:
            user = User.objects.filter(username=username)
            if not user.exists():
                return False
            
            user = user.first()
            if authenticate(request, email=user.email, password=password):
                login(request, user)
                return True
            else:
                return False  


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password], required=True)
    old_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise ValidationError('confirm_password', _('تکرار رمز عبور صحیح نمی‌باشد'))
        

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError(_('رمز عبور فعلی صحیح نمی‌باشد'))
        return old_password

    def save(self):
        password = self.cleaned_data.get('password')
        self.user.set_password(password)
        self.user.save()