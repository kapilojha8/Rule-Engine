import sys
from Loan_attributions import Actions, Class, Allocations, DataHandler

# Check for right usage:
#   - approach = rule-engine
#   - approach = if-statements
if len(sys.argv) != 2:
    sys.exit("Usage: python main.py approach")


# Define rules

# Inputs
# rules = {
#     # Rainbow High
#     "Loan == 'Primary'": [
#         "Eligible_assets in [Agricultural machinery and equipment,Materials handling/forklifts]",
#         "Excluded_Assets not in [Passenger cars, SUVs]",
#         "Used_assets == True",
#         "Private_sale ==  True"
#         "Age_in_months_of_ABN >= 24"
#         "Age_in_month_of_GST >= 0"
#     ],

#     # Waterfalls School for Girls 
#     "LoanType == 'Secondary'": [
#         "Eligible_assets in [Passenger vehicles, Light trucks, Light commercial vehicles (van, utes), Classic cars, Motorbikes]",
#         "Excluded_Assets not in [Electric or motor vehicle used for hire/rental purposes, food trucks]",
#         "Used_assets == True",
#         "Private_sale ==  True"
#         "Age_in_months_of_ABN >= 24"
#         "Age_in_month_of_GST >= 24"
#     ]
# }

Primary_Lenders_rule_definations = {
            "Flexi up to $20K"     : ["Eligible_assets in ['Agricultural machinery', 'Materials handling/forklifts']","Used_assets == true"],
            "Flexi: $20-$50K"      : ["Eligible_assets in ['equipment (non-mining)', 'Materials']","Used_assets == true"],
            "Flexi: $50-$300K"     : ["Eligible_assets in ['Construction and earth moving', 'Materials']","Used_assets == true"],
            "Resimac- low doc"     : ["Eligible_assets in ['caravans', 'Materials']","Used_assets == true"],
            "Resimac- light doc"   : ["Eligible_assets in ['Trailers', 'Materials']","Used_assets == true"],
            "Pepper Tier A"        : ["Eligible_assets in ['forklifts', 'Materials']","Used_assets == true"],
            "Pepper Tier B"        : ["Eligible_assets in ['trucks', 'Materials']","Used_assets == true"],
            "Pepper Tier C"        : ["Eligible_assets in ['wheeled construction equipment', 'Materials']","Used_assets == true"]
}


rules = {
    "LoanType == 'Primary'": [
        " or  ".join(Primary_Lenders_rule_definations['Flexi up to $20K']),
        " or  ".join(Primary_Lenders_rule_definations['Flexi: $20-$50K']),
        " or  ".join(Primary_Lenders_rule_definations['Flexi: $50-$300K']),
        " or  ".join(Primary_Lenders_rule_definations['Resimac- low doc']),
        " or  ".join(Primary_Lenders_rule_definations['Resimac- light doc']),
        " or  ".join(Primary_Lenders_rule_definations['Pepper Tier A']),
        " or  ".join(Primary_Lenders_rule_definations['Pepper Tier B']),
        " or  ".join(Primary_Lenders_rule_definations['Pepper Tier C']),
    ],
    "LoanType == 'Secondary'": [
        "Eligible_assets in ['Passenger vehicles', 'Light trucks', 'Motorbikes']",
        "Excluded_Assets not in ['Electric or motor vehicle used for hire/rental purposes', 'food trucks']",
        "Used_assets == true",
        "Private_sale == true",
        "Age_in_months_of_ABN >= 24",
        "Age_in_month_of_GST >= 4",
        "Age_in_month_of_GST >= 4",
        "Age_in_month_of_GST >= 4",
    ]
}

# print('The Rules were : ',rules)
 

# Input/output locations
load_path = "../data/Loan_dataset.csv"
save_path = "../data/saveRecord.csv"

# DataHandler
handler = DataHandler(load_path)
Loans = handler.load_Loans()

if (sys.argv[1] == "rule-engine"):

    actions =  Actions(
        logic = {
            0: Class("Flexi up to $20K"),
            1: Class("Flexi: $20-$50K"),
            2: Class("Flexi: $50-$300K"),
            3: Class("Resimac- low doc"),
            4: Class("Resimac- light doc"),
            5: Class("Pepper Tier A"), 
            6: Class("Pepper Tier B"), 
            7: Class("Pepper Tier C")

        }
    )

    # Allocate Loans using rule engine
    alloc1 = Allocations({})
    allocations1 = alloc1.allocate_Loans_rule_engine(actions, rules, Loans)
    print('allocations : ',allocations1)
    # Save allocated Loans
    handler.save_Loans(load_path, save_path, allocations1)

else:
    sys.exit("Incorrect arguments. Did you mean: rule-engine or if-statements?")


