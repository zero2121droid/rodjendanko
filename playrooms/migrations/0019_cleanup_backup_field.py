# Generated manually
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('playrooms', '0018_convert_location_city_to_fk'),
    ]

    operations = [
        # Obriši backup polje nakon uspešne konverzije
        migrations.RemoveField(
            model_name='location',
            name='location_city_old',
        ),
    ]
