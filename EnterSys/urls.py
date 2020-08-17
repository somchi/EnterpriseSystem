"""EnterSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from Employee.form import AuthenticationFormWithPlaceholder, PasswordChangeFormWithPlaceholder, PasswordResetFormWithPlaceholder, PasswordSetFormWithPlaceholder

urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
	url(r'^employee/', include('Employee.urls', namespace ='employee')),
    url(r'^operation/', include('Operation.urls', namespace ='operation')),
    url(r'^finance/', include('Finance.urls', namespace ='finance')),
    url(r'^marketing/', include('Marketing.urls', namespace ='marketing')),
    url(r'^admin/', admin.site.urls),
    url(r'^account/login/$', auth_views.login, {'authentication_form': AuthenticationFormWithPlaceholder}, name='login'),
    url(r'^account/logout/$', auth_views.logout, {'next_page': reverse_lazy('login')}, name='logout'),
    url(r'^account/change-password/$', auth_views.password_change, {'password_change_form': PasswordChangeFormWithPlaceholder,
        'post_change_redirect': 'password_change_done'}, name='password_change'),
    url(r'^account/change-password/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^account/password-reset/$', auth_views.password_reset, {'password_reset_form': PasswordResetFormWithPlaceholder}, name='password_reset'),
    url(r'^account/password-rest/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'set_password_form': PasswordSetFormWithPlaceholder, 'post_reset_redirect': 'post_reset_redirect'},name='password_reset_confirm'),
    url(r'^account/reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
