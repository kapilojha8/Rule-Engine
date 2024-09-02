from Rule_model import Rule, Rule_Connection
import json
import copy

# Load the JSON file
with open('../data/Rules.json', 'r') as file:
    rules_json = json.load(file)


# Create a dictionary to hold the lenders and their associated rules
lender_rules = {}

def Logical_OR_NestedRule(rule_var, rule_key="",parent_rule_heading=""):
    return Rule(
            ID=rule_key,
            Rule_header    =  rule_var['Rule_Head'],
            Rule_operator  =  rule_var['Rule_Operator'],
            Rule_value     =  rule_var['Rule_Value'],
            Rule_order     =  rule_var['Rule_order'] if rule_var.get('Rule_order') else None,
            Is_Nested      =  rule_var['Is_Nested'] if rule_var.get('Is_Nested') else False,
            Nested_Rule    =  Logical_OR_NestedRule(rule_var['Nested_Rule'],"Nested_Rule",parent_rule_heading) if rule_var.get('Nested_Rule') else None,
            Rule_parent    =  parent_rule_heading,
            Flow_for_True  =  rule_var['Flow_for_True'] if rule_var.get('Flow_for_True') else True,
            logical_operator = rule_var['logical_operator'] if rule_var.get('logical_operator') else None,
            Logical_Rule   =   Logical_OR_NestedRule(rule_var['Logical_Rule'],"Logical_Rule",parent_rule_heading) if rule_var.get('Logical_Rule') else None
    )

# Iterate over the lenders in the JSON file
for lender, rules in rules_json['Lenders'].items():
    # List to hold the connected rules
    connections = None
    # Create Rule objects and connect them
    for rule_key, rule_data in reversed(list(rules.items())):
        rule = Logical_OR_NestedRule(rule_data,rule_key,lender)
        # rule = Rule(
        #     ID             =  rule_key,
        #     Rule_header    =  rule_data['Rule_Head'],
        #     Rule_operator  =  rule_data['Rule_Operator'],
        #     Rule_value     =  rule_data['Rule_Value'],
        #     Rule_order     =  None,
        #     Is_Nested      =  rule_data['Is_Nested'] if rule_data.get('Is_Nested') else False,
        #     Nested_Rule    =  Logical_OR_NestedRule(rule_data['Nested_Rule'],"Nested_Rule",lender) if rule_data.get('Nested_Rule') else None,
        #     Rule_parent    =  lender,
        #     Flow_for_True  =  rule_data['Flow_for_True'] if rule_data.get('Flow_for_True') else True,
        #     logical_operator = rule_data['logical_operator'] if rule_data.get('logical_operator') else None,
        #     Logical_Rule   =  Logical_OR_NestedRule(rule_data['Logical_Rule'],"Logical_Rule",lender) if rule_data.get('Logical_Rule') else None
        # )
        # Connect the rules using Rule_Connection
        connections = Rule_Connection(ID=rule_key, Rule=rule, next_Rule=connections)
    # temppte = copy.deepcopy(connections)
    # print("======"*30)
    # while temppte!=None:
    #     print("\n Rule ", temppte.Rule,"\n")
    #     if temppte.Rule.Nested_Rule:
    #         print("\n Nested_Rule ", temppte.Rule.Nested_Rule,"\n")
    #     temppte = temppte.next_Rule


    # Store the connected rules for the lender
    lender_rules[lender] = connections