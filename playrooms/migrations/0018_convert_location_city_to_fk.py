# Generated manually  
from django.db import migrations, models
import django.db.models.deletion

def map_locations_to_cities(apps, schema_editor):
    """
    Mapira postojeće Location objekte na odgovarajuće LocationCity objekte
    """
    Location = apps.get_model('playrooms', 'Location')
    LocationCity = apps.get_model('playrooms', 'LocationCity')
    
    # Napravi lookup dict city_name -> LocationCity object
    city_lookup = {}
    for city in LocationCity.objects.all():
        city_lookup[city.city_name] = city
    
    # Mapuj lokacije 
    updated_count = 0
    for location in Location.objects.all():
        old_city = getattr(location, 'location_city_old', None)  # backup polje
        if old_city and old_city in city_lookup:
            # Postavi city ForeignKey na odgovarajući LocationCity objekat
            location.location_city = city_lookup[old_city]
            location.save()
            updated_count += 1
            print(f"Mapped location '{location.location_name}' to city '{old_city}'")
    
    print(f"Updated {updated_count} locations")

def reverse_mapping(apps, schema_editor):
    """
    Reverse operacija 
    """
    Location = apps.get_model('playrooms', 'Location')
    # Postavi sve location_city ForeignKey na None
    Location.objects.update(location_city=None)

class Migration(migrations.Migration):

    dependencies = [
        ('playrooms', '0017_backup_location_city'),
    ]

    operations = [
        # Promeni location_city iz CharField u ForeignKey
        migrations.RemoveField(
            model_name='location',
            name='location_city',
        ),
        migrations.AddField(
            model_name='location',
            name='location_city',
            field=models.ForeignKey(
                blank=True, 
                null=True, 
                on_delete=django.db.models.deletion.SET_NULL, 
                to='playrooms.locationcity'
            ),
        ),
        # Mapuj postojeće podatke
        migrations.RunPython(
            map_locations_to_cities,
            reverse_mapping,
        ),
    ]
