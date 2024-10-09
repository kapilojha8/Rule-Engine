import xml.etree.ElementTree as ET
from XMl_validator import XMl_validator
from Rule_model import Rule, Rule_Connection, Flow_exception


def parse_nested_rule(Rule_element):
    """Recursive function to parse nested rules in the XML."""
    # Extracting necessary attributes
    Flow_exception_True_Flow_rule, Flow_exception_True_Condition_to_proceed,Flow_exception_True_Remark,Flow_exception_False_Flow_rule, Flow_exception_False_Condition_to_proceed,Flow_exception_False_Remark = None, None, None, None, None, None
    if Rule_element.find("Flow_for_True_eval") is not None:
        Flow_Exception_for_True = Rule_element.find("Flow_for_True_eval")
        if Flow_Exception_for_True.find('Exception_rule'):
            Flow_exception_True_Flow_rule = Flow_Exception_for_True.find('Exception_rule')
        if Flow_Exception_for_True.attrib.get('Condition_to_proceed'): 
            Flow_exception_True_Condition_to_proceed = Flow_Exception_for_True.attrib.get('Condition_to_proceed')
        if Flow_Exception_for_True.attrib.get('Remark'): 
            Flow_exception_True_Remark = Flow_Exception_for_True.attrib.get('Remark')

    if Rule_element.find("Flow_for_False_eval")is not None:
        Flow_Exception_for_False = Rule_element.find("Flow_for_False_eval")
        if Flow_Exception_for_False.find('Exception_rule'):
            Flow_exception_False_Flow_rule = Flow_Exception_for_False.find('Exception_rule')
        if Flow_Exception_for_False.attrib.get('Condition_to_proceed'): 
            Flow_exception_False_Condition_to_proceed = Flow_Exception_for_False.attrib.get('Condition_to_proceed')
        if Flow_Exception_for_False.attrib.get('Remark'): 
            Flow_exception_False_Remark = Flow_Exception_for_False.attrib.get('Remark')
    
    return Rule(
                ID=Rule_element.tag,
                Rule_header    =  Rule_element.attrib['reference_field'],
                Rule_operator  =  Rule_element.attrib['rule_Operator'],
                Rule_value     =  Rule_element.attrib['rule_Value'],
                Field_Type     =  Rule_element.attrib.get('field_Type'),
                Is_Evaluating  =  Rule_element.attrib.get('Is_Evaluating', True),
                Flow_exception_True = Flow_exception(
                   Exception_rule =  parse_nested_rule(Flow_exception_True_Flow_rule) if Flow_exception_True_Flow_rule else None,
                   Condition_to_proceed =  bool(True) if Flow_exception_True_Condition_to_proceed == "true" else False,
                   Remark = Flow_exception_True_Remark if Flow_exception_True_Remark else ""
                  ),
                Flow_exception_False = Flow_exception(
                   Exception_rule =  parse_nested_rule(Flow_exception_False_Flow_rule) if Flow_exception_False_Flow_rule else None,
                   Condition_to_proceed = bool(False) if Flow_exception_False_Condition_to_proceed == "false" else True,
                   Remark = Flow_exception_False_Remark if Flow_exception_False_Remark else ""
                  ),
                
                logical_operator = Rule_element.attrib.get('logical_operator', None),
                Logical_Rule   =   parse_nested_rule(Rule_element.find('Logical_Rule')) if Rule_element.find('Logical_Rule') is not None else None,
        )

class RulesUsingXML:
    def __init__(self, xml_file_name, xsd_file_name):
        # Create a dictionary to hold the lenders and their associated rules
        xml_validator =  XMl_validator(XML_File_path=xml_file_name, XSD_File_path=xsd_file_name)
        if not xml_validator.validate_XML():
            return False
        self.lender_rules = {}
        # Load the XML file
        tree = ET.parse(xml_file_name)
        self.root = tree.getroot()
        print(self.root)

    def create_rules_using_xml(self):
        # Iterate over the lenders in the XML file
        Dict = {}
        for lender in self.root.find('Lenders'):
            lender_name = lender.attrib['name']
            Dict[lender_name] = {}
            for plans in lender:
                plan_name = plans.attrib['name']
                Dict[lender_name][plan_name] = {} 
                connections = None
                for rules in  reversed(list(plans)):
                    rule = parse_nested_rule(rules)
                    connections = Rule_Connection(ID=rules.attrib['name'], Rule=rule, next_Rule=connections)
                Dict[lender_name][plan_name] = connections
        self.lender_rules = Dict