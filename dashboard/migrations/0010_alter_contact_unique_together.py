# Generated by Django 3.2 on 2021-08-06 22:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0009_auto_20210807_0211'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together={('owner', 'phone', 'is_deleted')},
        ),
    ]