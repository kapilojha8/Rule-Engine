import sys
from Loan_attributions import Actions, Class, Allocations, DataHandler
from Rule_model import Rule,Rule_Connection
import copy
from Rules_using_JSON import  Rules_using_JSON
from Rules_using_XML import RulesUsingXML
import pandas as pd
from datetime import datetime
from src.preprocessing_of_data import PreprocessingOfData

def Evaluate_and_take_decision(Rule_chain, Rule, Data_rule):
    # print("The Rule is ",Rule)
    Rule.evaluate(Data_rule)
    # print("Evaluated Result : ",Rule.evaluate(Data_rule))
    # print("the Evaluation Result is :",Rule.Evaluated_result)
    # if Rule.Is_Nested and (not Rule.Evaluated_result):
    #     Rule.Evaluated_result = Evaluate_and_take_decision(Rule_chain, Rule.Nested_Rule, Data_rule)
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
        Running_logs = ""
        while temppte!=None:
            # EATD = Evaluate_and_take_decision(temppte, temppte.Rule, Data_rule)
            Rule_evaluate = temppte.Rule.evaluate(Data_rule)
            Running_logs = Running_logs + " -- " + Rule_evaluate['Remark']  if Running_logs!="" else Rule_evaluate['Remark']
            EATD = temppte.take_decisions(temppte.Rule)
            if not EATD :
                break
            if type(temppte.Rule.Remark) == int:
                remarks +=  Remarks[f'{temppte.Rule.Remark}']
            temppte = temppte.next_Rule

        if temppte == None:
            print(f">>> {Data_rule['application_number']} {LenderName} is an Eligible Lender ")
            print("This is tempte running Logs ",Running_logs)
            Data_rule['Evaluated_Lender'] = LenderName
        else:
            print(f"--> {Data_rule['application_number']} {LenderName} is not Eligible Lender ")
            print(f"Failure Remarks : {Rule_evaluate['Remark'].split('||')[-1]}")
            print("This is tempte running Logs ",Running_logs)
            Data_rule['Evaluated_Lender'] = "No Lender Found!"
exit()


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