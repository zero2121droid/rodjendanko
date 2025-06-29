from django.contrib import admin
from .models import Bookings
from .models import Rating

class BookingsAdmin(admin.ModelAdmin):
    list_display = ('public_id', 'customer', 'user', 'status', 'booking_date', 'created_at', 'updated_at')
    list_filter = ('status', 'user', 'customer')
    search_fields = ('public_id', 'customer__name', 'user__email')
    list_editable = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('public_id', 'created_at', 'updated_at')  
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

admin.site.register(Bookings, BookingsAdmin)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'location', 'rating', 'comment', 'created_at')
    search_fields = ('comment',)
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at',)
