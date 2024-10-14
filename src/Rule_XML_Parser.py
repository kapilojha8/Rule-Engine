from Rule_model import Rule, Rule_Connection, Flow_exception
import json
from XMl_validator import XMl_validator
import xml.etree.ElementTree as ET
from datetime import datetime

"""
    Summary of the Code:
        1. Logical_OR_NestedRule Function:
            This function is responsible for recursively creating Rule objects.
            It handles nested rules (Nested_Rule) and logical rules (Logical_Rule) by calling itself recursively.
            This function is designed to support flexible rule structures where rules can be combined using logical operators (and, or).
        2. Rules_using_JSON Class:
            This class loads rules from a JSON file and creates rule objects using the Logical_OR_NestedRule function.
            The rules are connected in a linked list manner using the Rule_Connection class.
            Each lender's rules are stored in a dictionary (lender_rules), with the lender's name as the key.
"""
def convert_value(value, Field_Type):
    if Field_Type == 0 or Field_Type == '0':  # bool
        return bool(value)
    elif Field_Type == 1 or Field_Type == '1':  # date
        try:
            return datetime.strptime(value, "%d/%m/%Y")  # Assuming the date format is dd/mm/yyyy
        except ValueError:
            raise ValueError(f"Invalid date format for {value}. Expected format: dd/mm/yyyy")
    elif Field_Type == 2 or Field_Type == '2':  # float
        return float(value)
    elif Field_Type == 3 or Field_Type == '3':  # int                
        return int(value)
    elif Field_Type == 4 or Field_Type == '4':  # str
        return str(value)
    else:
        raise ValueError(f"Unknown Field_Type: {Field_Type}")

def  take_decisions(Evaluation_result:bool, True_Condition_to_proceed: Rule, False_Condition_to_proceed):
        """
            Determines the next action based on the evaluated result of the rule.
            Args:
                rule (Rule): The rule to be evaluated.
            Returns:
                bool: The decision to continue (True) or stop (False) based on the rule's evaluation.
        """
        if Evaluation_result:
            return True_Condition_to_proceed
        else:
            return False_Condition_to_proceed
   

def evaluate_result(Rule_header, Rule_operator, Rule_value, Data):
    """
        Evaluates the rule against provided data.

        Args:
            data (dict): The data dictionary containing values to be evaluated against the rule.

        Returns:
            bool: The result of the rule evaluation (True or False).
    """
    if Rule_header not in Data:
        raise ValueError(f"Header {Rule_header} not found in data.")
    
    actual_value = Data[Rule_header]
    # Handle date comparison
    if isinstance(actual_value, datetime) or isinstance(Rule_value, datetime):
        Rule_value = datetime.strptime(Rule_value, "%d/%m/%Y").date() if isinstance(Rule_value, str) else Rule_value
        actual_value = actual_value.date() if isinstance(actual_value, datetime) else actual_value
    
    try:
        if isinstance(Rule_value, str) and Rule_value.isdigit():
            Rule_value = int(Rule_value)
        if isinstance(actual_value, str) and actual_value.isdigit():
            actual_value = int(actual_value)
    except ValueError:
        raise ValueError(f"Cannot convert {Rule_value} or {actual_value} to int.")
    result = False
    # Add additional operator support here
    if Rule_operator == "==":
        if isinstance(actual_value, str) and isinstance(Rule_value, str):
            result = actual_value.strip().lower() == Rule_value.strip().lower()
        else:
            result = actual_value == Rule_value
    elif Rule_operator == "!=":
        if isinstance(actual_value, str) and isinstance(Rule_value, str):
            result = actual_value.strip().lower() != Rule_value.strip().lower()
        else:
            result = actual_value != Rule_value
    elif Rule_operator == ">":
        result = actual_value > Rule_value
    elif Rule_operator == "<":
        result = actual_value < Rule_value
    elif Rule_operator == ">=":
        result = actual_value >= Rule_value
    elif Rule_operator == "<=":
        result = actual_value <= Rule_value
    elif Rule_operator == "in":
        if isinstance(Rule_value, str):
            Rule_value = [x.strip().lower() for x in Rule_value.split(",")]
        result = actual_value.strip().lower() in Rule_value
    elif Rule_operator == "not in":
        if isinstance(Rule_value, str):
            Rule_value = [x.strip().lower() for x in Rule_value.split(",")]
        result = actual_value.strip().lower() not in Rule_value
    else:
        raise ValueError(f"Unsupported operator: {Rule_operator}")

    return result




