# coding: utf-8
from django.urls import re_path, include
from django.views.generic import TemplateView
from registration.backends.default.views import ActivationView

from onadata.apps.main.forms import RegistrationFormUserProfile
from onadata.apps.main.registration_views import FHRegistrationView

"""
URLConf for Django user registration and authentication.

Recommended usage is a call to ``include()`` in your project's root
URLConf to include this URLConf for any URL beginning with
``/accounts/``.

"""

urlpatterns = [
    # '',
    re_path(r'^activate/complete/$',
            TemplateView.as_view(
                template_name='registration/activation_complete.html'),
            name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    re_path(r'^activate/(?P<activation_key>\w+)/$',
            ActivationView.as_view(),
            name='registration_activate'),
    re_path(r'^register/$',
            FHRegistrationView.as_view(form_class=RegistrationFormUserProfile),
            name='registration_register'),
    re_path(r'^register/complete/$',
            TemplateView.as_view(
                template_name='registration/registration_complete.html'),
            name='registration_complete'),
    re_path(r'', include('registration.auth_urls')),
]
