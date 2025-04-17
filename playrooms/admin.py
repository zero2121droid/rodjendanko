# admin.py (playrooms app)

from django.contrib import admin
from .models import Location, LocationImages, LocationWorkingHours

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("location_name", "customer", "location_address", "created_at")
    search_fields = ("location_name", "customer__name", "location_address")
    list_filter = ("customer", "location_name")

@admin.register(LocationImages)
class LocationImagesAdmin(admin.ModelAdmin):
    list_display = ("location", "location_image_url", "upload_date")
    list_filter = ("location",)
    search_fields = ("location__location_name", "location_image_url")

@admin.register(LocationWorkingHours)
class LocationWorkingHoursAdmin(admin.ModelAdmin):
    list_display = ("location", "day_of_week", "location_opening_time", "location_closing_time", "location_brake_duration")
    ordering = ("location", "day_of_week")
    list_filter = ("location", "day_of_week")
    search_fields = ("location__location_name",)
