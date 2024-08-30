from Rule_model import Rule, Rule_Connection
import json

# Load the JSON file
with open('../data/Rules.json', 'r') as file:
    rules_json = json.load(file)


# Create a dictionary to hold the lenders and their associated rules
lender_rules = {}

# Iterate over the lenders in the JSON file
for lender, rules in rules_json['Lenders'].items():
    # List to hold the connected rules
    connections = None

    # Create Rule objects and connect them
    for rule_key, rule_data in reversed(list(rules.items())):
        rule = Rule(
            ID=rule_key,
            Rule_header=rule_data['Rule_Head'],
            Rule_operator=rule_data['Rule_Operator'],
            Rule_value=rule_data['Rule_Value'],
            Rule_order=None,
            Is_Nested=False,
            Nested_Rule=None,
            Rule_parent=lender,
            Flow_for_True=True
        )
        # Connect the rules using Rule_Connection
        connections = Rule_Connection(ID=rule_key, Rule=rule, next_Rule=connections)

    # Store the connected rules for the lender
    lender_rules[lender] = connections