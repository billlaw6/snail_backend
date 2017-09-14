from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from order_manage.models import Merchandise, MerchandisePicture,\
    Order, Express, Payment, OrderStatus, Location, SubMerchandise

TokenAdmin.raw_id_fields = ('user',)


@admin.register(Merchandise)
class MerchandiseAdmin(admin.ModelAdmin):
    exclude = ('created_at',)


@admin.register(MerchandisePicture)
class MerchandisePictureAdmin(admin.ModelAdmin):
    exclude = ('created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = ('created_at',)


@admin.register(Express)
class ExpressAdmin(admin.ModelAdmin):
    exclude = ('created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    exclude = ('created_at',)


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    exclude = ('created_at',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    exclude = ('detail_location',)


@admin.register(SubMerchandise)
class SubMerchandiseAdmin(admin.ModelAdmin):
    exclude = ('created_at',)
