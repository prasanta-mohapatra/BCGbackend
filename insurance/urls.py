from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^customer/(?P<id>[0-9]*)$$', views.CustomerViewSet.as_view()),
    re_path(
        r'^allpolicydata/(?P<dt>[0-9]*)$', views.AllDataViewSet.as_view()),
    re_path(r'^analytics/(?P<region>[A-Za-z]*)$',
            views.AnalyticsViewSet.as_view()),
    re_path(r'^policy/$', views.PolicyViewSet.as_view()),
    re_path(r'^csv/', views.UploadCSV.as_view())
]
