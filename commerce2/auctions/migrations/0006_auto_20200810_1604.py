# Generated by Django 3.0.8 on 2020-08-10 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200810_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(max_length=2000),
        ),
    ]
