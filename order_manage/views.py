from django.contrib.auth.models import User, Permission, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, \
    IsAuthenticatedOrReadOnly
from rest_framework import status
# rest_framework的request和response解决了数据类型问题（json,xml）等
# http://www.django-rest-framework.org/tutorial/2-requests-and-responses/
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import list_route
import json
from django.core import serializers
from order_manage.models import Order, Merchandise, MerchandisePicture,\
    Location, Express, Payment, OrderStatus
from order_manage.serializers import UserSerializer, PermissionSerializer, \
    GroupSerializer, OrderSerializer, MerchandiseSerializer, \
    MerchandisePictureSerializer, LocationSerializer, ExpressSerializer, \
    PaymentSerializer, OrderStatusSerializer
from order_manage.permissions import IsAdminOrOwner


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAdminUser,)
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAdminUser,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ExpressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Express.objects.all().extra(select={'value': 'id',
                                                   'label': 'name'})
    serializer_class = ExpressSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Payment.objects.all().extra(select={'value': 'id',
                                                   'label': 'name'})
    serializer_class = PaymentSerializer


class OrderStatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = OrderStatus.objects.all().extra(select={'value': 'id',
                                                       'label': 'name'})
    serializer_class = OrderStatusSerializer


class MerchandiseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer

    def perform_create(self, serializer):
        print('creating')
        serializer.save(owner=self.request.user)


class MerchandisePictureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = MerchandisePicture.objects.all()
    serializer_class = MerchandisePictureSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    permission_classes = (IsAdminOrOwner,)
    queryset = Order.objects.all().exclude(status=7)
    serializer_class = OrderSerializer

    @list_route()
    def filtered_orders(self, request):
        # print(request.query_params)
        page = request.query_params['page']
        start = request.query_params['start']
        end = request.query_params['end']
        filter = request.query_params['filter']
        orders = Order.objects.filter(created_at__gte=start,
                                      created_at__lte=end,
                                      title__icontains=filter).exclude(status=7)

        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_info(request, format=None):
    serializer = UserSerializer(request.user, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_permissions(request, format=None):
    permissions = JSONRenderer().render(request.user.get_all_permissions(),
                                        context={'request': request})
    return Response(permissions)


@api_view(['POST'])
def add_order(request, format=None):
    data = request.data
    data['city'] = ','.join(data['city'])
    print(data['merchandise'])
    # data['merchandise'] = Merchandise.objects.get(pk=data['merchandise'])
    print(data)
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        print('valid')
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        for x in data:
            print("%s: %s" % (data[x], type(data[x])))
        return Response('data invalid')


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_locations(request, format=None):
    states = list(Location.objects.extra(select={'value': 'state_name', 'label': 'state_name', 'py': 'state_py_code'}).values('value', 'label', 'py').exclude(state_name='').distinct())
    for state in states:
        cities = list(Location.objects.exclude(city_name='').extra(select={'value': 'city_name', 'label': 'city_name', 'py': 'city_py_code'}).values('value', 'label', 'py').filter(state_name=state['value']).distinct())
        if len(cities) > 0:
            state['children'] = cities
            for city in state['children']:
                regions = list(Location.objects.exclude(region_name='').extra(select={'value': 'region_name', 'label': 'region_name', 'py': 'region_py_code'}).values('value', 'label', 'py').filter(city_name=city['value']).distinct())
                if len(regions) > 0:
                    city['children'] = regions
                    print(city['children'])
    city_json = JSONRenderer().render(states)
    return Response(city_json)
