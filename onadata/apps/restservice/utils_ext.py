# coding: utf-8
from __future__ import unicode_literals, print_function, division, absolute_import

#from urllib.parse import urljoin # python3
from urlparse import urljoin # python2
from functools import reduce

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def slash_join(*args):
    """
    concatenate url fragments
    """
    return reduce(urljoin, args).rstrip("/")

def import_from_settings(attr, *args):
    """
    Load an attribute from the django settings.
    :raises:
        ImproperlyConfigured
    """
    try:
        if args:
            return getattr(settings, attr, args[0])
        return getattr(settings, attr)
    except AttributeError:
        raise ImproperlyConfigured('Setting {0} not found'.format(attr))