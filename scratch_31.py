from xml.dom import minidom

xml_file = '/home/kpit/Downloads/upload.xml'
# docs = xml.dom.minidom.parse(xml_file)
#
# xml_str = docs.toprettyxml(indent='\t')
#
# with open("file.xml", "w") as file_obj:
#     file_obj.write(xml_str)

parent_node_attrs = {'xmlns:ns1': 'http://schema.ibm.com/vega/2008/',
                     'xmlns:ns10': 'http://open-services.net/ns/core#',
                     'xmlns:ns11': 'http://open-services.net/ns/qm#',
                     'xmlns:ns12': 'http://jazz.net/xmlns/prod/jazz/rqm/process/1.0/',
                     'xmlns:ns13': 'http://www.w3.org/2002/07/owl#',
                     'xmlns:ns14': 'http://jazz.net/xmlns/alm/qm/qmadapter/v0.1',
                     'xmlns:ns15': 'http://jazz.net/xmlns/alm/qm/qmadapter/task/v0.1',
                     'xmlns:ns16': 'http://jazz.net/xmlns/alm/qm/v0.1/executionresult/v0.1',
                     'xmlns:ns17': 'http://jazz.net/xmlns/alm/qm/v0.1/catalog/v0.1',
                     'xmlns:ns18': 'http://jazz.net/xmlns/alm/qm/v0.1/tsl/v0.1/',
                     'xmlns:ns2': 'http://jazz.net/xmlns/alm/qm/v0.1/',
                     'xmlns:ns20': 'http://jazz.net/xmlns/alm/qm/styleinfo/v0.1/',
                     'xmlns:ns21': 'http://www.w3.org/1999/XSL/Transform',
                     'xmlns:ns3': 'http://purl.org/dc/elements/1.1/',
                     'xmlns:ns4': 'http://jazz.net/xmlns/prod/jazz/process/0.6/',
                     'xmlns:ns5': 'http://jazz.net/xmlns/alm/v0.1/',
                     'xmlns:ns6': 'http://purl.org/dc/terms/',
                     'xmlns:ns7': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                     'xmlns:ns8': 'http://jazz.net/xmlns/alm/qm/v0.1/testscript/v0.1/',
                     'xmlns:ns9': 'http://jazz.net/xmlns/alm/qm/v0.1/executionworkitem/v0.1'}


# root = minidom.Document()
# # Creating the root element
# xml = root.createElement("ns2:executionresult")
# # Adding attributes
# for key in parent_node_attrs.keys():
#     xml.setAttribute(key, parent_node_attrs[key])
#
# # Creating the projectArea element
# project_area = root.createElement("ns2:projectArea")
# # Adding attributes
# project_area.setAttribute("alias", "Sandpit+%28Quality+Management%29")
# project_area.setAttribute(
#     "href",
#     "https://ktblrhonda02.kpit.com:9443/qm/resource/itemOid/com.ibm.team.process.ProjectArea/_MPBWQaxIEeih48gIzz96_w")
#
# # Appending to parent element
# xml.appendChild(project_area)
#
# # Creating the ns2:webId element
# web_id = root.createElement("ns2:webId")
# # Creating the text value for ns2:webId element
# web_id_text = root.createTextNode("1")
# # appending text value to the element
# web_id.appendChild(web_id_text)
#
# # Appending to parent element
# xml.appendChild(web_id)
#
#
#
#
# # Appending to doc element
# root.appendChild(xml)
#
# xml_str = root.toprettyxml(indent='\t')
#
# with open("node.xml", "w") as file_obj:
#     file_obj.write(xml_str)


