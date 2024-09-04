import xml.etree.ElementTree as ET
from Rule_model import Rule, Rule_Connection


def parse_nested_rule(element):
    # print("The Element is :",element.find('Reference_field').text)
    # print("Flow for true ->> ",element.find('Flow_for_True').text)
    """Recursive function to parse nested rules in the XML."""
    # Extracting necessary attributes
    reference_field = element.find('Reference_field').text
    rule_operator = element.find('Rule_Operator').text.strip()
    rule_value = element.find('Rule_Value').text
    flow_for_true = element.find('Flow_for_True').text == "true"
    flow_for_false = element.find('Flow_for_False').text == "true"
    logical_operator = element.find('logical_operator').text if element.find('logical_operator') is not None else None

    nested_rule_element = element.find('Nested_Rule')
    nested_rule = parse_nested_rule(nested_rule_element) if nested_rule_element is not None else None
    
    logical_rule_element = element.find('Logical_Rule')
    logical_rule = parse_nested_rule(logical_rule_element) if logical_rule_element is not None else None

    # Creating and returning Rule object
    return Rule(
        ID=element.tag,
        Rule_header=reference_field,
        Rule_operator=rule_operator,
        Rule_value=rule_value,
        Is_Nested=nested_rule is not None,
        Nested_Rule=nested_rule,
        Flow_for_True=flow_for_true,
        Flow_for_False=flow_for_false,
        logical_operator=logical_operator,
        Logical_Rule=logical_rule
    )


class RulesUsingXML:
    def __init__(self, xml_file_name):
        # Create a dictionary to hold the lenders and their associated rules
        self.lender_rules = {}
        # Load the XML file
        tree = ET.parse(xml_file_name)
        self.root = tree.getroot()

    def create_rules_using_xml(self):
        # Iterate over the lenders in the XML file
        for lender in self.root.find('Lenders'):
            lender_name = lender.tag
            connections = None

            # Create Rule objects and connect them
            for rule_element in reversed(list(lender)):
                rule = parse_nested_rule(rule_element)
                connections = Rule_Connection(ID=rule_element.tag, Rule=rule, next_Rule=connections)

            # Store the connected rules for the lender
            self.lender_rules[lender_name] = connections

# Example Usage:

# xml_file = 'rules.xml'  # Path to your XML file
# rules_from_xml = RulesUsingXML(xml_file)
# rules_from_xml.create_rules_using_xml()

# # Accessing the rules for a particular lender:
# for lender_name, rule_connection in rules_from_xml.lender_rules.items():
#     print(f"Lender: {lender_name}")
#     temp = rule_connection
#     while temp is not None:
#         print(temp.Rule)
#         temp = temp.next_Rule
