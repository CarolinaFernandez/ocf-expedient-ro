from django.conf.urls.defaults import *

urlpatterns = patterns("resource_orchestrator.controller.aggregate",
    url(r"^aggregate/create/$", "aggregate_crud", name="resource_orchestrator_aggregate_create"),
    url(r"^aggregate/(?P<agg_id>\d+)/edit/$", "aggregate_crud", name="resource_orchestrator_aggregate_edit"),
)

urlpatterns = urlpatterns + patterns("resource_orchestrator.controller.gui_dispatcher",
    url(r"^create/(?P<slice_id>\d+)/(?P<agg_id>\d+)/$", "create_resource", name="resource_orchestrator_create"),
    url(r"^manage/(?P<resource_id>\d+)/(?P<action_type>\w+)/$", "manage_resource", name="resource_orchestrator_manage"),
    url(r"^crud/(?P<slice_id>\d+)/(?P<agg_id>\d+)/$", "resource_crud", name="resource_orchestrator_resource_crud"),
)

