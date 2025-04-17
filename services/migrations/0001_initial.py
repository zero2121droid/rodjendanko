# Generated by Django 5.1.1 on 2025-04-16 22:17

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('playrooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicesImages',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('service_type', models.CharField(max_length=255)),
                ('service_id', models.UUIDField()),
                ('service_image_url', models.TextField(blank=True, null=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerServices',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('service_name', models.CharField(max_length=255)),
                ('service_type', models.CharField(choices=[('Proslava Rodjendana', 'Proslava'), ('Ostalo', 'Ostalo')], max_length=50)),
                ('duration', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price_per_child', models.DecimalField(decimal_places=2, max_digits=5)),
                ('min_quantity', models.IntegerField(default=0)),
                ('max_quantity', models.IntegerField(default=0)),
                ('other_services', models.CharField(blank=True, max_length=255, null=True)),
                ('service_image_url', models.TextField(blank=True, null=True)),
                ('payment_method', models.CharField(choices=[('Besplatno', 'Besplatno'), ('Naplata', 'Naplata'), ('Drugo', 'Drugo')], max_length=50)),
                ('coins_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playrooms.customer')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='playrooms.location')),
            ],
        ),
        migrations.CreateModel(
            name='OtherServices',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('type', models.TextField()),
                ('other_service_image_url', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=5)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playrooms.customer')),
            ],
        ),
        migrations.CreateModel(
            name='PartnerServices',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField(blank=True, null=True)),
                ('delivery', models.BooleanField(default=False)),
                ('product_image_url', models.TextField(blank=True, null=True)),
                ('coins_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playrooms.customer')),
            ],
        ),
    ]
