# Generated by Django 5.2 on 2025-05-05 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playrooms', '0004_rename_address1_customer_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
