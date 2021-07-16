from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse

from utils.config import CONFIG

register = template.Library()

@register.filter(name='none_replace')
def none_replace(data, replace_with=''):
    if data:
        return data
    else:
        return replace_with

@register.simple_tag
def reCaptcha_input():
    return mark_safe('<input type="hidden" id="captcha" name="captcha">')

@register.simple_tag
def reCaptcha_js(url):
    site_key = reCaptcha_sitekey=CONFIG['RECAPTCHA_V3_SITE_KEY']
    
    return mark_safe(
        '<script>'
            'grecaptcha.ready(function () {'
                'grecaptcha.execute("' + site_key + '", { action: "' + reverse(url) + '" }).then(function (token) {'
                    'document.getElementById("captcha").value = token;'
                '});'
            '});'
        '</script>')