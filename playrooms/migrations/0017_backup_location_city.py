# Generated manually
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('playrooms', '0016_data_migrate_cities'),
    ]

    operations = [
        # Kreiraj backup polje da sačuvaš postojeće location_city stringove
        migrations.AddField(
            model_name='location',
            name='location_city_old',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        # Kopiraj postojeće location_city podatke u backup polje
        migrations.RunSQL(
            "UPDATE playrooms_location SET location_city_old = location_city WHERE location_city IS NOT NULL;",
            reverse_sql="UPDATE playrooms_location SET location_city_old = NULL;"
        ),
    ]
