# Generated by Django 3.0.8 on 2020-07-29 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200727_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='bid_price_currency',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='price_currency',
        ),
        migrations.AlterField(
            model_name='bids',
            name='bid_price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]