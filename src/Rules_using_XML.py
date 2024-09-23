import xml.etree.ElementTree as ET
from Rule_model import Rule, Rule_Connection, Flow_exception


def parse_nested_rule(Rule_element):
    """Recursive function to parse nested rules in the XML."""
    # Extracting necessary attributes
    Flow_exception_True_Flow_rule, Flow_exception_True_Condition_to_proceed,Flow_exception_True_Remark,Flow_exception_False_Flow_rule, Flow_exception_False_Condition_to_proceed,Flow_exception_False_Remark = None, None, None, None, None, None
    if Rule_element.find("Flow_Exception_for_True"):
        Flow_Exception_for_True = Rule_element.find("Flow_Exception_for_True")
        if Flow_Exception_for_True.find('Exception_rule'):
            Flow_exception_True_Flow_rule = Flow_Exception_for_True.find('Exception_rule')
        if Flow_Exception_for_True.attrib.get('Condition_to_proceed'): 
            Flow_exception_True_Condition_to_proceed = Flow_Exception_for_True.attrib.get('Condition_to_proceed')
        if Flow_Exception_for_True.attrib.get('Remark'): 
            Flow_exception_True_Remark = Flow_Exception_for_True.attrib.get('Remark')

    if Rule_element.find("Flow_Exception_for_False"):
        Flow_Exception_for_False = Rule_element.find("Flow_Exception_for_False")
        if Flow_Exception_for_False.find('Exception_rule'):
            Flow_exception_False_Flow_rule = Flow_Exception_for_False.find('Exception_rule')
        if Flow_Exception_for_False.attrib.get('Condition_to_proceed'): 
            Flow_exception_False_Condition_to_proceed = Flow_Exception_for_False.attrib.get('Condition_to_proceed')
        if Flow_Exception_for_False.attrib.get('Remark'): 
            Flow_exception_False_Remark = Flow_Exception_for_False.attrib.get('Remark')
    
    return Rule(
                ID=Rule_element.tag,
                Rule_header    =  Rule_element.attrib['Reference_field'],
                Rule_operator  =  Rule_element.attrib['Rule_Operator'],
                Rule_value     =  Rule_element.attrib['Rule_Value'],
                Field_Type     =  Rule_element.attrib.get('Field_Type'),
                Is_Evaluating  =  Rule_element.attrib.get('Is_Evaluating', True),
                Flow_exception_True = Flow_exception(
                   Exception_rule =  parse_nested_rule(Flow_exception_True_Flow_rule) if Flow_exception_True_Flow_rule else None,
                   Condition_to_proceed =  Flow_exception_True_Condition_to_proceed if Flow_exception_True_Condition_to_proceed else False,
                   Remark = Flow_exception_True_Remark if Flow_exception_True_Remark else ""
                  ),
                Flow_exception_False = Flow_exception(
                   Exception_rule =  parse_nested_rule(Flow_exception_False_Flow_rule) if Flow_exception_False_Flow_rule else False,
                   Condition_to_proceed = Flow_exception_False_Condition_to_proceed if Flow_exception_False_Condition_to_proceed else None,
                   Remark = Flow_exception_False_Remark if Flow_exception_False_Remark else ""
                  ),
                
                logical_operator = Rule_element.attrib.get('logical_operator', None),
                Logical_Rule   =   parse_nested_rule(Rule_element.find('Logical_Rule')) if Rule_element.find('Logical_Rule') else None,
        )

class RulesUsingXML:
    def __init__(self, xml_file_name):
        # Create a dictionary to hold the lenders and their associated rules
        self.lender_rules = {}
        # Load the XML file
        tree = ET.parse(xml_file_name)
        self.root = tree.getroot()
        print(self.root)

    def create_rules_using_xml(self):
        # Iterate over the lenders in the XML file
        Dict = {}
        for lender in self.root.find('Lenders'):
            connections = None
            Dict[lender.tag] = {}
            lender_name = lender.tag
            for rule_element in reversed(list(lender)):
                rule = parse_nested_rule(rule_element)
                connections = Rule_Connection(ID=rule_element.tag, Rule=rule, next_Rule=connections)
                # for ref,refval in Dict[lender.tag][rule_element.tag]:
                #     print(ref,refval)
                Dict[lender.tag][rule_element.tag] = {}
                # Dict[lender.tag][rule_element.tag]['Reference_field'] = rule_element.find('Rule').get('Reference_field')
                # Dict[lender.tag][rule_element.tag]['Rule_Operator'] = rule_element.find('Rule').get('Rule_Operator')
                # Dict[lender.tag][rule_element.tag]['Field_Type'] = rule_element.find('Rule').get('Field_Type')
            self.lender_rules[lender_name] = connections