from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^inventory/$', views.Inventory.as_view(), name='products'),
    url(r'^specification/$', views.Specification.as_view(), name='specification'),
    url(r'^(?P<pk>\d+)/goods/$', views.GoodsDetail.as_view(), name='goods'),
	url(r'^create-goods/$', views.create_goods, name='create_goods'),
    url(r'^create-product/$', views.create_product, name='create_product'),
]