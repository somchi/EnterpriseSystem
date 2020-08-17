from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^process/$', views.process, name='pay_process'),
    url(r'^batch/(?P<id>\d+)/$', views.BatchDetailView.as_view(), name='pay_batch_detail'),
]