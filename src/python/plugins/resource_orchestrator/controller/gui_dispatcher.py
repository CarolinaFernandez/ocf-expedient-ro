"""
Graphical user interface functionalities for the
ResourceOrchestrator Aggregate Manager.

@date: Jun 12, 2013
@author: CarolinaFernandez
"""

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from expedient.clearinghouse.aggregate.models import Aggregate
from expedient.clearinghouse.slice.models import Slice
from expedient.common.messaging.models import DatedMessage
from expedient.common.utils.plugins.plugincommunicator import *
from expedient.common.utils.plugins.resources.link import Link
from expedient.common.utils.plugins.resources.node import Node
from expedient.common.utils.views import generic_crud

from resource_orchestrator.models import ResourceOrchestratorAggregate

#from resource_orchestrator.controller.resource import ResourceOrchestrator as ResourceOrchestratorController
#from resource_orchestrator import forms
#from resource_orchestrator.forms.ResourceOrchestrator import ResourceOrchestrator as ResourceOrchestratorModelForm
#from resource_orchestrator.models import ResourceOrchestrator as ResourceOrchestratorModel,\
#    ResourceOrchestratorAggregate as ResourceOrchestratorAggregateModel

import copy
import logging
import xmlrpclib

def list_resources(request):
    # TODO
    # Prepare GENIv3 server to connect to current aggregate (agg_id)
    # Send ListResources command
    DatedMessage.objects.post_message_to_user(
        "ResourceOrchestrator should send 'ListResources' command now",
        request.user, msg_type=DatedMessage.TYPE_SUCCESS)
    return HttpResponse("")

def create_resources(request, slice_id, agg_id):
    """Show a page that allows user to add a resource to the aggregate."""
    if request.method == "POST":
        # Shows error message when aggregate unreachable, disable creation through Resource Orchestrator and get back to slice detail page
        agg = Aggregate.objects.get(id = agg_id)
        if agg.check_status() == False:
            DatedMessage.objects.post_message_to_user(
                "Resource Orchestrator '%s' is not available" % agg.name,
                request.user, msg_type=DatedMessage.TYPE_ERROR,)
            return HttpResponseRedirect(reverse("slice_detail", args=[slice_id]))
        # TODO Fill with CRM, SDNRM, TNRM...
        return HttpResponseRedirect(reverse("slice_detail", args=[slice_id]))
    DatedMessage.objects.post_message_to_user(
        "ResourceOrchestrator should send 'Provision' command now",
        request.user, msg_type=DatedMessage.TYPE_SUCCESS)

def status_resources(request, slice_id, agg_id):
    # TODO
    # Get name of slice (using slice_id)
    # Prepare GENIv3 server to connect to current aggregate (agg_id)
    # Generate URN for name of slice obtained before
    # Send Status command with URN of slice
    DatedMessage.objects.post_message_to_user(
        "ResourceOrchestrator should send 'Status' command now",
        request.user, msg_type=DatedMessage.TYPE_SUCCESS)
    return HttpResponse("")

def delete_resources(request, slice_id, agg_id):
    # TODO
    # Get name of slice (using slice_id)
    # Prepare GENIv3 server to connect to current aggregate (agg_id)
    # Generate URN for name of slice obtained before
    # Send Delete command with URN of slice
    DatedMessage.objects.post_message_to_user(
        "ResourceOrchestrator should send 'Delete' command now",
        request.user, msg_type=DatedMessage.TYPE_SUCCESS)
    return HttpResponse("")

###
# Topology to show in the Expedient
#

def get_resource_managers_list(slice):
    ro_aggs = slice.aggregates.filter(leaf_name=ResourceOrchestratorAggregate.__name__.lower())
    try:
        # TODO: Use GENIv3 client to call ListResources
        for ro_agg in ro_aggs:
            ro_agg_class = ro_agg.as_leaf_class()
            project_uuid = Project.objects.filter(id = slice.project_id)[0].uuid
            # TODO: For each RO, retrieve resources, parse them and save them from each RO
    except:
        pass
    return ro_aggs

def get_resource_managers(slice):
    # TODO Fill with CRM, SDNRM, TNRM...
    return []

def get_node_description(node):
    # TODO Fill with CRM, SDNRM, TNRM...
    return "Description for %s = " % str(node)

def get_nodes_links(slice, chosen_group=None):

    ro_aggs = get_resource_managers_list(slice)
    
    # TODO Fill with CRM, SDNRM, TNRM...
    nodes = [1,2,3,4,5]
    links = [1,2,3,4,5,6,7,8,9,10]

    # Getting image for the nodes
    # FIXME: avoid to ask the user for the complete name of the method here! he should NOT know it
    try:
        image_url = reverse('img_media_resource_orchestrator', args=("sensor-tiny.png",))
    except:
        image_url = 'sensor-tiny.png'

    # For every RO aggregate in the slice
    for agg in ro_aggs:
        # For every resource in the RM
        for i, resource in enumerate(range(len(nodes))):
            nodes.append(Node(
                # Users shall not be left the choice to choose group/island; otherwise collision may arise
                name = str(resource), value = str(i), aggregate = agg, type = "Some kind of resource",
                description = get_node_description(resource), image = image_url)
            )
            links.append(
                Link(
                    target = str(links[i]), source = str(resource),
                    value = "rsc_id_%s-rsc_id_%s" % (str(links[i]), str(resource))
                    ),
                )
            links.append(
                Link(
                    target = str(links[2*i]), source = str(resource),
                    value = "rsc_id_%s-rsc_id_%s" % (str(links[2*i]), str(resource))
                    ),
            )
    return [nodes, links]

#from expedient.common.utils.plugins.plugininterface import PluginInterface
#
#class Plugin(PluginInterface):
#    @staticmethod
def get_ui_data(slice):
    """
    Hook method. Use this very same name so Expedient can get the resources for every plugin.
    """
    ui_context = dict()
    try:
        # TODO For each RM, retrieve its resources and place those appropriately
        ui_context['resource_managers_list'] = get_resource_managers_list(slice)
        ui_context['resource_managers'] = get_resource_managers(slice)
        ui_context['nodes'], ui_context['links'] = get_nodes_links(slice)
    except Exception as e:
        print "[ERROR] Problem loading UI data for plug-in 'resource_orchestrator'. Details: %s" % str(e)
    return ui_context

