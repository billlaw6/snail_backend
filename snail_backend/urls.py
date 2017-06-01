"""snail_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken import views as rest_views
from order_manage import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'user-permissions', views.PermissionViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'merchandises', views.MerchandiseViewSet)
router.register(r'merchandise-pictures', views.MerchandisePictureViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'expresses', views.ExpressViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^get-token/', rest_views.obtain_auth_token),
    url(r'^', include(router.urls)),
    url(r'^', include('order_manage.urls')),
]