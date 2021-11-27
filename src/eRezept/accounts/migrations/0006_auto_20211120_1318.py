# Generated by Django 3.1.7 on 2021-11-20 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_shippinginfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippinginfo',
            name='latitude_receiver',
            field=models.DecimalField(blank=True, decimal_places=6, default='0', max_digits=9),
        ),
        migrations.AddField(
            model_name='shippinginfo',
            name='latitude_sender',
            field=models.DecimalField(blank=True, decimal_places=6, default='0', max_digits=9),
        ),
        migrations.AddField(
            model_name='shippinginfo',
            name='longitude_receiver',
            field=models.DecimalField(blank=True, decimal_places=6, default='0', max_digits=9),
        ),
        migrations.AddField(
            model_name='shippinginfo',
            name='longitude_sender',
            field=models.DecimalField(blank=True, decimal_places=6, default='0', max_digits=9),
        ),
        migrations.AlterField(
            model_name='shippinginfo',
            name='state_receiver',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='shippinginfo',
            name='state_sender',
            field=models.CharField(max_length=2),
        ),
    ]
