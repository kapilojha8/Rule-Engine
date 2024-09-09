import sys
from Loan_attributions import Actions, Class, Allocations, DataHandler
from Rule_model import Rule,Rule_Connection
import copy
from Rules_using_JSON import  Rules_using_JSON
from Rules_using_XML import RulesUsingXML
import pandas as pd
from datetime import datetime
from preprocessing_of_data import PreprocessingOfData

def Evaluate_and_take_decision(Rule_chain, Rule, Data_rule):
    Rule.evaluate(Data_rule)
    if Rule.Is_Nested and (not Rule.Evaluated_result):
        Rule.Evaluated_result = Evaluate_and_take_decision(Rule_chain, Rule.Nested_Rule, Data_rule)
    return Rule_chain.take_decisions(Rule)


Preprocessed_data = PreprocessingOfData("../data/Data from Client.csv")
Preprocessed_data.converting_df_to_dict()
Data_of_Rule_test = Preprocessed_data.Data_of_Rule_test
 
# Check for right usage:
#   - approach = rule-engine
#   - approach = if-statements

if len(sys.argv) != 2:
    sys.exit("Usage: python main.py approach")

if (sys.argv[1] == "rule-engine-JSON"):
    Rules_by_Lender  = Rules_using_JSON('../data/Rules.json')
    Rules_by_Lender.Create_rules_using_json()
    Remarks = Rules_by_Lender.Remarks
elif (sys.argv[1] == "rule-engine-XML"):
    Rules_by_Lender  = RulesUsingXML('../data/Rules_output.xml')
    Rules_by_Lender.create_rules_using_xml()
else:
    sys.exit("Incorrect arguments. Did you mean: rule-engine or if-statements?")

Result_Evalulated = []
for Data_rule in Data_of_Rule_test:
    for LenderName,LenderRule in Rules_by_Lender.lender_rules.items():
        # print("The Lender Name is :",LenderName)
        if LenderName.upper().find(Data_rule['asset_category'].split("_")[0]) == -1:
            continue
        temppte = copy.deepcopy(LenderRule)
        remarks = ""
        while temppte!=None:
            
            # print("Rule ", temppte.Rule)
            # print("Eveluation : ",)
            # temppte.Rule.evaluate(Data_rule)
            # temppte.take_decisions(temppte.Rule)
            Evaluate_and_take_decision(temppte, temppte.Rule, Data_rule)
            # print("The Evaluation Result is ",temppte.Rule.Evaluated_result)
            # print("The Flow for False is ",temppte.Rule.Flow_for_False)
            # print("The take Decisions were :",temppte.take_decisions(temppte.Rule))
            if not temppte.take_decisions(temppte.Rule) :
                break
            if type(temppte.Rule.Remark) == int:
                remarks +=  Remarks[f'{temppte.Rule.Remark}']
            temppte = temppte.next_Rule

        if temppte == None:
            print(f">>>>>>>>>---------{Data_rule['application_number']} {LenderName} is an Eligible Lender ")
            print(f"All Remarks : {remarks} ")
            Data_rule['Evaluated_Lender'] = LenderName
        else:
            print(f"--> {Data_rule['application_number']} {LenderName} is not Eligible Lender ")
            print(f"Failure Remarks : {temppte.Rule.Remark}")
            Data_rule['Evaluated_Lender'] = "No Lender Found!"
exit()


# application_number
# status
# settled_at
# amount_financed
# deposit_amount
# balloon_amount
# repayment_term_month
# applicant_entity_type
# asset_supplier_type
# asset_category
# asset_type
# asset_manufacture_year
# usage_type
# gst_registered_date
# abn_registered_date
# guarantor_1_residential_status
# lender_name
 

"""
  "Assets": {
          "Reference_field": "asset_type",
          "Rule_Operator": "in",
          "Field_Type": 4,
          "Is_Nested": true,
          "Nested_Rule": {
            "Reference_field": "asset_type",
            "Rule_Operator": "not in",
            "Field_Type": 4,
            "Is_Nested": false,
            "Flow_for_True": false,
            "Flow_for_False": true
          },
          "Flow_for_True": false,
          "Flow_for_False": true,
          "Remark": 1
        },

QF12108,DRAFTED_AMENDED,,60000,0,0,60,Trusts,Private,TERTIARY_ASSETS,Agricultural machinery and equipment,2021,USED,01-06-2014,01-04-2014,RENTING,Flexicommercial
QF12103,DRAFTED_AMENDED,,25000,0,0,60,Trusts,Private,TERTIARY_ASSETS,Aeroplane equipment,2021,USED,01-06-2015,01-04-2015,RENTING,Flexicommercial
QF12107,DRAFTED_AMENDED,,25000,0,0,60,Trusts,Private,TERTIARY_ASSETS,Agricultural machinery and equipment,2021,USED,01-06-2017,01-04-2017,RENTING,Flexicommercial
QF12057,DRAFTED_AMENDED,,108900,0,0,60,TRUSTS,DEALER,TERTIARY_ASSETS,BEAUTY_EQUIPMENT,2023,NEW,01-06-2015,01-04-2015,OWNING,Flexicommercial
QF12107,DRAFTED_AMENDED,,25000,0,0,60,Trusts,Private,TERTIARY_ASSETS,Agricultural machinery and equipment,2021,USED,01-06-2017,01-04-2017,RENTING,Flexicommercial
QF12108,DRAFTED_AMENDED,,60000,0,0,60,Trusts,Private,TERTIARY_ASSETS,Agricultural machinery and equipment,2021,USED,01-06-2014,01-04-2014,RENTING,Flexicommercial




"""