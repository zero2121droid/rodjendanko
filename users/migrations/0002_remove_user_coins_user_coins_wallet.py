# Generated by Django 5.2 on 2025-04-23 14:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('wallet', '0002_alter_coinswallet_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='coins',
        ),
        migrations.AddField(
            model_name='user',
            name='coins_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_wallet', to='wallet.coinswallet'),
        ),
    ]
