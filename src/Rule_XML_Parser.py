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


def Logical_OR_NestedRule(rule_var, rule_key="",parent_rule_heading=""):
    """
        Recursively creates Rule objects based on the provided rule data. Handles nested and logical rules.

        Args:
            rule_var (dict): Dictionary containing rule information.
            rule_key (str): Unique identifier for the rule.
            parent_rule_heading (str): The heading of the parent rule, used for reference.

        Returns:
            Rule: A Rule object created based on the input rule data.
    """
    try:
        Flow_exception_True_Flow_rule, Flow_exception_True_Condition_to_proceed,Flow_exception_True_Remark, Flow_exception_False_Flow_rule, Flow_exception_False_Condition_to_proceed,Flow_exception_False_Remark = None, None, None, None, None, None
        if rule_var.get('Flow_Exception_for_True'):
            if rule_var.get('Flow_Exception_for_True').get('Exception_rule'):
                Flow_exception_True_Flow_rule = rule_var['Flow_Exception_for_True'].get('Exception_rule')
            if rule_var.get('Flow_Exception_for_True').get('Condition_to_proceed'): 
                Flow_exception_True_Condition_to_proceed = rule_var['Flow_Exception_for_True'].get('Condition_to_proceed')
            if rule_var.get('Flow_Exception_for_True').get('Remark'): 
                Flow_exception_True_Remark = rule_var['Flow_Exception_for_True'].get('Remark')

        if rule_var.get('Flow_Exception_for_False'):
            if rule_var.get('Flow_Exception_for_False').get('Exception_rule'):
                Flow_exception_False_Flow_rule = rule_var['Flow_Exception_for_False'].get('Exception_rule')
            if rule_var.get('Flow_Exception_for_False').get('Condition_to_proceed'): 
                Flow_exception_False_Condition_to_proceed = rule_var['Flow_Exception_for_False'].get('Condition_to_proceed')
            if rule_var.get('Flow_Exception_for_False').get('Remark'): 
                Flow_exception_False_Remark = rule_var['Flow_Exception_for_False'].get('Remark')

        return Rule(
                ID=rule_key,
                Rule_header    =  rule_var['Reference_field'],
                Rule_operator  =  rule_var['Rule_Operator'],
                Rule_value     =  rule_var['Rule_Value'],
                Field_Type     =  rule_var.get('Field_Type'),            
                Is_Nested      =  rule_var.get('Is_Nested', False),
                Nested_Rule    =  Logical_OR_NestedRule(rule_var['Nested_Rule'],"Nested_Rule",parent_rule_heading) if rule_var.get('Nested_Rule') else None,
                Flow_for_True  = rule_var.get('Flow_for_True', True),
                Flow_for_False = rule_var.get('Flow_for_False', False),

                Flow_exception_True = Flow_exception(
                   Exception_rule =  Logical_OR_NestedRule(Flow_exception_True_Flow_rule) if Flow_exception_True_Flow_rule else None,
                   Condition_to_proceed =  Flow_exception_True_Condition_to_proceed if Flow_exception_True_Condition_to_proceed else False,
                   Remark = Flow_exception_True_Remark if Flow_exception_True_Remark else ""
                  ),
                Flow_exception_False = Flow_exception(
                   Exception_rule =  Logical_OR_NestedRule(Flow_exception_False_Flow_rule) if Flow_exception_False_Flow_rule else False,
                   Condition_to_proceed = Flow_exception_False_Condition_to_proceed if Flow_exception_False_Condition_to_proceed else None,
                   Remark = Flow_exception_False_Remark if Flow_exception_False_Remark else ""
                  ),
                
                logical_operator=rule_var.get('logical_operator', None),
                Logical_Rule   =   Logical_OR_NestedRule(rule_var['Logical_Rule'],"Logical_Rule",parent_rule_heading) if rule_var.get('Logical_Rule') else None,
                Remark         =   rule_var.get('Remark', "")
        )
    except KeyError as e:
        raise ValueError(f"Missing required key {e} in rule data: {rule_var}")
    except Exception as e:
        raise ValueError(f"An error occurred while creating a rule: {e}")
    
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


