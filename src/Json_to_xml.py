import json
import xml.etree.ElementTree as ET

def json_to_xml_element(json_obj, root_tag):
    # Create the root element
    root = ET.Element(root_tag)

    def build_element(parent, key, value):
        if isinstance(value, dict):
            # Recursively build the XML tree for dictionaries
            elem = ET.SubElement(parent, key)
            for sub_key, sub_value in value.items():
                build_element(elem, sub_key.replace(" ", "_"), sub_value)
        elif isinstance(value, list):
            for item in value:
                build_element(parent, "item", item)
        else:
            if isinstance(value, bool):
                value = str(value).lower()  # Convert boolean to lowercase string
            elif isinstance(value, int) or isinstance(value, float):
                value = str(value)
            
            parent.set(key.replace(" ", "_"), value)

    # Build the XML structure starting from the root element
    for key, value in json_obj.items():
        build_element(root, key.replace(" ", "_"), value)
    
    return root

def json_file_to_xml(json_data, output_xml_file, root_tag="root"):
    # Convert JSON to XML
    xml_root = json_to_xml_element(json_data, root_tag)

    # Create an ElementTree object from the XML root
    tree = ET.ElementTree(xml_root)

    # Write the XML tree to the output file
    tree.write(output_xml_file, encoding="utf-8", xml_declaration=True)

with open("../data/Rules.json", 'r') as file:
    rules_json = json.load(file)
# Output XML file path
output_xml_file = "output.xml"

# Convert JSON to XML and save it to a file
json_file_to_xml(rules_json, output_xml_file, root_tag="root")

print(f"XML file saved as {output_xml_file}")
