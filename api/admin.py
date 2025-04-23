from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.site_header = "Rodjendanko Administration"
admin.site.site_title = "Rodjendanko Admin Portal"
admin.site.index_title = "Welcome to Rodjendanko Admin"

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("Dodatne informacije", {
            "fields": ("address", "city", "phone", "coins", "description")
        }),
    )
    list_display = ["username", "email", "is_staff", "coins"]

