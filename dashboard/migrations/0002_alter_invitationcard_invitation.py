# Generated by Django 3.2 on 2021-08-17 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitationcard',
            name='invitation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cards', to='dashboard.invitation', verbose_name='دعوت'),
        ),
    ]