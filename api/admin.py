from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.site_header = "Rodjendanko Administration"
admin.site.site_title = "Rodjendanko Admin Portal"
admin.site.index_title = "Welcome to Rodjendanko Admin"

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    def get_coins(self, obj):
        return obj.coins_wallet.coins_balance if obj.coins_wallet else 0
    get_coins.short_description = 'Coin balans'

    fieldsets = UserAdmin.fieldsets + (
        ("Dodatne informacije", {
            "fields": ("address", "city", "phone", "description")
        }),
    )

    list_display = ["username", "email", "is_staff", "get_coins"]
    readonly_fields = ["get_coins"]
    ordering = ["-created_at"]

