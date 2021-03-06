# Generated by Django 3.1.7 on 2021-11-27 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20211127_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippinginfo',
            name='address_receiver',
            field=models.CharField(blank=True, default='542 W. 15th Street', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='shippinginfo',
            name='city_receiver',
            field=models.CharField(blank=True, default='New York', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='shippinginfo',
            name='email_receiver',
            field=models.EmailField(blank=True, default='john@example.com', max_length=254, null=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='shippinginfo',
            name='name_receiver',
            field=models.CharField(blank=True, default='John M. Doe', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='shippinginfo',
            name='state_receiver',
            field=models.CharField(blank=True, default='NY', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='shippinginfo',
            name='zip_receiver',
            field=models.IntegerField(blank=True, default=10001, null=True),
        ),
    ]
