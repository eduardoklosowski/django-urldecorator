__version__ = '0.1.dev0'
__license__ = 'MIT'


from django.conf import settings
from django.conf.urls import include, url
from django.core.exceptions import ImproperlyConfigured


try:
    FORCE_NAMESPACE = getattr(settings, 'URLDECORATOR_FORCE_NAMESPACE', False)
except ImproperlyConfigured:
    FORCE_NAMESPACE = False


class NamespaceError(Exception):
    pass


class URLList(object):
    def __init__(self, namespace=None):
        if FORCE_NAMESPACE and namespace is None:
            raise NamespaceError('Namespace not defined')
        self.namespace = namespace
        self.urls = []

    def get_urls(self):
        if self.namespace:
            return [url(r'', include(self.urls, namespace=self.namespace))]
        return self.urls

    def add_url(self, regex, view, kwargs=None, name=None, prefix=''):
        self.urls.append(url(regex, view, kwargs, name=name, prefix=prefix))

    def url(self, regex, kwargs=None, name=None, prefix=''):
        def func(view):
            if hasattr(view, 'as_view') and callable(view.as_view):
                view_function = view.as_view()
            else:
                view_function = view
            self.add_url(regex, view_function, kwargs, name=name, prefix=prefix)
            return view
        return func
