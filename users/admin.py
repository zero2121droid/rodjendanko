from django.contrib import admin
from .models import User, Children

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name','email', 'phone', 'coins', 'created_at')
    search_fields = ('username', 'firstname', 'lastname','email')
    ordering = ('-created_at',)

@admin.register(Children)
class ChildrenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'birth_date', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)