from django import template
from django.conf import settings

register = template.Library()

# Explicit functions are used as to not expose all settings to templates


@register.simple_tag
def linz_api_key():
    """ Fetch LINZ_API_KEY from settings """
    return getattr(settings, 'LINZ_API_KEY')


@register.simple_tag
def mapbox_api_key():
    """ Fetch MAPBOX_API_KEY from settings """
    return getattr(settings, 'MAPBOX_API_KEY')
