# coding: utf-8
from __future__ import unicode_literals, print_function, division, absolute_import

import logging

from celery import shared_task
from django.conf import settings

from onadata.apps.restservice.models import RestService

from onadata.apps.restservice.utils import import_from_settings
from onadata.apps.restservice.utils import slash_join

@shared_task(bind=True)
def service_definition_task(self, rest_service_id, data):
    """
    Tries to send data to the endpoint of the hook
    It retries 3 times maximum.
    - after 2 minutes,
    - after 20 minutes,
    - after 200 minutes

    :param self: Celery.Task.
    :param rest_service_id: RestService primary key.
    :param data: dict.
    """
    try:
        rest_service = RestService.objects.get(pk=rest_service_id)
        service = rest_service.get_service_definition()()
        service.send(rest_service.service_url, data)
    except Exception as e:
        logger = logging.getLogger("console_logger")
        logger.error("service_definition_task - {}".format(str(e)), exc_info=True)
        # Countdown is in seconds
        countdown = 120 * (10 ** self.request.retries)
        # Max retries is 3 by default.
        raise self.retry(countdown=countdown, max_retries=settings.REST_SERVICE_MAX_RETRIES)

    return True

@shared_task(bind=True)
def service_definition_otherwise_task(self, rest_service_id, data):
    """
    same as service_definition but for updates
    """
    try:
        rest_service = RestService.objects.get(pk=rest_service_id)
        service = rest_service.get_service_definition()()
        service_url = slash_join(rest_service.service_url, import_from_settings('REST_SERVICE_OTHERWISE_SUFFIX','') )
        service.send(service_url, data)
    except Exception as e:
        logger = logging.getLogger("console_logger")
        logger.error("service_definition_otherwise_task - {}".format(str(e)), exc_info=True)
        # Countdown is in seconds
        countdown = 120 * (10 ** self.request.retries)
        # Max retries is 3 by default.
        raise self.retry(countdown=countdown, max_retries=settings.REST_SERVICE_MAX_RETRIES)

    return True
