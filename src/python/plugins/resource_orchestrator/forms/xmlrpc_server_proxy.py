"""
Model for the xmlrpcServerProxy.
It defines the fields used in the aggregate CRUD form.

@date: Apr 29, 2010
@author: jnaous
"""

from django import forms
from resource_orchestrator.models import xmlrpcServerProxy

class xmlrpcServerProxy(forms.ModelForm):
    """
    A form to create and edit OpenFlow Aggregates.
    """

    def __init__(self, check_available=False, *args, **kwargs):
        super(xmlrpcServerProxy, self).__init__(*args, **kwargs)
        self.check_available = check_available

    class Meta:
        model = xmlrpcServerProxy
        # Defines all the fields in the model by ORDER
        fields = ("certificate", "key", "url",)

    # Validation and so on
    def clean(self):
        print "\n\n\n\n\n\n\nself.cleaned_data: %s\n\n\n\n" % str(self.cleaned_data)
        return self.cleaned_data
