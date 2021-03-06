#from rspecs.commons import DEFAULT_XMLNS, DEFAULT_XS, DEFAULT_SCHEMA_LOCATION,\
#    DSL_PREFIX
#from rspecs.commons_of import DEFAULT_OPENFLOW
#from rspecs.formatter_base import FormatterBase
from parsers.commons import DEFAULT_XMLNS, DEFAULT_XS, DEFAULT_SCHEMA_LOCATION,\
    DSL_PREFIX
from parsers.commons_of import DEFAULT_OPENFLOW
from parsers.formatter_base import FormatterBase

from lxml import etree

DEFAULT_REQ_SCHEMA_LOCATION = DEFAULT_SCHEMA_LOCATION
DEFAULT_REQ_SCHEMA_LOCATION += DSL_PREFIX + "3/request.xsd "
DEFAULT_REQ_SCHEMA_LOCATION += DSL_PREFIX + "ext/openflow/3/of-resv.xsd"


class OFv3RequestFormatter(FormatterBase):
    def __init__(self, xmlns=DEFAULT_XMLNS, xs=DEFAULT_XS,
                 openflow=DEFAULT_OPENFLOW,
                 schema_location=DEFAULT_REQ_SCHEMA_LOCATION):
        super(OFv3RequestFormatter, self).__init__(
            "request", schema_location, {"openflow": "%s" % (openflow)},
            xmlns, xs)
        self.__of = openflow

    def sliver(self, description=None, ref=None, email=None):
        s = etree.SubElement(self.rspec, "{%s}sliver" % (self.__of))
        if description is not None:
            s.attrib["description"] = description
        if ref is not None:
            s.attrib["ref"] = ref
        if email is not None:
            s.attrib["email"] = email

    def controller(self, url, type):
        s = self.__find_sliver()
        c = etree.SubElement(s, "{%s}controller" % (self.__of))
        c.attrib["url"] = url
        c.attrib["type"] = type

    def group(self, name):
        s = self.__find_sliver()
        g = etree.SubElement(s, "{%s}group" % (self.__of))
        g.attrib["name"] = name

    def group_datapath(self, gname, dpid):
        g = self.__find_group(gname)
        self.__datapath(g,
                        dpid.get('component_id'),
                        dpid.get('component_manager_id'),
                        dpid.get('dpid'),
                        dpid.get('ports'))

    def match(self, mtc):
        s = self.__find_sliver()
        match = etree.SubElement(s, "{%s}match" % (self.__of))

        for ug in mtc.get('use_groups'):
            use_group = etree.SubElement(match, "{%s}use-group" % (self.__of))
            use_group.attrib["name"] = ug.get("name")

        for dp in mtc.get('dpids'):
            self.__datapath(match,
                            dp.get('component_id'),
                            dp.get('component_manager_id'),
                            dp.get('dpid'),
                            dp.get('ports'))

        if mtc.get('packet') is not None:
            packet = etree.SubElement(match, "{%s}packet" % (self.__of))
            self.__packet_sub_elem(packet, mtc.get('packet'), 'dl_src')
            self.__packet_sub_elem(packet, mtc.get('packet'), 'dl_dst')
            self.__packet_sub_elem(packet, mtc.get('packet'), 'dl_type')
            self.__packet_sub_elem(packet, mtc.get('packet'), 'dl_vlan')
            self.__packet_sub_elem(packet, mtc.get('packet'), 'nw_src')
            self.__packet_sub_elem(packet, mtc.get('packet'), 'nw_dst')
            self.__packet_sub_elem(packet, mtc.get('packet'), 'nw_proto')
            self.__packet_sub_elem(packet, mtc.get('packet'), 'tp_src')
            self.__packet_sub_elem(packet, mtc.get('packet'), 'tp_dst')

    def __find_sliver(self):
        s = self.rspec.find("{%s}sliver" % (self.__of))
        if s is None:
            self.raise_exception("Sliver tag not found!")
        return s

    def __find_group(self, name):
        for g in self.rspec.findall(".//{%s}group" % (self.__of)):
            if g.get("name") == name:
                return g
        self.raise_exception("Group %s not found!" % (name))

    def __datapath(self, element, component_id, component_manager_id,
                   dpid, ports):
        datapath = etree.SubElement(element, "{%s}datapath" % (self.__of))
        datapath.attrib["component_id"] = component_id
        datapath.attrib["component_manager_id"] = component_manager_id
        datapath.attrib["dpid"] = dpid

        for p in ports:
            port = etree.SubElement(datapath, "{%s}port" % (self.__of))
            port.attrib["num"] = p.get("num")
            if p.get("name") is not None:
                port.attrib["name"] = p.get("name")

    def __packet_sub_elem(self, element, data, tag):
        if data.get(tag) is not None:
            v = etree.SubElement(element, "{%s}%s" % (self.__of, tag))
            v.attrib["value"] = data.get(tag)
