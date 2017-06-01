from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from order_manage import views

urlpatterns = [
    url(r'^user-info/$', views.get_user_info),
    url(r'^user-permissions/$', views.get_user_permissions),
]

urlpatterns = format_suffix_patterns(urlpatterns)

