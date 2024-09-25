from lxml import etree

class XMl_validator:
    def __init__(self,XML_File_path, XSD_File_path):
        print()
        self.XML_File_path = XML_File_path
        self.XSD_File_path = XSD_File_path
        self.load_xml_Xsd_using_path()
    
    def load_xml_Xsd_using_path(self):
        # Load XSD Schema
        with open(self.XSD_File_path, "rb") as schema_file:
            schema_root = etree.XML(schema_file.read())
            self.Xsd_schema = etree.XMLSchema(schema_root)

        # Load XML
        with open(self.XML_File_path, "rb") as xml_file:
            self.Xml_root = etree.XML(xml_file.read())

    def validate_XML(self):
        # Validate XML with error handling
        try:
            self.Xsd_schema.assertValid(self.Xml_root)
            print("XML is valid against the XSD.")
            return True
        except etree.DocumentInvalid as e:
            print(f"XML is invalid: {e}")
            return False

