from Rule_model import Rule, Rule_Connection
import json

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
        return Rule(
                ID=rule_key,
                Rule_header    =  rule_var['Reference_field'],
                Rule_operator  =  rule_var['Rule_Operator'],
                Rule_value     =  rule_var['Rule_Value'],
                Is_Nested      =  rule_var.get('Is_Nested', False),
                Nested_Rule    =  Logical_OR_NestedRule(rule_var['Nested_Rule'],"Nested_Rule",parent_rule_heading) if rule_var.get('Nested_Rule') else None,
                Flow_for_True=rule_var.get('Flow_for_True', True),
                logical_operator=rule_var.get('logical_operator', None),
                Logical_Rule   =   Logical_OR_NestedRule(rule_var['Logical_Rule'],"Logical_Rule",parent_rule_heading) if rule_var.get('Logical_Rule') else None
        )
    except KeyError as e:
        raise ValueError(f"Missing required key {e} in rule data: {rule_var}")
    except Exception as e:
        raise ValueError(f"An error occurred while creating a rule: {e}")


class Rules_using_JSON:
    def __init__(self, JsonFile_name):
        """
            Initializes the Rules_using_JSON object and loads the rules from a JSON file.

            Args:
                JsonFile_name (str): The name of the JSON file containing the rules.
        """
        # Create a dictionary to hold the lenders and their associated rules
        self.lender_rules = {}
        # Load the JSON file



        try:
            # Load the JSON file
            with open(JsonFile_name, 'r') as file:
                self.rules_json = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {JsonFile_name} not found. Please check the file path.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON file {JsonFile_name}: {e}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred while loading JSON file {JsonFile_name}: {e}")

    def Create_rules_using_json(self):
        """
            Creates Rule objects for each lender based on the rules defined in the JSON file.
            These Rule objects are connected using Rule_Connection and stored in lender_rules.
        """
        try:
            # Iterate over the lenders in the JSON file
            for lender, rules in self.rules_json['Lenders'].items():
                # List to hold the connected rules
                connections = None
                # Create Rule objects and connect them
                for rule_key, rule_data in reversed(list(rules.items())):
                    rule = Logical_OR_NestedRule(rule_data,rule_key,lender)
                    # Connect the rules using Rule_Connection
                    connections = Rule_Connection(ID=rule_key, Rule=rule, next_Rule=connections)
            
                # Store the connected rules for the lender
                self.lender_rules[lender] = connections
            if not self.lender_rules:
                raise ValueError("No lender rules were created. Check the JSON file for correctness.")
        except KeyError as e:
            raise ValueError(f"Missing required key {e} in lender rules data.")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred while creating rules from JSON: {e}")







