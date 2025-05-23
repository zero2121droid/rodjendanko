# Generated by Django 5.2 on 2025-04-23 07:52

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('playrooms', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Na čekanju', 'Na Cekanju'), ('Prihvacen', 'Prihvacen'), ('Odbijen', 'Odbijen'), ('Otkazan', 'Otkazan')], default='Na čekanju', max_length=20)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('booking_validation_date', models.DateTimeField(auto_now_add=True)),
                ('booking_type', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playrooms.customer')),
                ('customer_services', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.customerservices')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playrooms.location')),
            ],
        ),
    ]
