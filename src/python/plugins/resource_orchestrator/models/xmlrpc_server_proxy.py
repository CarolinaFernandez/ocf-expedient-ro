"""
Implements a server proxy for XML-RPC calls that checks SSL certs and
uses a password to talk to the server. The password is automatically renewed
whenever it expires.

@date: Apr 29, 2010
@author: jnaous
"""

from django.db import models
from django.conf import settings
import os

DEFAULT_UPLOAD_PATH = os.path.join(settings.SRC_DIR, "python/plugins/resource_orchestrator/cert/trusted")

class xmlrpcServerProxy(models.Model):

    class Meta:
        app_label = "resource_orchestrator"
        verbose_name = "Resource Orchestrator XMLRPC Server"

    certificate = models.FileField(
        upload_to=DEFAULT_UPLOAD_PATH,
        default=os.path.join("/etc/apache2/ssl.crt/server.crt"),
        help_text="Certificate trusted by this Resource Orchestrator.")

    key = models.FileField(
        upload_to=DEFAULT_UPLOAD_PATH,
        default=os.path.join("/etc/apache2/ssl.key/server.key"),
        help_text="Key corresponding to the certificate.")

    url = models.URLField("Server URL", verify_exists = False, max_length=1024,
         help_text="URL used to access the remote server's xmlrpc interface, should be https://DOMAIN_OR_IP:PORT/ROUTE_TO_XMLRPC_INTERFACE")
