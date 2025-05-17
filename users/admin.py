from django.contrib import admin
from .models import User, Children

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def get_coins(self, obj):
        wallet = getattr(obj, 'coins_wallet', None)
        return wallet.coins_balance if wallet else 0
    get_coins.short_description = 'Coins'

    list_display = ('id', 'public_id', 'first_name', 'last_name','email', 'phone', 'get_coins', 'created_at')
    search_fields = ('username', 'firstname', 'lastname','email', 'public_id')
    ordering = ('-created_at',)

@admin.register(Children)
class ChildrenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'birth_date', 'get_years', 'created_at')

    def get_years(self, obj):
        return obj.years
    get_years.short_description = 'Godine'