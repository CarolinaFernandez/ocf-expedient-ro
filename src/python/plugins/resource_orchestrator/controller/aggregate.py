"""
Controller for the ResourceOrchestrator aggregate.
Performs aggregate CRUD operations and the
synchronization with the resources it contains.

@date: Jun 12, 2013
@author: CarolinaFernandez
"""

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import simple
from expedient.clearinghouse.utils import post_message_to_current_user
from expedient.common.messaging.models import DatedMessage
from expedient.common.permissions.shortcuts import give_permission_to
from resource_orchestrator.controller.resource_parsing import ResourceParser
from resource_orchestrator.controller.resource import ResourceOrchestrator as ResourceOrchestratorController
# IMPORTANT NOTE: Module name definitely not Pythonic, but it is 
# necessary to use the same name in module and class for Expedient 
# to be able to recognize it as a new Aggregate
from resource_orchestrator.forms.ResourceOrchestratorAggregate import ResourceOrchestratorAggregate as ResourceOrchestratorAggregateForm
from resource_orchestrator.models.ResourceOrchestratorAggregate import ResourceOrchestratorAggregate as ResourceOrchestratorAggregateModel
from resource_orchestrator.forms.xmlrpc_server_proxy import xmlrpcServerProxy as xmlrpcServerProxyForm
from resource_orchestrator.models.xmlrpc_server_proxy import xmlrpcServerProxy as xmlrpcServerProxyModel
from resource_orchestrator.models.xmlrpc_server_proxy import DEFAULT_UPLOAD_PATH
#from resource_orchestrator.models.ResourceOrchestrator import ResourceOrchestrator as ResourceOrchestratorModel
from expedient.common.clients import xmlrpc_secure
from django.core.files.base import ContentFile

import os
import random
import socket
import string


class am_resource(object):
    """
    Used to extend any object properties.
    """
    pass

def get_file_name(aggregate):
    """
    Not a view. Helper method
    """
    chars = string.ascii_uppercase + string.digits
    size = 7 
    file_name = "".join(random.choice(chars) for _ in range(size))
    try:
        file_name = "%s_%s" % (aggregate.name.replace(" ", "_").lower(), file_name)
    except Exception as e:
        print "\n\n\n\n\n\nexception!!!!!! %s" % str(e)
    return file_name

def aggregate_crud(request, agg_id=None):
    '''
    Create/update a ResourceOrchestrator Aggregate.
    '''
    if agg_id != None:
        aggregate = get_object_or_404(ResourceOrchestratorAggregateModel, pk=agg_id)
        client = aggregate.client
    else:
        aggregate = None
        client = None

    extra_context_dict = {}
    errors = ""

    if request.method == "GET":
        agg_form = ResourceOrchestratorAggregateForm(instance=aggregate)
        client_form = xmlrpcServerProxyForm(instance=client)
        
    elif request.method == "POST":
        agg_form = ResourceOrchestratorAggregateForm(
            data=request.POST, instance=aggregate)
        client_form = xmlrpcServerProxyForm(
            data=request.POST, instance=client)

        if client_form.is_valid() and agg_form.is_valid():
            # Ping is tried after every field check
            client = client_form.save(commit=False)
            print "client.certificate.name: ",  client.certificate.name
            print "client.certificate dir>> ",  client.certificate.__dict__
            print "client.certificate.instance dir>> ",  client.certificate.instance.__dict__
            print "client.key.name: ",  client.key.name
            print "client.key.name dir>> ",  client.key.__dict__
            print "client.key.instance.name dir>> ",  client.key.instance.__dict__

            # Retrieve contents of client.key and client.cert, not the whole object
            s = xmlrpc_secure.make_client(client.url, client.key.name, client.certificate.name)
            try:
                # s.GetVersion()
                sync_ro_resources(s)

            # TODO Check what happens when certificates are incorrect! (untrusted)
            # TODO Check what hapens when certificates are not signed by CH!
            except Exception as e:
                print "----------------- Expedient ---> RO connection FAILED! Details: ", e
                if isinstance(e, socket.error):
                    errors = "Could not connect to server: URL is not correct or remote RO is down"
                else:
                    errors = "Could not connect to server: either certificate or URL is not correct"

                DatedMessage.objects.post_message_to_user(
                    errors, user=request.user, msg_type=DatedMessage.TYPE_ERROR,
                )
                extra_context_dict['errors'] = errors

            if not errors:
                client = client_form.save()
                print "\n\n\n\n\nrequest FILES!!!!!!!!!!!! dict ", request.FILES.__dict__
                print "\n\n\n\n\nrequest POST!!!!!!!!!!!! dict ", request.POST.__dict__
                print "\n\n\n\n\nclient 1!!!!!!!!!!!! ", client.__dict__
                print "\n\n\n\n\nclient 1 cert!!!!!!!!!!!! ", dir(client.certificate.storage)
                print "\n\n\n\n\nclient 1 cert location!!!!!!!!!!!! ", client.certificate.storage.base_location, client.certificate.storage.path, client.certificate.storage.base_url, dir(client.certificate.storage.url), client.certificate.storage.listdir
                print "\n\n\n\n\nclient 1 key!!!!!!!!!!!! ", dir(client.key.storage)
                client_xmplrc_secure = xmlrpcServerProxyModel(request.POST, request.FILES)
                print "\n\n\n\n\nclient 2!!!!!!!!!!!! ", dir(client_xmplrc_secure)
                print "\n\n\n\n\nclient 2 certificate!!!!!!!!!!!! ", client_xmplrc_secure.__dict__["certificate"]
                print "\n\n\n\n\nclient 2 certificate!!!!!!!!!!!! 1", dir(client_xmplrc_secure.__dict__["certificate"])

                print "\n\n\n\n\nclient 2 certificate!!!!!!!!!!!! 2", client_xmplrc_secure.__dict__["certificate"].keys()

                for v in client_xmplrc_secure.__dict__["certificate"].values():
                    print "\n\n\n\n\nclient 2 certificate!!!!!!!!!!!! 3", v

                aggregate = agg_form.save(commit=False)

                #if "certificate" in request.FILES:
                #    certificate_contents = request.FILES["certificate"]
                try:
                    certificate_contents = client_xmplrc_secure.__dict__["certificate"].values()[0]
                    certificate_default_storage = client.certificate.storage
                    # from django.core.files.storage import default_storage
                    certificate_name = get_file_name(aggregate)
                    print "certificate_name: ", certificate_name
                    # "certificate_default_storage.location" not good
                    path = certificate_default_storage.save( \
                                os.path.join(DEFAULT_UPLOAD_PATH, "%s.crt" % certificate_name), \
                                ContentFile(certificate_contents.read()))
                    print "path...............", path
                    print "dir(certificate_default_storage): ", dir(certificate_default_storage)
                    print "location(certificate_default_storage): ", certificate_default_storage.location
                    certificate_file = open(path,"wb")
                    for line in certificate_contents.readlines():
                        certificate_file.write(line)
                    certificate_file.close()
                    # Update path of certificate
                    certificate.key.name = path
                    certificate.save()
                except Exception as e:
                    print "certificate.e: ", e

                try:
                    #if "key" in request.FILES:
                    #    key_contents = request.FILES["key"]
                    key_contents = client_xmplrc_secure.__dict__["key"].values()[0]
                    print "key_contents: ", key_contents
                    key_default_storage = client.key.storage
                    key_name = get_file_name(aggregate)
                    print "key_name: ", key_name
                    path = certificate_default_storage.save( \
                                os.path.join(DEFAULT_UPLOAD_PATH, "%s.key" % certificate_name), \
                                ContentFile(certificate_contents.read()))
                    print "path...............", path
                    print "dir(key_default_storage): ", key_default_storage["path"]
                    key_file = open("/opt/felix/%s" % key_name,"wb")
                    for line in key_contents.readlines():
                        key_file.write(line)
                    key_file.close()
                    # Update path of key
                    client.key.name = path
                    client.save()
                except Exception as e:
                    print "key.e: ", e

                aggregate.client = client
                # Set to available
                #aggregate.available = True
                aggregate.save()
                agg_form.save_m2m()
                aggregate.save()
                # Update agg_id to sync its resources
