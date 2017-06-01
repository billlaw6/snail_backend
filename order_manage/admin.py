from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from order_manage.models import Merchandise, MerchandisePicture, Order, Express

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


