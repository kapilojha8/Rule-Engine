import sys
from Loan_attributions import Actions, Class, Allocations, DataHandler
from Rule_model import Rule,Rule_Connection
import copy

# Check for right usage:
#   - approach = rule-engine
#   - approach = if-statements
if len(sys.argv) != 2:
    sys.exit("Usage: python main.py approach")

R1 = Rule("111","Eligible_assets","['EV Car', 'Materials handling/forklifts']","in",1,False,"","Flexi up to $20K")
# print(R1)
R_I1 = Rule("112","Eligible_assets","EV Car","==",1,False,"","Flexi up to $20K")
RI1 = Rule("113","Asset_age",3,">",7,True,R_I1,"Flexi up to $20K")
RN1 = Rule("114", "Borrowering_for_months", 60, "<=", 1, True, RI1, "Flexi up to $20K")

ROP = Rule("111","Used_assets","true","==",1,False,"","Flexi up to $20K")
ABN = Rule("111","ABN(Months)",24,">",1,False,"","Flexi up to $20K")
GST = Rule("111","GST(Months)",24,">",1,False,"","Flexi up to $20K")

Data_of_Rule_test = {
    "ID" : 1001,
    "Eligible_assets" : "EV Car",
    "Excluded_Assets" : "food trucks",
    "Used_assets" : "true",
    "Private_sale" : "False",
    "Age_in_months_of_ABN" : 5,
    "Age_in_month_of_GST" : 1,
    "LoanType" : "Primary",
    "Asset_age" : 5,
    "Borrowering_for_months" : 55,
    "ABN(Months)":27,
    "GST(Months)":30
}
# print("R1 Rule :",R1)
# print('R1 Result : ',R1.evaluate(Data_of_Rule_test))

# print("RN1 Rule :",RN1)
# print('RN1 Result : ',RN1.evaluate(Data_of_Rule_test))


Flexi_up_to_20K = Rule_Connection(27001,R1,Rule_Connection(27002,ABN,Rule_Connection(27003,GST)))


temppte = copy.deepcopy(Flexi_up_to_20K)
while temppte!=None:
    print("Flexi up to 20k ", temppte)
    print("Eveluation : ",temppte.Rule.evaluate(Data_of_Rule_test))
    temppte = temppte.next_Rule




exit()

print('Flexi Rule ',Flexi_up_to_20K)
Primary_Lenders_rule_definations = {
            "Flexi up to $20K"     : str(Flexi_up_to_20K),
            "Flexi: $20-$50K"      : ["Eligible_assets in ['equipment (non-mining)', 'Materials']","Used_assets == 'true'"],
            "Flexi: $50-$300K"     : ["Eligible_assets in ['Construction and earth moving', 'Materials']","Used_assets == 'true'"],
            "Resimac- low doc"     : ["Eligible_assets in ['caravans', 'Materials']","Used_assets == 'true'"],
            "Resimac- light doc"   : ["Eligible_assets in ['Trailers', 'Materials']","Used_assets == 'true'"],
            "Pepper Tier A"        : ["Eligible_assets in ['forklifts', 'Materials']","Used_assets == 'true'"],
            "Pepper Tier B"        : ["Eligible_assets in ['trucks', 'Materials']","Used_assets == 'true'"],
            "Pepper Tier C"        : ["Eligible_assets in ['wheeled construction equipment', 'Materials']","Used_assets == 'true'"]
}


rules = {
    "LoanType == 'Primary'": [
        Primary_Lenders_rule_definations['Flexi up to $20K'],
        " and  ".join(Primary_Lenders_rule_definations['Flexi: $20-$50K']),
        " and  ".join(Primary_Lenders_rule_definations['Flexi: $50-$300K']),
        " and  ".join(Primary_Lenders_rule_definations['Resimac- low doc']),
        " and  ".join(Primary_Lenders_rule_definations['Resimac- light doc']),
        " and  ".join(Primary_Lenders_rule_definations['Pepper Tier A']),
        " and  ".join(Primary_Lenders_rule_definations['Pepper Tier B']),
        " and  ".join(Primary_Lenders_rule_definations['Pepper Tier C']),
        "true" 
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
        "true"
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
            7: Class("Pepper Tier C"),
            8: Class('Lender Not Found !')

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


