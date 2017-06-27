from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from snail_backend import settings
from order_manage.models import Merchandise, MerchandisePicture, Location, \
    Express, Payment, OrderStatus, Order, Comment


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
        fields = ('id', 'url', 'name',)


class PaymentSerializer(serializers.ModelSerializer):
    orders = serializers.StringRelatedField(many=True)

    class Meta:
        model = Payment
        fields = ('id', 'code', 'name', 'pinyin', 'orders',)


class OrderStatusSerializer(serializers.ModelSerializer):
    orders = serializers.StringRelatedField(many=True)

    class Meta:
        model = OrderStatus
        fields = ('id', 'code', 'name', 'pinyin', 'orders',)


class ExpressSerializer(serializers.ModelSerializer):
    orders = serializers.StringRelatedField(many=True)

    class Meta:
        model = Express
        fields = ('id', 'code', 'name', 'pinyin', 'orders',)


class MerchandisePictureSerializer(serializers.ModelSerializer):
    # image = serializers.CharField()
    image = serializers.ImageField(
        max_length=1000, allow_empty_file=False, use_url=False)
    created_at = serializers.DateTimeField(
        format=settings.DATETIME_FORMAT,
        required=False,
        read_only=True)

    class Meta:
        model = MerchandisePicture
        fields = ('id', 'name', 'pinyin', 'description', 'image',
                  'merchandise', 'order', 'url')


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # merchandise = serializers.CharField(source='merchandise.name')
    # payment = serializers.ReadOnlyField(source='payment.name')
    # express = serializers.ReadOnlyField(source='express.name')
    # status = serializers.ReadOnlyField(source='status.name')
    created_at = serializers.DateTimeField(
        format=settings.DATETIME_FORMAT,
        required=False,
        read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    """
    For main order list page
    """
    merchandise = serializers.CharField(source='merchandise.name')
    payment = serializers.ReadOnlyField(source='payment.name')
    express = serializers.ReadOnlyField(source='express.name')
    status = serializers.ReadOnlyField(source='status.name')

    class Meta:
        model = Order
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    For main order list page
    """
    # 可增加字段，如何拼接字段以后探索
    title = serializers.CharField(source='cell_phone')

    class Meta:
        model = Comment
        fields = '__all__'


class MerchandiseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # pictures = serializers.StringRelatedField(many=True)
    pictures = MerchandisePictureSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    # # 订单列表以__str__返回结果显示
    # orders = serializers.StringRelatedField(many=True, read_only=True)
    end_datetime = serializers.DateTimeField(
        format=settings.DATETIME_FORMAT)
    created_at = serializers.DateTimeField(
        format=settings.DATETIME_FORMAT,
        required=False,
        read_only=True)
    # 订单列表以pk列表显示，用queryset限定修改时可选的范围
    # orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # orders = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Order.objects.filter(status=7))
    orders = OrderSerializer(many=True, read_only=True)
    # orders = serializers.HyperlinkedRelatedField(
    #             many=True,
    #             read_only=True,
    #             view_name='order-detail'
    #         )

    class Meta:
        model = Merchandise
        fields = ('id', 'name', 'pinyin', 'brand', 'price', 'old_price',
                  'is_active', 'is_bestseller', 'end_datetime', 'description',
                  'meta_keywords', 'meta_description', 'created_at', 'owner',
                  'url', 'pictures', 'orders', 'comments', )
