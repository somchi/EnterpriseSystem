from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Employees.as_view(), name='employees'),
    url(r'^add-employee/$', views.add_employee, name='add_employee'),
    url(r'^export-employee/$', views.export_members, name="export_employee"),
    url(r'^detail/$', views.EmployeeDetail.as_view(), name='e_details'),
    url(r'^(?P<pk>\d+)/profile/$', views.Profile.as_view(), name='detail'),
    url(r'^update/$', views.EmployeeUpdate.as_view(), name='update'),
    url(r'^(?P<employee_id>\d+)/make-request', views.make_request, name='request'),
    url(r'^(?P<employee_id>\d+)/make-complain', views.make_complain, name='complain'),
    url(r'^history/$', views.RequestList.as_view(), name='leave_history'),
    url(r'^chat/$', views.EmployeeList.as_view(), name='employee_list'),

    ]