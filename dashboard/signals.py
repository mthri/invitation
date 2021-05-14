import logging

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from django_mysql.models import SetF

from .models import Contact, Tag

logger = logging.getLogger(__name__)

# when we want delete some tag, must update all contact have that tag
@receiver(pre_delete, sender=Tag)
def update_contact_tag(sender, instance, **kwarg):
    tag_id = str(instance.id)
    owner_id = instance.owner.id
    Contact.objects.filter(owner__id=owner_id, tags__contains=tag_id)\
                   .update(tags=SetF('tags')\
                   .remove(tag_id))
    logger.info(f'update all contact contain tag {tag_id} for user {owner_id}')


