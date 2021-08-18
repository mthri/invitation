# Generated by Django 3.2 on 2021-08-17 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='آیا حذف شده است؟')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', django_mysql.models.EnumField(choices=[('P', 'پرداخت شده'), ('U', 'پرداخت نشده'), ('A', 'در انتظار پرداخت'), ('C', 'لغو شد')], default='A', verbose_name='وضعیت')),
                ('amount', models.IntegerField(verbose_name='مبلغ')),
                ('description', models.CharField(blank=True, max_length=250, null=True, verbose_name='توضیحات')),
                ('shipping_date', models.DateTimeField(blank=True, null=True, verbose_name='زمان ارسال به درگاه')),
                ('authority', models.BigIntegerField(blank=True, null=True, verbose_name='شناسه پرداخت')),
                ('reference_id', models.IntegerField(blank=True, null=True, verbose_name='شماره پیگیری')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
            ],
            options={
                'verbose_name': 'صورت حساب',
                'verbose_name_plural': 'صورت حساب ها',
            },
        ),
    ]