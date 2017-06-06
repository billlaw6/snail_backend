from django.contrib.auth.models import User, Permission, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# rest_framework的request和response解决了数据类型问题（json,xml）等
# http://www.django-rest-framework.org/tutorial/2-requests-and-responses/
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
import json
from order_manage.models import Order, Merchandise, MerchandisePicture,\
    Location, Express, Payment, OrderStatus
from order_manage.serializers import UserSerializer, PermissionSerializer, \
    GroupSerializer, OrderSerializer, MerchandiseSerializer, \
    MerchandisePictureSerializer, LocationSerializer, ExpressSerializer, \
    PaymentSerializer, OrderStatusSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ExpressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Express.objects.all().extra(select={'value': 'id',
                                                   'label': 'name'})
    serializer_class = ExpressSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Payment.objects.all().extra(select={'value': 'id',
                                                   'label': 'name'})
    serializer_class = PaymentSerializer


class OrderStatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = OrderStatus.objects.all().extra(select={'value': 'id',
                                                       'label': 'name'})
    serializer_class = OrderStatusSerializer


class MerchandiseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MerchandisePictureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = MerchandisePicture.objects.all()
    serializer_class = MerchandisePictureSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


@api_view(['GET'])
def get_user_info(request, format=None):
    serializer = UserSerializer(request.user, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def get_user_permissions(request, format=None):
    permissions = JSONRenderer().render(request.user.get_all_permissions(),
                                        context={'request': request})
    return Response(permissions)


@api_view(['POST'])
def add_order(request, format=None):
    data = request.data
    data['city'] = json.dumps(data['city'])
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        print('valid')
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        for x in data:
            print("%s: %s" % (data[x], type(data[x])))
        return Response('asldkasd')
