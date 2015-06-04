"""
Communicates the ResourceOrchestrator Aggregate Manager with Expedient.

@date: Jun 12, 2013
@author: CarolinaFernandez
"""

from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from expedient.clearinghouse.aggregate.models import Aggregate
from expedient.common.permissions.shortcuts import must_have_permission
#from resource_orchestrator.models.resource_orchestrator import ResourceOrchestrator

# ResourceOrchestrator Aggregate class
class ResourceOrchestratorAggregate(Aggregate):

    # Resource Orchestrator Aggregate information field
    information = "An aggregate of resource managers"

    class Meta:
        app_label = 'resource_orchestrator'
        verbose_name = "Resource Orchestrator Aggregate"
    
    client = models.OneToOneField('xmlrpcServerProxy', editable = False, blank = True, null = True)

    def stop_slice(self, slice):
        super(ResourceOrchestratorAggregate, self).stop_slice(slice)
        pass

    def get_resources(self):
        try:
##            return ResourceOrchestrator.objects.filter(slice_id = slice_id, aggregate = self.pk)
#            return ResourceOrchestrator.objects.filter(aggregate = self.pk)
            return []
        except Exception as e:
            return []

    def remove_from_project(self, project, next):
        """
        aggregate.remove_from_project on a ResourceOrchestrator AM will get here first to check
        that no slice inside the project contains ResourceOrchestrator's for the given aggregate
        """
        # Check permission because it won't always call parent method (where permission checks)
        must_have_permission("user", self.as_leaf_class(), "can_use_aggregate")
        return super(ResourceOrchestratorAggregate, self).remove_from_project(project, next)

    def remove_from_slice(self, slice, next):
        """
        aggregate.remove_from_slice on a ResourceOrchestrator AM will get here first to check
        that the slice does not contain ResourceOrchestrator's for the given aggregate
        """
        # Warn if any ResourceOrchestrator (created in this slice) is found inside the ResourceOrchestrator AM
        return super(ResourceOrchestratorAggregate, self).remove_from_slice(slice, next)

