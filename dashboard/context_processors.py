from utils.config import CONFIG

def global_vars(request):
    return {
        'reCaptcha_key': CONFIG['RECAPTCHA_V3_SITE_KEY']
    }