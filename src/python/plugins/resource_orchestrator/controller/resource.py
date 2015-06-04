"""
Controller for the ResourceOrchestrator object.
Performs the operations to create, update and
delete such objects.

@date: Jun 12, 2013
@author: CarolinaFernandez
"""

#from resource_orchestrator.models.ResourceOrchestrator import ResourceOrchestrator as ResourceOrchestratorModel
from resource_orchestrator.utils.validators import validate_resource_name
import decimal, random

class ResourceOrchestrator():
    """
    Manages creation/edition of ResourceOrchestrators from the input of a given form.
    """
    
    @staticmethod
    def create(instance, aggregate_id, slice=None):
        # TODO add
        pass

    @staticmethod
    def fill(instance, slice, aggregate_id, resource_id = None):
        # TODO add
        return instance

    @staticmethod
    def delete(resource_id):
        # TODO add
        pass

