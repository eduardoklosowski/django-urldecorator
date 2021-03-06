__version__ = '0.1.dev0'
__license__ = 'MIT'


from django.conf import settings
from django.conf.urls import include, url
from django.core.exceptions import ImproperlyConfigured
from importlib import import_module


try:
    SAVE_URLNAME = getattr(settings, 'URLDECORATOR_SAVE_URLNAME_IN_VIEW', False)
except ImproperlyConfigured:
    SAVE_URLNAME = False


class URLList(object):
    def __init__(self, namespace=None, lazy_import=None):
        self.namespace = namespace
        self.urls = []
        self.ready = False
        self.lazy_import = lazy_import

    def __repr__(self):
        return repr(self.get_urls())

    def __len__(self):
        self._avaliate()
        if self.namespace:
            return 1
        return len(self.urls)

    def __getitem__(self, key):
        self._avaliate()
        if self.namespace:
            return self.get_urls()[key]
        return self.urls[key]

    def __iter__(self):
        self._avaliate()
        return iter(self.get_urls())

    def _avaliate(self):
        if self.ready:
            return
        if self.lazy_import:
            import_module(self.lazy_import)
        self.ready = True

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
            if SAVE_URLNAME and name:
                if self.namespace:
                    namespace = self.namespace + ':'
                else:
                    namespace = ''
                view.urlname = namespace + name
            return view
        return func
