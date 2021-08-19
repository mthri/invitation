# Generated by Django 3.2 on 2021-08-19 20:18

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_invitation_is_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='extra_data',
            field=models.JSONField(null=True, verbose_name='اطلاعات اضافی'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='informations',
            field=models.JSONField(validators=[utils.validators.validate_draft7], verbose_name='اطلاعات قالب'),
        ),
    ]