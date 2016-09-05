from django.conf.urls import url

from .views import BirdListView, BirdDetailView


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', BirdDetailView.as_view(template_name='birds/detail.html'),
        name='detail'),
    url(r'^$', BirdListView.as_view(template_name='birds/index.html'), name='index'),
]