def parse_nested_rule(Rule_element, Data_for_rule):
    """
        Recursively parsing the XMl Rule Element and extracting the required attribues from it. then applying the Data for the specific rules. Handles nested and logical rules.

        Args:
            rule_var (dict): Dictionary containing rule information.
            rule_key (str): Unique identifier for the rule.
            parent_rule_heading (str): The heading of the parent rule, used for reference.

        Returns:
            Rule: A Rule object created based on the input rule data.
    """
    ID             =  Rule_element.tag
    Rule_header    =  Rule_element.attrib['reference_field']
    Rule_operator  =  Rule_element.attrib['rule_Operator']
    Field_Type     =  Rule_element.attrib.get('field_Type')
    Rule_value     =  convert_value(Rule_element.attrib['rule_Value'], Field_Type)
    Evaluation_result  = evaluate_result(Rule_header, Rule_operator, Rule_value, Data_for_rule)
    Is_Evaluating  =  False if Rule_element.attrib.get('is_Evaluating', True) == "false" else True
    nested_remark = ""
    Flow_exception_True_Flow_rule, Flow_exception_True_Condition_to_proceed,Flow_exception_True_Remark,Flow_exception_False_Flow_rule, Flow_exception_False_Condition_to_proceed,Flow_exception_False_Remark = None, None, None, None, None, None

    if Rule_element.find("Flow_for_True_eval") is not None:
        Flow_Exception_for_True = Rule_element.find("Flow_for_True_eval")
        if Flow_Exception_for_True.attrib.get('Condition_to_proceed'):
            Flow_exception_True_Condition_to_proceed =  True if Flow_Exception_for_True.attrib.get('Condition_to_proceed') == "true" else False
        if Flow_Exception_for_True.attrib.get('Remark'):
            Flow_exception_True_Remark = Flow_Exception_for_True.attrib.get('Remark')
        if Evaluation_result:
            nested_remark += Flow_exception_True_Remark
        if Evaluation_result and (Flow_Exception_for_True.find('Exception_rule') is not None):
            Flow_exception_True_Flow_rule = Flow_Exception_for_True.find('Exception_rule')
            LLO = parse_nested_rule(Flow_exception_True_Flow_rule, Data_for_rule)
            nested_remark = nested_remark+" || "+LLO['Remark'] if nested_remark != "" else LLO['Remark']
            Evaluation_result = LLO['Return_result']


    if Rule_element.find("Flow_for_False_eval") is not None:
        Flow_Exception_for_False = Rule_element.find("Flow_for_False_eval")
        if Flow_Exception_for_False.attrib.get('Condition_to_proceed'): 
            Flow_exception_False_Condition_to_proceed =  True if Flow_Exception_for_False.attrib.get('Condition_to_proceed') == "true" else False
        if Flow_Exception_for_False.attrib.get('Remark'): 
            Flow_exception_False_Remark = Flow_Exception_for_False.attrib.get('Remark')
        if not Evaluation_result:
            nested_remark += Flow_exception_False_Remark
        if (not Evaluation_result) and (Flow_Exception_for_False.find('Exception_rule') is not None):
            Flow_exception_False_Flow_rule = Flow_Exception_for_False.find('Exception_rule')
            LLO = parse_nested_rule(Flow_exception_False_Flow_rule, Data_for_rule)
            nested_remark = nested_remark+" || "+LLO['Remark'] if nested_remark != "" else LLO['Remark']
            Evaluation_result = LLO['Return_result']


    # evaluating
    if Is_Evaluating:
        Evaluation_result =  True if take_decisions(Evaluation_result, Flow_exception_True_Condition_to_proceed, Flow_exception_False_Condition_to_proceed) else False
    else:
        Evaluation_result = True

    return {"Return_result": Evaluation_result, "Remark": nested_remark }


class Rules_XML_Parser:
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

    def create_rules_using_xml(self, Data_of_Rule_test):
        # Iterate over the lenders in the XML file
        Dict = {}
        for Data_for_rule in Data_of_Rule_test:
            for lender in self.root.find('Lenders'):
                lender_name = lender.attrib['name']
                Dict[lender_name] = {}
                for plans in lender:
                    plan_name = plans.attrib['name']
                    Dict[lender_name][plan_name] = {} 
                    connections = None
                    for rules in  list(plans):# reversed(list(plans)):
                        rule_name = rules.attrib['name']
                        rule_output = parse_nested_rule(rules, Data_for_rule)
                        Dict[lender_name][plan_name][rule_name] = rule_output
                        if not rule_output['Return_result']:
                            print("Kya hua Result is :",rule_output)
                            break
                        print("The Rule Result is :",rule_output)
                    # break
                    
                        # connections = Rule_Connection(ID=rules.attrib['name'], Rule=rule, next_Rule=connections)
                    # Dict[lender_name][plan_name] = connections
            # self.lender_rules = Dict
        print("==="*30)
        print("The Result Dictionary",Dict)

