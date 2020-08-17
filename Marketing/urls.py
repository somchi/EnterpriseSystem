from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^create-demand/$', views.CreateDemand.as_view(), name='demand'),
    url(r'^create-production/$', views.CreateProduction.as_view(), name='production'),
    url(r'^productions/$', views.ProductionList.as_view(), name='production-list'),
    url(r'^demand-list/$', views.DemandList.as_view(), name='demand-list'),
    url(r'^pro-produced/$', views.Inventory.as_view(), name='inventory'),
    url(r'^sale-list/$', views.SaleList.as_view(), name='sale'),
    url(r'^customers/$', views.CustomerList.as_view(), name='customers'),
    url(r'^(?P<pk>\d+)/customer-transactions/$', views.DemandDetail.as_view(), name='customer_trans'),
    url(r'^(?P<pk>\d+)/sale-detail/$', views.SaleDetailView.as_view(), name='sale_detail'),
    url(r'^create-sale/$', views.SaleCreate.as_view(), name='create_sale'),
    url(r'^add-customer/$', views.AddCustomer.as_view(), name='create_customer'),
    url(r'^search/$', views.SalesSearch.as_view(), name='sale_sum'),
    url(r'^sales/$', views.export_sales, name='sales'),
    ]