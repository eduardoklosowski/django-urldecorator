Django URLDecorator
===================

Make Django URLs with decorator.


Example
=======

project/urls.py
---------------

.. code:: python

  ...

  urlpatterns = [
      ...
      url(r'^yourapp/', include('yourapp.urls')),
      ...
  ]


yourapp/urls.py
---------------

.. code:: python

  from urldecorator import URLList

  urlpatterns = URLList(lazy_import='yourapp.views')


yourapp/views.py
----------------

.. code:: python

  from django.http import HttpResponse
  from django.views.generic import View
  from .urls import urlpatterns

  @urlpatterns.url(r'^$')
  def index_view(request):
      return HttpResponse('Index')

  @urlpatterns.url(r'^cbv/$')
  class ClassBasedView(View):
      def get(self, request, *args, **kwargs):
          return HttpResponse('Class-based View')
