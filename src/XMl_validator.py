# Importing necessary modules
from lxml import etree

class XMl_validator:
    """
        A class to validate an XML file against an XSD schema using lxml.

        Attributes:
            XML_File_path (str): Path to the XML file.
            XSD_File_path (str): Path to the XSD file.
            Xsd_schema (etree.XMLSchema): The compiled XSD schema for validation.
            Xml_root (etree.Element): The parsed root element of the XML file.
    """
    def __init__(self,XML_File_path, XSD_File_path):
        """
            Initializes the XML_validator class with paths to the XML and XSD files.
            Loads and parses both files for validation.

            Args:
                XML_File_path (str): Path to the XML file.
                XSD_File_path (str): Path to the XSD file.
        """
        self.XML_File_path = XML_File_path
        self.XSD_File_path = XSD_File_path
        self.load_xml_Xsd_using_path()
    
    def load_xml_Xsd_using_path(self):
        """
            Loads the XML and XSD files from their respective paths.
            Compiles the XSD schema and parses the XML document.
        """
        with open(self.XSD_File_path, "rb") as schema_file:
            schema_root = etree.XML(schema_file.read())
            self.Xsd_schema = etree.XMLSchema(schema_root)

        # Load XML
        with open(self.XML_File_path, "rb") as xml_file:
            self.Xml_root = etree.XML(xml_file.read())

    def validate_XML(self):
        """
            Validates the loaded XML document against the compiled XSD schema.

            Returns:
                bool: True if the XML is valid, False otherwise.
        """
        try:
            self.Xsd_schema.assertValid(self.Xml_root)
            print("XML is valid against the XSD.")
            return True
        except etree.DocumentInvalid as e:
            print(f"XML is invalid: {e}")
            return False

