from Rule_model import Rule, Rule_Connection, Flow_exception
import json
from XMl_validator import XMl_validator
import xml.etree.ElementTree as ET
from datetime import datetime

"""
    Summary of the Code:
        1. parse_nested_rule function: 
                This function recursively parses an XML element to create a Rule object, handling nested rules and exception flows (True/False conditions and remarks).
        2. take_decisions function: 
                This function takes the evaluated result of a rule and determines whether to proceed or stop based on the respective flow (True or False) conditions.
        3. Rule_XML_Approach (Class):
            1. __init__ method:
                This method initializes the class by validating the XML file against the given XSD schema.
                It parses the XML file and retrieves the root element for further processing.
            2. create_rules_using_xml method:
                This method creates rules for each lender by iterating over the provided test data.
                It evaluates each rule based on the data, takes decisions, and stores the results in a dictionary.
                If a rule requires evaluation and its decision is negative, it stops evaluating further rules for that lender's plan.
"""

def parse_nested_rule(Rule_element):
    """Recursive function to parse nested rules in the XML."""
    # Extracting necessary attributes
    # Initialize variables for True and False flow exception handling
    Flow_exception_True_Flow_rule, Flow_exception_True_Condition_to_proceed,Flow_exception_True_Remark,Flow_exception_False_Flow_rule, Flow_exception_False_Condition_to_proceed,Flow_exception_False_Remark = None, None, None, None, None, None
    # Parse the flow when the rule evaluation is True
    if Rule_element.find("Flow_for_True_eval") is not None:
        Flow_Exception_for_True = Rule_element.find("Flow_for_True_eval")
        # Parse exception rule and condition to proceed for the True flow
        if Flow_Exception_for_True.find('Exception_rule'):
            Flow_exception_True_Flow_rule = Flow_Exception_for_True.find('Exception_rule')
        if Flow_Exception_for_True.attrib.get('Condition_to_proceed'): 
            Flow_exception_True_Condition_to_proceed = Flow_Exception_for_True.attrib.get('Condition_to_proceed')
        if Flow_Exception_for_True.attrib.get('Remark'): 
            Flow_exception_True_Remark = Flow_Exception_for_True.attrib.get('Remark')
    # Parse the flow when the rule evaluation is False
    if Rule_element.find("Flow_for_False_eval") is not None:
        Flow_Exception_for_False = Rule_element.find("Flow_for_False_eval")
        # Parse exception rule and condition to proceed for the False flow
        if Flow_Exception_for_False.find('Exception_rule'):
            Flow_exception_False_Flow_rule = Flow_Exception_for_False.find('Exception_rule')
        if Flow_Exception_for_False.attrib.get('Condition_to_proceed'): 
            Flow_exception_False_Condition_to_proceed = Flow_Exception_for_False.attrib.get('Condition_to_proceed')
        if Flow_Exception_for_False.attrib.get('Remark'): 
            Flow_exception_False_Remark = Flow_Exception_for_False.attrib.get('Remark')
    # Create and return a Rule object with the parsed values, including any nested rules or exceptions
    return Rule(
                ID=Rule_element.tag,
                Rule_header    =  Rule_element.attrib['reference_field'],
                Rule_operator  =  Rule_element.attrib['rule_Operator'],
                Rule_value     =  Rule_element.attrib['rule_Value'],
                Field_Type     =  Rule_element.attrib.get('field_Type'),
                Is_Evaluating  =  Rule_element.attrib.get('Is_Evaluating', True),
                # Parse exception flow for True evaluation
                Flow_exception_True = Flow_exception(
                   Exception_rule =  parse_nested_rule(Flow_exception_True_Flow_rule) if Flow_exception_True_Flow_rule else None,
                   Condition_to_proceed =  bool(True) if Flow_exception_True_Condition_to_proceed == "true" else False,
                   Remark = Flow_exception_True_Remark if Flow_exception_True_Remark else ""
                  ),
                # Parse exception flow for False evaluation
                Flow_exception_False = Flow_exception(
                   Exception_rule =  parse_nested_rule(Flow_exception_False_Flow_rule) if Flow_exception_False_Flow_rule else None,
                   Condition_to_proceed = bool(False) if Flow_exception_False_Condition_to_proceed == "false" else True,
                   Remark = Flow_exception_False_Remark if Flow_exception_False_Remark else ""
                  ),
                # Parse logical operator and any nested logical rules
                logical_operator = Rule_element.attrib.get('logical_operator', None),
                Logical_Rule   =   parse_nested_rule(Rule_element.find('Logical_Rule')) if Rule_element.find('Logical_Rule') is not None else None,
        )

def  take_decisions(rule: Rule):
        """
            Determines the next action based on the evaluated result of the rule.
            Args:
                rule (Rule): The rule to be evaluated.
            Returns:
                bool: The decision to continue (True) or stop (False) based on the rule's evaluation.
        """
        # If the rule evaluation is True, follow the flow exception for True; otherwise, follow the False flow.
        if rule.Evaluated_result:
            return rule.Flow_Exception_for_True.Condition_to_proceed
        else:
            return rule.Flow_Exception_for_False.Condition_to_proceed

class Rule_XML_Approach:
    def __init__(self, xml_file_name, xsd_file_name):

        # Initialize the Rule_XML_Approach class by loading and validating the XML file
        # Create a dictionary to store lenders and their associated rules
        xml_validator = XMl_validator(XML_File_path=xml_file_name, XSD_File_path=xsd_file_name)
        
        # Validate the XML file against the XSD schema
        if not xml_validator.validate_XML():
            return False  # Exit if XML validation fails
        
        # Initialize an empty dictionary to hold rules for each lender
        self.lender_rules = {}
        
        # Parse the XML file and get the root element
        tree = ET.parse(xml_file_name)
        self.root = tree.getroot()
        print(self.root)  # Print the root element for debugging purposes

    def create_rules_using_xml(self, Data_of_Rule_test):
        # Create rules for each lender using the XML data and test data provided
        Dict = {}  # Dictionary to store rule evaluations
        
        # Iterate through each test case provided in Data_of_Rule_test
        for Data_for_rule in Data_of_Rule_test:
            # Iterate over each lender in the XML file
            for lender in self.root.find('Lenders'):
                lender_name = lender.attrib['name']  # Get lender's name
                Dict[lender_name] = {}  # Initialize dictionary for the lender
                
                # Iterate over each plan associated with the lender
                for plans in lender:
                    plan_name = plans.attrib['name']  # Get plan's name
                    Dict[lender_name][plan_name] = {}  # Initialize dictionary for the plan
                    
                    connections = None  # Placeholder for connections (not used in this snippet)
                    
                    # Iterate over the rules in the plan
                    for rules in list(plans):
                        rule_name = rules.attrib['name']  # Get rule's name
                        
                        # Parse the rule and create a rule object
                        rule_Obj = parse_nested_rule(rules)
                        
                        # Evaluate the rule with the test data
                        Evaluation_result = rule_Obj.evaluate(Data_for_rule)
                        
                        # Take a decision based on the rule's evaluation
                        taken_decision = take_decisions(rule_Obj)
                        
                        # Store the evaluation result for the rule
                        Dict[lender_name][plan_name][rule_name] = Evaluation_result
                        
                        # If the rule requires evaluation and the decision is negative, stop evaluating further rules
                        if rule_Obj.Is_Evaluating:
                            if not taken_decision:
                                break
        
        # Update the lender_rules attribute with the evaluated results
        self.lender_rules = Dict
