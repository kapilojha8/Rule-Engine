import sys
from Loan_attributions import Actions, Class, Allocations, DataHandler
from Rule_model import Rule,Rule_Connection
import copy
from Rules_using_JSON import  Rules_using_JSON
import pandas as pd
from datetime import datetime

Client_data = pd.read_csv("../data/Data from Client.csv")

Client_data.rename(columns= {"asset_type":"Assets","applicant_entity_type":"Eligible_Applicant"}, inplace=True)  #"repayment_term_month" : "", "applicant_entity_type":"", "asset_supplier_type":"",

def Evaluate_and_take_decision(Rule_chain, Rule, Data_rule):
    Rule.evaluate(Data_rule)
    if Rule.Is_Nested and (not Rule.Evaluated_result):
        Rule.Evaluated_result = Evaluate_and_take_decision(Rule_chain, Rule.Nested_Rule, Data_rule)
    return Rule_chain.take_decisions(Rule)

# Calculating the Age  of Assets
# Get the current year
current_year = datetime.now().year

# Calculate the asset age
Client_data['Asset_age'] = current_year - Client_data['asset_manufacture_year']


# Calculating the Number of Months of GST & ABN
Client_data['gst_registered_date'] = pd.to_datetime(Client_data['gst_registered_date'], format='%d-%m-%Y')
Client_data['abn_registered_date'] = pd.to_datetime(Client_data['abn_registered_date'], format='%d-%m-%Y')

# Calculate the number of months from gst_registered_date to the current date
current_date = pd.to_datetime(datetime.now().strftime('%d-%m-%Y'))

# Calculate the difference in months
Client_data['GST(Months)'] = (current_date.year - Client_data['gst_registered_date'].dt.year) * 12 + (current_date.month - Client_data['gst_registered_date'].dt.month)
Client_data['ABN(Months)'] = (current_date.year - Client_data['abn_registered_date'].dt.year) * 12 + (current_date.month - Client_data['abn_registered_date'].dt.month)

Client_data['Loan_Amount'] = Client_data['amount_financed'].copy()

#Dropping the unrevelent Columns
Client_data.drop([],)


PartData = Client_data[:10].copy()
# print(PartData.columns)
# print(PartData.head())
# print(PartData.to_dict(orient="records"))
Data_of_Rule_test = PartData.to_dict(orient="records")

# Check for right usage:
#   - approach = rule-engine
#   - approach = if-statements
if len(sys.argv) != 2:
    sys.exit("Usage: python main.py approach")
Result_Evalulated = []

Rules_by_Lender  = Rules_using_JSON('../data/Rules.json')
Rules_by_Lender.Create_rules_using_json()
for Data_rule in Data_of_Rule_test:
    # print('Date Rule :',Data_rule)
    for LenderName,LenderRule in Rules_by_Lender.lender_rules.items():
        temppte = copy.deepcopy(LenderRule)
        while temppte!=None:
            
            print("Rule ", temppte.Rule)
            # print("Eveluation : ",)
            # temppte.Rule.evaluate(Data_rule)
            # temppte.take_decisions(temppte.Rule)
            Evaluate_and_take_decision(temppte, temppte.Rule, Data_rule)
            print("The Evaluation Result is ",temppte.Rule.Evaluated_result)
            if not temppte.take_decisions(temppte.Rule) :
                break
            temppte = temppte.next_Rule

        if temppte == None:
            print(f"{Data_rule['application_number']} {LenderName} is an Eligible Lender ")
            Data_rule['Evaluated_Lender'] = LenderName
        else:
            Data_rule['Evaluated_Lender'] = "No Lender Found!"

exit()



