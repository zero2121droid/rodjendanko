from django.contrib import admin
from .models import CustomerServices, PartnerServices, OtherServices, ServicesImages

@admin.register(CustomerServices)
class CustomerServicesAdmin(admin.ModelAdmin):
    list_display = ("service_name", "customer", "price_per_child", "coins_price")
    search_fields = ("service_name", "customer__name")
    list_filter = ("customer",)

@admin.register(PartnerServices)
class PartnerServicesAdmin(admin.ModelAdmin):
    list_display = ("product_name", "customer", "price_per_unit")
    search_fields = ("product_name", "customer__name")
    list_filter = ("customer",)

@admin.register(OtherServices)
class OtherServicesAdmin(admin.ModelAdmin):
    list_display = ("name", "price_per_unit", "customer")
    list_filter = ("customer",)
    ordering = ("customer",)
    search_fields = ("name",)

@admin.register(ServicesImages)
class ServicesImagesAdmin(admin.ModelAdmin):
    list_display = ("service_type", "service_id", "service_image_url")
    list_filter = ("service_type",)