class CreateXML(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.document = minidom.Document()
        self.root = self.document.createElement(
            self.kwargs.get("parent_node"))

    def set_parent_attributes(self, **attrs):
        for attr in attrs.keys():
            self.root.setAttribute(attr, attrs[attr])
        return self.root

    def create_node(self, node_name, parent_node):
        node = self.document.createElement(node_name)
        parent_node.appendChild(node)
        return parent_node

    def create_parent_node(self, node_name, **attrs):
        node = self.document.createElement(node_name)
        for attr in attrs.keys():
            node.setAttribute(attr, attrs[attr])
        return node

    def create_node_under_parent(self, node_name, parent, **attrs):
        node = self.create_parent_node(node_name, **attrs)
        parent.appendChild(node)
        return parent

    def create_text_node(self, node_name, parent, text):
        node = self.document.createElement(node_name)
        text_node = self.document.createTextNode(text)
        node.appendChild(text_node)
        parent.appendChild(node)
        return parent

    def create_nested_node(self, nested_node, parent, nodes):
        nested = self.document.createElement(nested_node)
        for node_name in nodes:
            for node_info in node_name:
                node = self.document.createElement(node_info)
                for sub_node in node_name[node_info]:
                    if sub_node != "children":
                        node.setAttribute(sub_node, node_name[node_info][sub_node])
                    elif sub_node == "children":
                        for child in node_name[node_info][sub_node]:
                            for key in child:
                                child_node = self.document.createElement(key)
                                child_text_node = self.document.createTextNode(child[key])
                                child_node.appendChild(child_text_node)
                                node.appendChild(child_node)
                nested.appendChild(node)
        parent.appendChild(nested)
        return parent

    def close_document(self):
        self.document.appendChild(self.root)
        return self.document


custom_attr = [
    {
        "ns2.customAttribute": {
            "type": "SMALL_STRING",
            "required": "false",
            "children": [
                {
                    "ns2:name": "Description"
                },
                {
                    "ns2:value": ""
                },
                {
                    "ns2:name": "Resultpath"
                },
                {
                    "ns2:value": "Resultpath"
                },
            ]
        }
    }
]

create_xml_doc = CreateXML(parent_node="ns2:executionresult")
updated_node = create_xml_doc.set_parent_attributes(**parent_node_attrs)
updated_node = create_xml_doc.create_node_under_parent(
    "ns2:projectArea",
    updated_node,
    alias="Sandpit+%28Quality+Management%29",
    href="https://ktblrhonda02.kpit.com:9443/qm/resource/itemOid/com.ibm.team.process.ProjectArea/_MPBWQaxIEeih48gIzz96_w"
)
updated_node = create_xml_doc.create_text_node("ns2:webId", updated_node, "1")
updated_node = create_xml_doc.create_text_node("ns3:title", updated_node, "Chnaged to failed")
updated_node = create_xml_doc.create_node("ns2:variables", updated_node)
updated_node = create_xml_doc.create_text_node("ns16:weight", updated_node, "200")
updated_node = create_xml_doc.create_text_node("ns5:owner", updated_node, "harshap")
updated_node = create_xml_doc.create_text_node("ns2:locked", updated_node, "false")
updated_node = create_xml_doc.create_text_node("ns5:state", updated_node, "com.ibm.rqm.execution.common.state.error")
updated_node = create_xml_doc.create_node_under_parent(
    "ns5:state",
    updated_node,
    href='https://ktblrhonda02.kpit.com:9443/qm/service/com.ibm.rqm.integration.service.IIntegrationService/resources/Sandpit+%28Quality+Management%29/testcase/3f23801e-a8d4-4890-aaed-14eb5e0740b7')
updated_node = create_xml_doc.create_nested_node("ns2:customAttributes", updated_node, custom_attr)
updated_node = create_xml_doc.create_node_under_parent(
    "ns2:testplan",
    updated_node,
    href='https://ktblrhonda02.kpit.com:9443/qm/service/com.ibm.rqm.integration.service.IIntegrationService/resources/Sandpit+%28Quality+Management%29/testplan/14940e39-1805-4ae0-bd16-1f9568a8c2e0')
updated_node = create_xml_doc.create_node_under_parent(
    "ns2:executionworkitem",
    updated_node,
    href="https://ktblrhonda02.kpit.com:9443/qm/service/com.ibm.rqm.integration.service.IIntegrationService/resources/Sandpit+%28Quality+Management%29/executionworkitem/6b743b99-36e0-4ea7-b9b5-8cb2ef4bcdae"
)

root = create_xml_doc.close_document()
xml_str = root.toprettyxml(indent='\t')

with open("node.xml", "w") as file_obj:
    file_obj.write(xml_str)