R0 = Rule("111","Eligible_assets","in","'Agricultural machinery and equipment', 'Materials handling/forklifts', 'Access equipment (boom/scissor lifts)', 'Light trucks <3.5 tonnes', 'Heavy trucks >3.5 tonnes', 'Trailers and buses/coaches', 'Commercial motor vehicles', '(utes, vans and 4WDs)', 'Construction and earth moving', 'equipment (non-mining)'",1,False,"","Flexi up to $20K",Flow_for_True=True, Flow_for_False=True)
ABN0 = Rule("111","ABN(Months)", ">", 24,1,False,"","Flexi up to $20K", Flow_for_True=True)
GST0 = Rule("111","GST(Months)", ">", 24,1,False,"","Flexi up to $20K", Flow_for_True=True)
Max_Loan_amount0 = Rule("111", "loan Amount", "<", 20000, 1, False, None, "Flexi up to $20K",Flow_for_True=True)
# ID, Rule_header,Rule_operator, Rule_value, Rule_order, Is_Nested, Nested_Rule, Rule_parent,logical_operator="and", Flow_for_True=False, Flow_for_False=False, Terminate=False):

R2   = Rule("111","Eligible_assets","in","'trailers', 'buses', 'forklifts', 'material handling', 'yelow goods', 'earthmoving equipment', 'wheeled construction equipment', 'agricultural equipment'",1,False,"","Flexi up to $20K",Flow_for_True=True, Flow_for_False=True)
ABN2 = Rule("111","ABN(Months)", ">", 60,1,False,"","Flexi up to $20K", Flow_for_True=True)
GST2 = Rule("111","GST(Months)", ">", 36,1,False,"","Flexi up to $20K", Flow_for_True=True)
Max_Loan_amount2 = Rule("111", "loan Amount", "<", 20000, 1, False, None, "Flexi up to $20K",Flow_for_True=True)

R3 = Rule("111","Eligible_assets","in","'Motor vehicles', 'Passenger vehicles', 'Light trucks', 'Light commercial vehicles (van, utes)', 'Classic cars (loadings apply)', 'Motorbikes', 'Primary assets', 'Heavy trucks >4.5T GVM', 'Trailers', 'Buses and coaches', 'Small yellow goods and excavators', 'Construction and earth moving equipment', 'Farming and agriculture', 'Materials handling and access equipment', 'Prime movers (loadings apply)', 'Caravans'",1,False,"","Flexi up to $20K",Flow_for_True=True, Flow_for_False=True)
ABN3 = Rule("111","ABN(Months)", ">", 24,1,False,"","Flexi up to $20K", Flow_for_True=True)
GST3 = Rule("111","GST(Months)", ">", 24,1,False,"","Flexi up to $20K", Flow_for_True=True)
Max_Loan_amount3 = Rule("111","loan Amount","<",250000,1, False, None, "Flexi up to $20K",Flow_for_True=True)


{
    "Flexi_up_to_20K" : Rule_Connection(27001,R0,Rule_Connection(27002,ABN0,Rule_Connection(27003,GST0, Rule_Connection(27004,Max_Loan_amount0)))),
    "Pepper_Tier_A" : Rule_Connection(7001,R2,Rule_Connection(7002,ABN2,Rule_Connection(7003,GST2, Rule_Connection(27004,Max_Loan_amount2)))),
    "Resimac- low doc" : Rule_Connection(7001,R3,Rule_Connection(7002,ABN3,Rule_Connection(7003,GST3, Rule_Connection(27004,Max_Loan_amount3))))
}    


Data_of_Rule_test = {
    "ID" : 1001,
    "Eligible_assets" : "Passenger vehicles",
    "Excluded_Assets" : "food trucks",
    "Used_assets" : "true",
    "Private_sale" : "False",
    "Age_in_months_of_ABN" : 5,
    "Age_in_month_of_GST" : 1,
    "LoanType" : "Primary",
    "Asset_age" : 5,
    "Borrowering_for_months" : 55,
    "ABN(Months)":27,
    "GST(Months)":30,
    "Loan_Amount":15000
}

# print(R1)
# R_I1 = Rule("112","Eligible_assets","==","EV Car",1,False,"","Flexi up to $20K")
# RI1 = Rule("113","Asset_age",">",3,7,True,R_I1,"Flexi up to $20K")
# RN1 = Rule("114", "Borrowering_for_months", "<=", 60, 1, True, RI1, "Flexi up to $20K")

# ROP = Rule("111","Used_assets","true","==",1,False,"","Flexi up to $20K")

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