#                agg_id = aggregate.pk
#                # Get resources from ResourceOrchestrator AM's xmlrpc server every time the AM is updated
#                try:
#                    # TODO Process output of GetVersion for more info on associated RMs?
#                    do_sync = True
#                    if agg_form.is_bound:
#                        do_sync = agg_form.data.get("sync_resources")
#                    else:
#                        do_sync = agg_form.initial.get("sync_resources")
#
#                    if do_sync:
#                        failed_resources = sync_ro_resources(agg_id, s)
#
#                        if failed_resources:
#                            DatedMessage.objects.post_message_to_user(
#                                "Could not synchronize resources %s within Expedient" % str(failed_resources),
#                                user=request.user, msg_type=DatedMessage.TYPE_WARNING,
#                            )
#                except:
#                    warning = "Could not synchronize RO resources within Expedient"
#                    DatedMessage.objects.post_message_to_user(
#                        errors, user=request.user, msg_type=DatedMessage.TYPE_WARNING,
#                    )
#                    extra_context_dict['errors'] = warning

                give_permission_to(
                   "can_use_aggregate",
                   aggregate,
                   request.user,
                   can_delegate=True
                )
                give_permission_to(
                    "can_edit_aggregate",
                    aggregate,
                    request.user,
                    can_delegate=True
                )
                DatedMessage.objects.post_message_to_user(
                    "Successfully created/updated aggregate %s" % aggregate.name,
                    user=request.user, msg_type=DatedMessage.TYPE_SUCCESS,
                )
                return HttpResponseRedirect("/")
    else:
        return HttpResponseNotAllowed("GET", "POST")


    if not errors:
        extra_context_dict['available'] = aggregate.check_status() if agg_id else False

    # Updates the dictionary with the common fields
    extra_context_dict.update({
            "agg_form": agg_form,
            "client_form": client_form,
            "create": not agg_id,
            "aggregate": aggregate,
            "breadcrumbs": (
                ('Home', reverse("home")),
                ("%s ResourceOrchestrator Aggregate" % ("Update" if agg_id else "Create"),
                 request.path),
            )
        })

    return simple.direct_to_template(
        request,
        template="resource_orchestrator_aggregate_crud.html",
        extra_context=extra_context_dict
    )

def sync_ro_resources(xmlrpc_client):
    """
    Retrieves the resources from the Resource Orchestrator
    XMLRPC API every time the RO is updated
    """
    geni_options = {
        "geni_rspec_version": {
            "version": "3",
            "type": "geni"
        },
        "geni_available": False,
        "geni_compressed": True
    }
    # TODO: Obtain proper credentials from the ClearingHouse
    geni_credentials = []
    try:
        list_resources = xmlrpc_client.ListResources(geni_credentials, geni_options)
        print "RO > List Resources: ", list_resources
        # Call to resource_parsing to parse all data from ListResources
        try:
            parser = ResourceParser(from_string=list_resources)
        except Exception as e:
            print "RO > Unable to parse list of resources"
    except Exception as e:
        print "RO > Unable to fetch list of resources"
