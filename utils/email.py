from django.core.mail import send_mail
from django.template import Template, Context

# TODO implement this method
def send_email(email_address:str, subject:str, message:str):
    pass

def render_to_string(template:str, context:dict):
    template = Template(template)
    context = Context(context)
    return template.render(context)