# Generated by Django 5.2 on 2025-04-25 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
