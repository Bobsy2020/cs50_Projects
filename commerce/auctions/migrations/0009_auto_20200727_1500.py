# Generated by Django 3.0.8 on 2020-07-27 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_bids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='bid_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]