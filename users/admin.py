from django.contrib import admin
from .models import User, Children
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def get_coins(self, obj):
        wallet = getattr(obj, 'coins_wallet', None)
        return wallet.coins_balance if wallet else 0
    get_coins.short_description = 'Coins'

    list_display = ('id', 'public_id', 'first_name', 'last_name','email', 'phone', 'get_coins', 'created_at')
    search_fields = ('username', 'first_name', 'last_name','email', 'public_id')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

    # Ako koristiš `USERNAME_FIELD = 'email'`, ovo treba:
    filter_horizontal = ("groups", "user_permissions")

@admin.register(Children)
class ChildrenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'birth_date', 'get_years', 'created_at')

    def get_years(self, obj):
        return obj.years
    get_years.short_description = 'Godine'