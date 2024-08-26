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

rules = {
    "LoanType == 'Primary'": [
        "Eligible_assets in ['Agricultural machinery and equipment', 'Materials handling/forklifts']",
        "Excluded_Assets not in ['Passenger cars', 'SUVs']",
        "Used_assets == true",
        "Private_sale == true",
        "Age_in_months_of_ABN >= 24",
        "Age_in_month_of_GST >= 4"
    ],
    "LoanType == 'Secondary'": [
        "Eligible_assets in ['Passenger vehicles', 'Light trucks', 'Light commercial vehicles (van, utes)', 'Classic cars', 'Motorbikes']",
        "Excluded_Assets not in ['Electric or motor vehicle used for hire/rental purposes', 'food trucks']",
        "Used_assets == true",
        "Private_sale == true",
        "Age_in_months_of_ABN >= 24",
        "Age_in_month_of_GST >= 24"
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
            0: Class("A"),
            1: Class("B"),
            2: Class("C"),
            3: Class("D"),
            4: Class("E"),
            5: Class("F") 

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


