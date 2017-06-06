from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from order_manage.models import Merchandise, MerchandisePicture, Location, \
    Express, Payment, OrderStatus, Order


class UserSerializer(serializers.ModelSerializer):
    merchandises = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Merchandise.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'email',
                  'groups', 'is_active', 'is_staff', 'is_superuser', 'url',
                  'merchandises', )


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'content_type', 'codename', 'objects',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'url', 'name')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'code', 'name', 'pinyin',)


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ('id', 'code', 'name', 'pinyin',)


class ExpressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Express
        fields = ('id', 'code', 'name', 'pinyin',)


class MerchandiseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    pictures = MerchandisePicture.objects.all()

    class Meta:
        model = Merchandise
        fields = ('id', 'name', 'pinyin', 'brand', 'price', 'old_price',
                  'is_active', 'is_bestseller', 'description', 'meta_keywords',
                  'meta_description', 'created_at', 'owner', 'url', )


class MerchandisePictureSerializer(serializers.ModelSerializer):
    merchandise = serializers.ReadOnlyField(source='merchandise.name')

    class Meta:
        model = Merchandise
        fields = ('id', 'name', 'pinyin', 'description', 'created_at',
                  'merchandise', )


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False,
                                  max_length=100)
    merchandise = serializers.ModelField(model_field=Merchandise()._meta.get_field('id'))
    amount = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=9, decimal_places=2,
                                     default=0.00)
    payment = serializers.ModelField(model_field=Payment()._meta.get_field('code'))
    buyer = serializers.CharField(max_length=100, allow_blank=False)
    cell_phone = serializers.RegexField(
        # '^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}', max_length=11,
        '^1[3|4|5|8][0-9]\d{4,8}$', max_length=11,
        allow_blank=True)
    city = serializers.ListField(child=serializers.CharField(max_length=200))
    address = serializers.CharField(max_length=300, allow_blank=False)
    comment = serializers.CharField(max_length=300, allow_blank=True)
    # status = serializers.CharField(default=1)
    created_at = serializers.DateTimeField(required=False)
    express = serializers.ModelField(model_field=Express()._meta.get_field('code'))
    express_no = serializers.CharField(max_length=50, allow_blank=True)
    express_info = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        """
        Create and return a new 'Order' instance, given the validated data.
        """
        validated_data['merchandise'] = Merchandise.objects.get(pk=validated_data['merchandise'])
        validated_data['payment'] = Payment.objects.filter(code=validated_data['payment'])[0]
        validated_data['express'] = Express.objects.filter(code=validated_data['express'])[0]
        return Order.objects.create(**validated_data)
