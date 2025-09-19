# admin.py (playrooms app)

from django.contrib import admin
from .models import Location, LocationImages, LocationWorkingHours, Customer, LocationCity

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "owner","address", "city", "phone", "created_at")
    search_fields = ("name", "address", "city", "phone")
    list_filter = ("name",)
    ordering = ["-created_at"]

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("location_name", "customer", "location_address", "location_min_children", "location_max_children", "created_at", "location_featured", "location_top_priority")
    list_editable = ("location_featured", "location_top_priority", "location_min_children", "location_max_children")
    search_fields = ("location_name", "customer__name", "location_address")
    list_filter = ("customer", "location_name", "location_min_children", "location_max_children")
    ordering = ["-created_at"]
    
    fieldsets = (
        ("Osnovne informacije", {
            "fields": ("location_name", "customer", "location_address", "location_city", "location_state", "location_phone", "description")
        }),
        ("Kapacitet", {
            "fields": ("location_min_children", "location_max_children", "location_accommodation_children_aged")
        }),
        ("Prioritet i isticanje", {
            "fields": ("location_featured", "location_top_priority")
        }),
        ("Sadržaji", {
            "fields": ("location_accommodation_parking", "location_accommodation_wifi", "location_accommodation_videosurveillance", 
                      "location_accommodation_air_conditioning", "location_accommodation_animator", "location_accommodation_catering")
        }),
        ("Tip i lokacija", {
            "fields": ("location_type", "location_latitude", "location_longitude")
        })
    )

@admin.register(LocationImages)
class LocationImagesAdmin(admin.ModelAdmin):
    list_display = ("location", "upload_date")
    list_filter = ("location",)
    search_fields = ("location__location_name",)
    ordering = ["-created_at"]

@admin.register(LocationWorkingHours)
class LocationWorkingHoursAdmin(admin.ModelAdmin):
    list_display = ("location", "day_of_week", "location_opening_time", "location_closing_time", "location_brake_duration")
    ordering = ("location", "day_of_week")
    list_filter = ("location", "day_of_week")
    search_fields = ("location__location_name",)
    ordering = ["-created_at"]

@admin.register(LocationCity)
class LocationCityAdmin(admin.ModelAdmin):
    list_display = ("city_name", "created_at")
    search_fields = ("city_name",)
    ordering = ["city_name"]
