from django.conf.urls import url
#from django.views.generic import TemplateView

from .views import BirdListView


urlpatterns = [
    #url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^$', BirdListView.as_view(template_name='index.html')),
]
