from django.conf.urls import url

from .views import SightingListView, SightingDetailView


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', SightingDetailView.as_view(template_name='sightings/detail.html'),
        name='detail'),
    url(r'^$', SightingListView.as_view(template_name='sightings/index.html'), name='index'),
]
