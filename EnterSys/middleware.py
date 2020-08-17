from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.utils.http import urlquote_plus
from django.utils.deprecation import MiddlewareMixin
import re

class RequireLoginMiddleware(object):
    """
    Middlware which requires the user to be authenticated for all urls, except those
    defined in `settings.LOGIN_EXEMPT_URLS`.
    
    `settings.LOGIN_EXEMPT_URLS` should be a tuple of regular expresssions for the
    urls you want anonymous users to have access to. If LOGIN_EXEMPT_URLS is not defined,
    it defaults to `settings.LOGIN_URL`.
    
    Requests for urls not matching LOGIN_EXEMPT_URLS get redirected to LOGIN_URL with `next`
    set to the original path of the unauthenticted request. 
    
    All urls statically served by django are, by default, excluded from this check.
    """

    '''def __init__(self, get_response):
        self.get_response = get_response

        try:
            self.login_url = settings.LOGIN_URL
        except AttributeError:
            raise ImproperlyConfigured(u'You need to set `settings.LOGIN_URL` for the RequireLoginMiddleware.')
            
        exempt_urls = [re.compile(r'^%s$' % self.login_url[1:], re.UNICODE)]
        root_urlconf = __import__(settings.ROOT_URLCONF)
        for pattern in root_urlconf.urls.urlpatterns:
            if pattern.__dict__.get('_callback_str') == 'django.contrib.staticfiles.views.serve':
                exempt_urls.append(pattern.regex)
        exempt_urls.extend([re.compile(url, re.UNICODE) for url in getattr(settings, 'LOGIN_EXEMPT_URLS', [])])
        self.exempt_urls = exempt_urls

    def __call__(self, request):
    
        response = self.get_response(request)

        return response
        
    def process_request(self, request):
        if not request.user.is_authenticated():
            for url in self.exempt_urls:
                if url.match(request.path[1:]):
                    return None
            url = '%s?next=%s' % (self.login_url, urlquote_plus(request.path))
            return HttpResponseRedirect(url)'''


class LoginRequiredMiddleware(object):
    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):
        try:
            self.login_url = settings.LOGIN_URL
        except AttributeError:
            raise ImproperlyConfigured(u'You need to set `settings.LOGIN_URL` for the RequireLoginMiddleware.')
            
        exempt_urls = [re.compile(r'^%s$' % self.login_url[1:], re.UNICODE)]
        root_urlconf = __import__(settings.ROOT_URLCONF)
        for pattern in root_urlconf.urls.urlpatterns:
            if pattern.__dict__.get('_callback_str') == 'django.contrib.staticfiles.views.serve':
                exempt_urls.append(pattern.regex)
        exempt_urls.extend([re.compile(url, re.UNICODE) for url in getattr(settings, 'LOGIN_EXEMPT_URLS', [])])
        self.exempt_urls = exempt_urls

        response = self.get_response(request)

        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any (m.match(path) for m in self.exempt_urls):
                return HttpResponseRedirect(settings.LOGIN_URL)
        return response