4# Original imports from expedient
"""
from resource_orchestrator.utils.parsers.parser_base import ParserBase
from resource_orchestrator.utils.parsers.crm.advertisement_parser import CRMv3AdvertisementParser
from resource_orchestrator.utils.parsers.crm.manifest_parser import CRMv3ManifestParser

from resource_orchestrator.utils.parsers.openflow.advertisement_parser import OFv3AdvertisementParser
from resource_orchestrator.utils.parsers.openflow.manifest_parser import OFv3ManifestParser

from resource_orchestrator.utils.parsers.ro.advertisement_parser import ROv3AdvertisementParser
from resource_orchestrator.utils.parsers.ro.manifest_parser import ROManifestParser
from resource_orchestrator.utils.parsers.serm.advertisement_parser import SERMv3AdvertisementParser
from resource_orchestrator.utils.parsers.serm.manifest_parser import SERMv3ManifestParser
#from resource_orchestrator.utils.parsers.tnrm.advertisement_parser import TNRMv3AdvertisementParser
#from resource_orchestrator.utils.parsers.tnrm.manifest_parser import TNRMv3ManifestParser
"""

# Imports from external testing
import os, sys
libpath = "/opt/felix/ocf/expedient/src/python/plugins/resource_orchestrator/utils/parsers/"
sys.path.append(libpath)

from parser_base import ParserBase
from crm.advertisement_parser import CRMv3AdvertisementParser
from crm.manifest_parser import CRMv3ManifestParser

from openflow.advertisement_parser import OFv3AdvertisementParser
from openflow.manifest_parser import OFv3ManifestParser

from ro.advertisement_parser import ROv3AdvertisementParser
from ro.manifest_parser import ROManifestParser

from serm.advertisement_parser import SERMv3AdvertisementParser
from serm.manifest_parser import SERMv3ManifestParser


# Class for testing purposes only
class mcolors:
    OKGREEN = '\033[92m'
    CRM = '\033[1;33m'
    RO = '\033[36m'
    OF = '\033[92m'
    SERM = '\033[35m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
    def disable(self):
        self.OKGREEN = ''
        CRM = ''
        RO = ''
        OF = ''
        SERM = ''
        self.FAIL = ''
        self.ENDC = ''


class ResourceParser(object):
        
    def __init__(self, from_file=None, from_string=None): 

        self.__ro_ad_parser = ROv3AdvertisementParser(from_file, from_string)
        self.__com_ad_parser = CRMv3AdvertisementParser(from_file, from_string)
        self.__of_ad_parser = OFv3AdvertisementParser(from_file, from_string)
        self.__se_ad_parser = SERMv3AdvertisementParser(from_file, from_string)
        #self.__tn_ad_parser = TNRMv3AdvertisementParser(from_file, from_string)

        self.__ro_ma_parser = ROManifestParser(from_file, from_string)
        self.__com_ma_parser = CRMv3ManifestParser(from_file, from_string)
        self.__of_ma_parser = OFv3ManifestParser(from_file, from_string)
        self.__se_ma_parser = SERMv3ManifestParser(from_file, from_string)
        #self.__tn_ma_parser = TNRMv3ManifestParser(from_file, from_string)


        if from_file is not None: 
            self.resources_xml = etree.parse(from_file).getroot() 
        elif from_string is not None: 
            self.resources_xml = etree.fromstring(from_string) 
        else:
            self.raise_exception("Resources not received")

    def element_to_string(self):
        return etree.tostring(self.resources_xml)          
 
    def get_resources_xml(self): 
        return self.resources_xml 
 
    def get_serm_advertisement(self, resources_xml):
        print "get_SERM_advertisement", self.resources_xml
        return self.__se_ad_parser() 

    def get_serm_manifest(self, resources_xml):
        return self.__se_ma_parser()

    def get_ro_advertisement(self):
        print "get_RO_advertisement", self.resources_xml
        resources_string = self.element_to_string()
        return self.__ro_ad_parser(from_string=resources_string)
    
    def get_ro_manifest(self, resources_xml):
        return self.__ro_ma_parser()

    def get_of_advertisement(self, resources_xml):
        print "get_OF_advertisement", self.resources_xml
        return self.__of_ad_parser(from_string=self.resources_xml)
 
    def get_of_manifest(self, resources_xml):
        return self.__of_ma_parser()

    def get_crm_advertisement(self):
        print "get_CRM_advertisement", self.resources_xml
        resources_string = self.element_to_string()
#        return self.__com_ad_parser(from_string=self.resources_xml)
        return CRMv3ManifestParser(from_string=resources_string)

    def get_crm_manifest(self, resources_xml):
        return self.__com_ma_parser()

    def get_tn_advertisement(self, resources_xml):
        #print "get_TN_advertisement", self.resources_xml
        #return self.__tn_ad_parser(from_string=self.resources_xml)
        pass

    def get_tn_manifest(self, resources_xml):
        #return self.__tn_ma_parser()
        pass

    def raise_exception(self, msg): 
        raise Exception("[ListResources-Parser] %s" % (msg,)) 
  
    def __repr__(self): 
        return etree.tostring(self.resources_xml, pretty_print=True) 







#############################  

if __name__ == "__main__":

    from lxml import etree    

    html = etree.Element("html")
    body = etree.SubElement(html, "body")
    body.text = "TEXT"
        
    br = etree.SubElement(body, "br")

    br.tail = "TAIL"
    
#    res = ResourceParser(None, etree.tostring(html))
#    res = ResourceParser(from_string = etree.tostring(html))

    f = open("values.xml", "r+")
    data = f.read()
#    print "data \n", data
   
#    print "Type", type(data)

    tree = etree.ElementTree(etree.fromstring(data))
#    print tree
#    etree.dump(tree)

    res_instance = ResourceParser(from_string=etree.tostring(tree))    
#    res_instance = ResourceParser(from_file = etree.tostring(tree))

    crm = res_instance.get_crm_advertisement()
    print "RESULT: \n", mcolors.CRM+str(crm)+mcolors.ENDC

    ro = res_instance.get_ro_advertisement()
    print "RESULT: \n", mcolors.RO+str(ro)+mcolors.ENDC
    
#    getted = res_instance.get_resources_xml()
#    print getted

    print mcolors.OKGREEN+"OK"+mcolors.ENDC
