# Generated by Django 5.2 on 2025-04-26 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='booking_validation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
