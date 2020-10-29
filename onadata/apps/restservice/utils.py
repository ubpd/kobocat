# coding: utf-8
from __future__ import unicode_literals, print_function, division, absolute_import

from onadata.apps.restservice.models import RestService
from onadata.apps.restservice.tasks import service_definition_task
from onadata.apps.restservice.tasks import service_definition_otherwise_task

def call_service(parsed_instance):
    # lookup service
    instance = parsed_instance.instance
    rest_services = RestService.objects.filter(xform=instance.xform)
    # call service send with url and data parameters
    for rest_service in rest_services:
        # Celery can't pickle ParsedInstance object,
        # let's use build a serializable object instead
        # We don't really need `xform_id`, `xform_id_string`, `instance_uuid`
        # We use them only for retro compatibility with all services (even if they are deprecated)
        data = {
            "xform_id": instance.xform.id,
            "xform_id_string": instance.xform.id_string,
            "instance_uuid": instance.uuid,
            "instance_id": instance.id,
            "xml": parsed_instance.instance.xml,
            "json": parsed_instance.to_dict_for_mongo()
        }
        service_definition_task.delay(rest_service.pk, data)

def call_service_otherwise(parsed_instance, otherwise=None):
    # lookup service
    instance = parsed_instance.instance
    rest_services = RestService.objects.filter(xform=instance.xform)
    # call service send with url and data parameters
    for rest_service in rest_services:
        # Celery can't pickle ParsedInstance object,
        # let's use build a serializable object instead
        # We don't really need `xform_id`, `xform_id_string`, `instance_uuid`
        # We use them only for retro compatibility with all services (even if they are deprecated)
        data = {
            "xform_id": instance.xform.id,
            "xform_id_string": instance.xform.id_string,
            "instance_uuid": instance.uuid,
            "instance_id": instance.id,
            "xml": parsed_instance.instance.xml,
            "json": parsed_instance.to_dict_for_mongo()
        }
        if otherwise is not None:
            data["otherwise"] = otherwise
        service_definition_otherwise_task.delay(rest_service.pk, data)

