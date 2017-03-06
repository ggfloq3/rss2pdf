from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    url(r'^$', csrf_exempt(views.MyFormView.as_view())),
    url(r'^data$', views.GetJsonData.as_view()),
    url(r'^demo$', views.DemoDigest.as_view()),
]
