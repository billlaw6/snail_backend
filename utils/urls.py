from django.conf.urls import url
from utils import views

urlpatterns = [
    url(r'^get-express-info/$', views.get_express_info),
]
