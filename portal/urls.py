from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
]
