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
from rest_framework.schemas import get_schema_view
from django.conf.urls.static import static
from django.conf import settings
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
router.register(r'payments', views.PaymentViewSet)
router.register(r'order-status', views.OrderStatusViewSet)

schema_view = get_schema_view(title='Pasteben API')

urlpatterns = [
    url(r'^schema/$', schema_view),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^get-token/', rest_views.obtain_auth_token),
    url(r'^', include(router.urls)),
    url(r'^', include('order_manage.urls')),
    url(r'^', include('utils.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
