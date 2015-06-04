from resource_orchestrator.utils.parsers.parser_base import ParserBase
from resource_orchestrator.utils.parsers.crm.advertisement_parser import CRMv3AdvertisementParser
from resource_orchestrator.utils.parsers.crm.manifest_parser import CRMv3ManifestParser

from resource_orchestrator.utils.parsers.openflow.advertisement_parser import OFv3AdvertisementParser
from resource_orchestrator.utils.parsers.openflow.manifest_parser import OFv3ManifestParser

from resource_orchestrator.utils.parsers.ro.advertisement_parser import ROv3AdvertisementParser
from resource_orchestrator.utils.parsers.ro.manifest_parser import ROManifestParser

from resource_orchestrator.utils.parsers.serm.advertisement_parser import SERMv3AdvertisementParser
from resource_orchestrator.utils.parsers.serm.manifest_parser import SERMv3ManifestParser


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

        if from_file is not None: 
            self.resources_xml = etree.parse(from_file).getroot() 
        elif from_string is not None: 
            #self.resources_xml = etree.fromstring(from_string)
            self.resources_xml = from_string 
        else:
            self.raise_exception("Resources not received")

    def element_to_string(self):
        #return etree.tostring(self.resources_xml)          
        return self.resources_xml 

    def get_resources_xml(self): 
        return self.resources_xml 
 
    def get_serm_advertisement(self, resources_xml):
        print "get_SERM_advertisement", self.resources_xml
        return self.__se_ad_parser() 

    def get_serm_manifest(self, resources_xml):
        return self.__se_ma_parser()

    def get_ro_advertisement(self):
        #print "get_RO_advertisement", self.resources_xml
        #resources_string = self.element_to_string()
        #ro = ROv3AdvertisementParser(from_string=resources_string)
        ro = ROv3AdvertisementParser(from_string=self.resources_xml)    
        print "RO > COM-nodes: ", ro.com_nodes()
        print "RO > COM-links: ", ro.com_links()
        print "RO > SDN-nodes: ", ro.sdn_nodes()
        print "RO > SDN-links: ", ro.sdn_links()

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
        return CRMv3AdvertisementParser(from_string=resources_string)

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

    source = """<?xml version="1.0" encoding="UTF-8" ?>
<data>
   <rspec xmlns:openflow="http://www.geni.net/resources/rspec/ext/openflow/3" xmlns:protogeni="http://www.protogeni.net/resources/rspec/0.1" xmlns:sharedvlan="http://www.geni.net/resources/rspec/ext/shared-vlan/1" xmlns:xs="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.geni.net/resources/rspec/3" xs:schemaLocation="http://www.geni.net/resources/rspec/3/ad.xsd" type="advertisement">
    <node component_manager_id="urn:publicid:IDN+ocf:i2cat:vtam+authority+cm" component_name="urn:publicid:IDN+ocf:i2cat:vtam+node+Rodoreda" component_id="urn:publicid:IDN+ocf:i2cat:vtam+node+Rodoreda" exclusive="false" protogeni:component_manager_uuid="felix:CRM">
      <available now="true"/>
    </node>
    <node component_manager_id="urn:publicid:IDN+ocf:i2cat:vtam+authority+cm" component_name="urn:publicid:IDN+ocf:i2cat:vtam+node+March" component_id="urn:publicid:IDN+ocf:i2cat:vtam+node+March" exclusive="false" protogeni:component_manager_uuid="felix:CRM">
      <available now="true"/>
    </node>
    <node component_manager_id="urn:publicid:IDN+ocf:i2cat:vtam+authority+cm" component_name="urn:publicid:IDN+ocf:i2cat:vtam+node+Verdaguer" component_id="urn:publicid:IDN+ocf:i2cat:vtam+node+Verdaguer" exclusive="false" protogeni:component_manager_uuid="felix:CRM">
      <available now="true"/>
    </node>
    <node component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0" component_manager_id="urn:publicid:IDN+fms:i2cat:serm+authority+cm" exclusive="false" protogeni:component_manager_uuid="felix:SERM">
      <interface component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_21"/>
      <interface component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_1"/>
      <interface component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_3"/>
      <interface component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_2"/>
      <interface component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_5"/>
      <interface component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_4"/>
    </node>
    <link component_id="urn:publicid:IDN+ocf:i2cat:vtam:Rodoreda+link+eth1-00:10:00:00:00:00:00:03_12" component_name="urn:publicid:IDN+ocf:i2cat:vtam:Rodoreda+link+eth1-00:10:00:00:00:00:00:03_12" protogeni:component_manager_uuid="felix:CRM">
      <property source_id="urn:publicid:IDN+ocf:i2cat:vtam+node+Rodoreda+interface+eth1" dest_id="urn:publicid:IDN+openflow:ocf:i2cat:ofam+datapath+00:10:00:00:00:00:00:03" capacity="1024MB/s"/>
      <link_type name="L2 Link"/>
    </link>
    <link component_id="urn:publicid:IDN+ocf:i2cat:vtam:Rodoreda+link+eth2-00:10:00:00:00:00:00:05_12" component_name="urn:publicid:IDN+ocf:i2cat:vtam:Rodoreda+link+eth2-00:10:00:00:00:00:00:05_12" protogeni:component_manager_uuid="felix:CRM">
      <property source_id="urn:publicid:IDN+ocf:i2cat:vtam+node+Rodoreda+interface+eth2" dest_id="urn:publicid:IDN+openflow:ocf:i2cat:ofam+datapath+00:10:00:00:00:00:00:05" capacity="1024MB/s"/>
      <link_type name="L2 Link"/>
    </link>
    <link component_id="urn:publicid:IDN+ocf:i2cat:vtam:March+link+eth1-00:10:00:00:00:00:00:04_12" component_name="urn:publicid:IDN+ocf:i2cat:vtam:March+link+eth1-00:10:00:00:00:00:00:04_12" protogeni:component_manager_uuid="felix:CRM">
      <property source_id="urn:publicid:IDN+ocf:i2cat:vtam+node+March+interface+eth1" dest_id="urn:publicid:IDN+openflow:ocf:i2cat:ofam+datapath+00:10:00:00:00:00:00:04" capacity="1024MB/s"/>
      <link_type name="L2 Link"/>
    </link>
    <link component_id="urn:publicid:IDN+ocf:i2cat:vtam:March+link+eth2-00:10:00:00:00:00:00:05_11" component_name="urn:publicid:IDN+ocf:i2cat:vtam:March+link+eth2-00:10:00:00:00:00:00:05_11" protogeni:component_manager_uuid="felix:CRM">
      <property source_id="urn:publicid:IDN+ocf:i2cat:vtam+node+March+interface+eth2" dest_id="urn:publicid:IDN+openflow:ocf:i2cat:ofam+datapath+00:10:00:00:00:00:00:05" capacity="1024MB/s"/>
      <link_type name="L2 Link"/>
    </link>
    <link component_id="urn:publicid:IDN+ocf:i2cat:vtam:Verdaguer+link+eth1-00:10:00:00:00:00:00:01_12" component_name="urn:publicid:IDN+ocf:i2cat:vtam:Verdaguer+link+eth1-00:10:00:00:00:00:00:01_12" protogeni:component_manager_uuid="felix:CRM">
      <property source_id="urn:publicid:IDN+ocf:i2cat:vtam+node+Verdaguer+interface+eth1" dest_id="urn:publicid:IDN+openflow:ocf:i2cat:ofam+datapath+00:10:00:00:00:00:00:01" capacity="1024MB/s"/>
      <link_type name="L2 Link"/>
    </link>
    <link component_id="urn:publicid:IDN+ocf:i2cat:vtam:Verdaguer+link+eth2-00:10:00:00:00:00:00:02_12" component_name="urn:publicid:IDN+ocf:i2cat:vtam:Verdaguer+link+eth2-00:10:00:00:00:00:00:02_12" protogeni:component_manager_uuid="felix:CRM">
      <property source_id="urn:publicid:IDN+ocf:i2cat:vtam+node+Verdaguer+interface+eth2" dest_id="urn:publicid:IDN+openflow:ocf:i2cat:ofam+datapath+00:10:00:00:00:00:00:02" capacity="1024MB/s"/>
      <link_type name="L2 Link"/>
    </link>
    <link component_id="urn:publicid:IDN+fms:i2cat:serm:link" protogeni:component_manager_uuid="felix:SERM">
      <component_manager name="urn:publicid:IDN+fms:i2cat:serm+authority+cm"/>
      <link_type name="urn:felix"/>
      <interface_ref component_id="*"/>
      <interface_ref component_id="*"/>
      <property source_id="*" dest_id="*" capacity="1G"/>
    </link>
    <link component_id="urn:publicid:IDN+fms:i2cat:serm+link+10:00:78:ac:c0:15:19:c0_1_00:10:00:00:00:00:00:01_6" protogeni:component_manager_uuid="felix:SERM">
      <link_type name="urn:felix+static_link"/>
      <interface_ref component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_1"/>
      <interface_ref component_id="urn:publicid:IDN+openflow:ocf:i2cat:ofam+datapath+00:10:00:00:00:00:00:01_6"/>
    </link>
    <link component_id="urn:publicid:IDN+fms:i2cat:serm+link+10:00:78:ac:c0:15:19:c0_3_00:10:00:00:00:00:00:03_6" protogeni:component_manager_uuid="felix:SERM">
      <link_type name="urn:felix+static_link"/>
      <interface_ref component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_3"/>
      <interface_ref component_id="urn:publicid:IDN+openflow:ocf:i2cat:ofam+datapath+00:10:00:00:00:00:00:03_6"/>
    </link>
    <link component_id="urn:publicid:IDN+fms:i2cat:serm+link+10:00:78:ac:c0:15:19:c0_2_00:10:00:00:00:00:00:02_6" protogeni:component_manager_uuid="felix:SERM">
      <link_type name="urn:felix+static_link"/>
      <interface_ref component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_2"/>
      <interface_ref component_id="urn:publicid:IDN+openflow:ocf:i2cat:ofam+datapath+00:10:00:00:00:00:00:02_6"/>
    </link>
    <link component_id="urn:publicid:IDN+fms:i2cat:serm+link+10:00:78:ac:c0:15:19:c0_5_00:10:00:00:00:00:00:05_6" protogeni:component_manager_uuid="felix:SERM">
      <link_type name="urn:felix+static_link"/>
      <interface_ref component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_5"/>
      <interface_ref component_id="urn:publicid:IDN+openflow:ocf:i2cat:ofam+datapath+00:10:00:00:00:00:00:05_6"/>
    </link>
    <link component_id="urn:publicid:IDN+fms:i2cat:serm+link+10:00:78:ac:c0:15:19:c0_21_00:00:54:e0:32:cc:a4:c0_24" protogeni:component_manager_uuid="felix:SERM">
      <link_type name="urn:felix+vlan_trans"/>
      <interface_ref component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_21"/>
      <interface_ref component_id="urn:publicid:IDN+fms:i2cat:tnrm+stp+urn:publicid:IDN+fms:psnc:serm+datapath+00:00:54:e0:32:cc:a4:c0_24"/>
    </link>
    <link component_id="urn:publicid:IDN+fms:i2cat:serm+link+10:00:78:ac:c0:15:19:c0_4_00:10:00:00:00:00:00:04_6" protogeni:component_manager_uuid="felix:SERM">
      <link_type name="urn:felix+static_link"/>
      <interface_ref component_id="urn:publicid:IDN+fms:i2cat:serm+datapath+10:00:78:ac:c0:15:19:c0_4"/>
      <interface_ref component_id="urn:publicid:IDN+openflow:ocf:i2cat:ofam+datapath+00:10:00:00:00:00:00:04_6"/>
    </link>
  </rspec>  
</data>"""


#    res_instance = ResourceParser(from_string=etree.tostring(tree))    
#    res_instance = ResourceParser(from_file = etree.tostring(tree))
    res_instance = ResourceParser(from_string=source) 

    ro = res_instance.get_ro_advertisement()
    print "RESULT: \n", mcolors.RO+str(ro)+mcolors.ENDC
    
#    getted = res_instance.get_resources_xml()
#    print getted

    print mcolors.OKGREEN+"OK"+mcolors.ENDC
