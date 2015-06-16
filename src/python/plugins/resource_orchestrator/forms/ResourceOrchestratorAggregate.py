"""
Model for the ResourceOrchestrator aggregate.
It defines the fields that will be used in the CRUD form.

@date: Apr 2, 2013
@author: CarolinaFernandez
"""

from django import forms
from resource_orchestrator.models import ResourceOrchestratorAggregate as ResourceOrchestratorAggregateModel

class ResourceOrchestratorAggregate(forms.ModelForm):
    """
    A form to create and edit ResourceOrchestrator Aggregates.
    """

#    sync_resources = forms.BooleanField(label = "Sync resources?", initial = True, required = False)

    class Meta:
        model = ResourceOrchestratorAggregateModel
        exclude = ["client", "owner", "users", "available"]