def evaluate(self, data):
    """
        Evaluates the rule against provided data.

        Args:
            data (dict): The data dictionary containing values to be evaluated against the rule.

        Returns:
            bool: The result of the rule evaluation (True or False).
    """

    nested_remark = ""
    if self.Rule_header not in data:
        raise ValueError(f"Header {self.Rule_header} not found in data.")
    
    actual_value = data[self.Rule_header]
    
    # Handle date comparison
    if isinstance(actual_value, datetime) or isinstance(self.Rule_value, datetime):
        self.Rule_value = datetime.strptime(self.Rule_value, "%d/%m/%Y").date() if isinstance(self.Rule_value, str) else self.Rule_value
        actual_value = actual_value.date() if isinstance(actual_value, datetime) else actual_value
    
    try:
        if isinstance(self.Rule_value, str) and self.Rule_value.isdigit():
            self.Rule_value = int(self.Rule_value)
        if isinstance(actual_value, str) and actual_value.isdigit():
            actual_value = int(actual_value)
    except ValueError:
        raise ValueError(f"Cannot convert {self.Rule_value} or {actual_value} to int.")
    
    # Add additional operator support here
    if self.Rule_operator == "==":
        if isinstance(actual_value, str) and isinstance(self.Rule_value, str):
            result = actual_value.strip().lower() == self.Rule_value.strip().lower()
        else:
            result = actual_value == self.Rule_value
    elif self.Rule_operator == "!=":
        if isinstance(actual_value, str) and isinstance(self.Rule_value, str):
            result = actual_value.strip().lower() != self.Rule_value.strip().lower()
        else:
            result = actual_value != self.Rule_value
    elif self.Rule_operator == ">":
        result = actual_value > self.Rule_value
    elif self.Rule_operator == "<":
        result = actual_value < self.Rule_value
    elif self.Rule_operator == ">=":
        result = actual_value >= self.Rule_value
    elif self.Rule_operator == "<=":
        result = actual_value <= self.Rule_value
    elif self.Rule_operator == "in":
        if isinstance(self.Rule_value, str):
            self.Rule_value = [x.strip().lower() for x in self.Rule_value.split(",")]
        result = actual_value.strip().lower() in self.Rule_value
    elif self.Rule_operator == "not in":
        if isinstance(self.Rule_value, str):
            self.Rule_value = [x.strip().lower() for x in self.Rule_value.split(",")]
        result = actual_value.strip().lower() not in self.Rule_value
    else:
        raise ValueError(f"Unsupported operator: {self.Rule_operator}")
    
    if self.logical_operator:
        if self.logical_operator == "and":
            result = result and self.Logical_Rule.evaluate(data)['Return_result']
        elif self.logical_operator == "or":
            result = result or self.Logical_Rule.evaluate(data)['Return_result']
    
    if result:
        if self.Flow_Exception_for_True and self.Flow_Exception_for_True.Remark:
            nested_remark += self.Flow_Exception_for_True.Remark
        if self.Flow_Exception_for_True and self.Flow_Exception_for_True.Exception_rule:
            LLO = self.Flow_Exception_for_True.Exception_rule.evaluate(data)
            nested_remark = nested_remark+" || "+LLO['Remark'] if nested_remark != "" else LLO['Remark']
            result = LLO['Return_result']
    else:
        if self.Flow_Exception_for_False and self.Flow_Exception_for_False.Remark:
            nested_remark += self.Flow_Exception_for_False.Remark
        if self.Flow_Exception_for_False and self.Flow_Exception_for_False.Exception_rule:
            LLO = self.Flow_Exception_for_False.Exception_rule.evaluate(data)
            nested_remark = nested_remark+" || "+LLO['Remark'] if nested_remark != "" else LLO['Remark']
            result = LLO['Return_result']        
    self.Evaluated_result = result
    return {"Return_result": result, "Remark": nested_remark }



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
    nested_remark = ""
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

    ID             =  Rule_element.tag
    Rule_header    =  Rule_element.attrib['reference_field']
    Rule_operator  =  Rule_element.attrib['rule_Operator']
    Field_Type     =  Rule_element.attrib.get('field_Type')
    Rule_value     =  convert_value(Rule_element.attrib['rule_Value'], Field_Type)
    # Evaluation_result = False  ## The Evaluation will be executed here
    Evaluation_result  = evaluate_result(Rule_header, Rule_operator, Rule_value, Data_for_rule)
    if Rule_element.find("Flow_for_True_eval") is not None:
        Flow_Exception_for_True = Rule_element.find("Flow_for_True_eval")
        if Flow_Exception_for_True.find('Exception_rule'):
            Flow_exception_True_Flow_rule = Flow_Exception_for_True.find('Exception_rule')
        if Flow_Exception_for_True.attrib.get('Condition_to_proceed'): 
            Flow_exception_True_Condition_to_proceed = Flow_Exception_for_True.attrib.get('Condition_to_proceed')
        if Flow_Exception_for_True.attrib.get('Remark'): 
            Flow_exception_True_Remark = Flow_Exception_for_True.attrib.get('Remark')

    if Rule_element.find("Flow_for_False_eval") is not None:
        Flow_Exception_for_False = Rule_element.find("Flow_for_False_eval")
        if Flow_Exception_for_False.find('Exception_rule'):
            Flow_exception_False_Flow_rule = Flow_Exception_for_False.find('Exception_rule')
        if Flow_Exception_for_False.attrib.get('Condition_to_proceed'): 
            Flow_exception_False_Condition_to_proceed = Flow_Exception_for_False.attrib.get('Condition_to_proceed')
        if Flow_Exception_for_False.attrib.get('Remark'): 
            Flow_exception_False_Remark = Flow_Exception_for_False.attrib.get('Remark')
    

    take_decisions(Evaluation_result, Flow_exception_True_Condition_to_proceed, Flow_exception_False_Condition_to_proceed)
    # evaluating 
    Is_Evaluating  =  Rule_element.attrib.get('Is_Evaluating', True)


    # print('==> ',Rule_header, Rule_operator, Rule_value)
    # print("The Rule operator is  ",Rule_operator, Field_Type)
    return True

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
                        rule = parse_nested_rule(rules, Data_for_rule)
                        print("The Rule Result is :",rule)
                    break
                        # connections = Rule_Connection(ID=rules.attrib['name'], Rule=rule, next_Rule=connections)
                    # Dict[lender_name][plan_name] = connections
            # self.lender_rules = Dict

