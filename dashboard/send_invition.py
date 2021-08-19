from utils.config import CONFIG
import invitation
from django.db import transaction
from django.utils.timezone import now

from .models import Invitation, InvitationCard
from utils.email import send_email, render_to_string
from utils.sms import send_sms

sms_text = '''
سلام {first_name} {last_name}
شما به مهمانی {invite_title} ما دعوت شدید
مشاهده دعوت نامه: {invite_linke}
'''

@transaction.atomic
def send_by_invition(invition:Invitation):

    template_file = open(invition.template.path.path, 'r').read()

    #TODO use select for update
    invition_cards = InvitationCard.objects.select_related('contact')\
                                           .filter(invitation=invition)

    for invition_card in invition_cards:
        email_address = invition_card.contact.communicative_road['email']
        first_name = invition_card.contact.first_name
        last_name = invition_card.contact.last_name
        phone = invition_card.contact.phone
        context = {**invition.informations, 'first_name':first_name, 'last_name': last_name}
        content = render_to_string(template_file, context=context)
        send_email(email_address, subject=invition.title, message=content)
        
        if invition.extra_data.get('send_sms'):
            send_sms(
                phone=phone,
                message=sms_text.format(first_name=first_name, last_name=last_name, invite_title=invition.title,
                                        invite_linke=CONFIG['HOST'] + invition_card.get_absolute_url())
            )
        
        invition_card.is_sent = True

    # or only use update
    InvitationCard.objects.bulk_update(invition_cards, ['is_sent'])

    invition.is_sent = True
    invition.save()

    

def send_ready_invition():
    unsend_invitions = Invitation.objects.filter(send_at__lte=now(), is_sent=False)
    for invition in unsend_invitions:
        send_by_invition(invition)
    