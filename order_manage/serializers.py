from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from order_manage.models import Order, Merchandise, MerchandisePicture, Location, Express


class UserSerializer(serializers.ModelSerializer):
    merchandises = serializers.PrimaryKeyRelatedField(many=True, queryset=Merchandise.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'email',
                  'groups', 'is_active', 'is_staff', 'is_superuser', 'url', 'merchandises', )

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'content_type', 'codename', 'objects',)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'url', 'name')

class ExpressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Express
        fields = ('id', 'code', 'name', 'pinyin', 'label', 'value',)

class MerchandiseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    pictures = MerchandisePicture.objects.all()
    class Meta:
        model = Merchandise
        fields = ('id', 'name', 'pinyin', 'brand', 'price', 'old_price', 'is_active',
                  'is_bestseller', 'description', 'meta_keywords', 'meta_description',
                  'created_at', 'owner', 'url', )


class MerchandisePictureSerializer(serializers.ModelSerializer):
# class MerchandisePictureSerializer(serializers.HyperlinkedModelSerializer):
    merchandise = serializers.ReadOnlyField(source='merchandise.name')
    class Meta:
        model = Merchandise
        fields = ('id', 'name', 'pinyin', 'description', 'created_at', 'merchandise', )

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'title', 'merchandise', 'amount', 'price', 'payment',
                  'buyer', 'cell_phone', 'state', 'city', 'region', 'address',
                 'comment', 'status', 'created_at', 'express_no',
                  'express_info', 'url', )

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
