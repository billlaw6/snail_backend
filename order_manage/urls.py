from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from order_manage import views

urlpatterns = [
    url(r'^user-info/$', views.get_user_info),
    url(r'^user-permissions/$', views.get_user_permissions),
    url(r'^china/$', views.get_locations),
    url(r'^add_order/$', views.add_order),
]

urlpatterns = format_suffix_patterns(urlpatterns)

