# Generated manually
from django.db import migrations

def create_cities_from_existing_data(apps, schema_editor):
    """
    Kreira LocationCity objekte iz postojećih location_city stringova
    i mapira Location.location_city na odgovarajuće LocationCity objekte
    """
    Location = apps.get_model('playrooms', 'Location')
    LocationCity = apps.get_model('playrooms', 'LocationCity')
    
    # Sakupi sve jedinstvene gradove iz postojećih lokacija
    existing_cities = set()
    for location in Location.objects.all():
        # Proveri da li postoji location_city polje kao string (stara struktura)
        city_name = getattr(location, 'location_city', None)
        if city_name and isinstance(city_name, str) and city_name.strip():
            existing_cities.add(city_name.strip())
    
    print(f"Found cities to migrate: {existing_cities}")
    
    # Kreiraj LocationCity objekte
    city_objects = {}
    for city_name in existing_cities:
        # Koristi get_or_create da izbegneš duplikate
        city_obj, created = LocationCity.objects.get_or_create(
            city_name=city_name,  # koristim city_name jer je to polje u modelu
            defaults={'city_name': city_name}
        )
        city_objects[city_name] = city_obj
        if created:
            print(f"Created city: {city_name}")

def reverse_migration(apps, schema_editor):
    """
    Reverse operacija - obriši sve LocationCity objekte
    """
    LocationCity = apps.get_model('playrooms', 'LocationCity')
    LocationCity.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('playrooms', '0015_locationcity'),
    ]

    operations = [
        # Prvo kreiraj LocationCity objekte iz postojećih stringova
        migrations.RunPython(
            create_cities_from_existing_data,
            reverse_migration,
        ),
    ]
