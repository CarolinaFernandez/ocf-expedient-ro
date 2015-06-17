from django.conf.urls.defaults import *

urlpatterns = patterns("resource_orchestrator.controller.aggregate",
    url(r"^aggregate/create/$", "aggregate_crud", name="resource_orchestrator_aggregate_create"),
    url(r"^aggregate/(?P<agg_id>\d+)/edit/$", "aggregate_crud", name="resource_orchestrator_aggregate_edit"),
)

urlpatterns = urlpatterns + patterns("resource_orchestrator.controller.gui_dispatcher",
    url(r"^list/$", "list_resources", name="resource_orchestrator_list"),
    url(r"^create/(?P<slice_id>\d+)/(?P<agg_id>\d+)/$", "create_resources", name="resource_orchestrator_create"),
    url(r"^status/(?P<slice_id>\d+)/(?P<agg_id>\d+)/$", "status_resources", name="resource_orchestrator_status"),
    url(r"^delete/(?P<slice_id>\d+)/(?P<agg_id>\d+)/$", "delete_resources", name="resource_orchestrator_delete"),
)

