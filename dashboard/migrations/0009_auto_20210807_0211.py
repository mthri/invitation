# Generated by Django 3.2 on 2021-08-06 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_invitationcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AddField(
            model_name='contact',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='آیا حذف شده است؟'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='آیا حذف شده است؟'),
        ),
        migrations.AddField(
            model_name='invitationcard',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AddField(
            model_name='invitationcard',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='آیا حذف شده است؟'),
        ),
        migrations.AddField(
            model_name='tag',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AddField(
            model_name='tag',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='آیا حذف شده است؟'),
        ),
        migrations.AddField(
            model_name='template',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AddField(
            model_name='template',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='آیا حذف شده است؟'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='title',
            field=models.CharField(default='ندارد', max_length=150, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='invitationcard',
            name='is_sent',
            field=models.BooleanField(default=False, verbose_name='ارسال شده'),
        ),
    ]