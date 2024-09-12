import sys
from Loan_attributions import Actions, Class, Allocations, DataHandler
from Rule_model import Rule,Rule_Connection
import copy
from Rules_using_JSON import  Rules_using_JSON
from Rules_using_XML import RulesUsingXML
import pandas as pd
from datetime import datetime
from preprocessing_of_data import PreprocessingOfData


Preprocessed_data = PreprocessingOfData(csv_file_path="../data/Data from Client.csv", ClientDataDict=False)
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
    TempDict = {}
    for LenderName,LenderRule in Rules_by_Lender.lender_rules.items():
        TempDict[LenderName] = {}
        # print("The Lender Name is :",LenderName)
        if LenderName.upper().find(Data_rule['asset_category'].split("_")[0]) == -1:
            continue
        temppte = copy.deepcopy(LenderRule)
        remarks = ""
        Running_logs = ""
        while temppte!=None:
            Rule_evaluate = temppte.Rule.evaluate(Data_rule)
            Running_logs = Running_logs + " -- " + Rule_evaluate['Remark']  if Running_logs!="" else Rule_evaluate['Remark']
            # TempDict[LenderName] = {temppte.RC_ID:}
            TempDict[LenderName]["RC_TD"] = temppte.RC_ID
            EATD = temppte.take_decisions(temppte.Rule)
            if not EATD :
                break
            if type(temppte.Rule.Remark) == int:
                remarks +=  Remarks[f'{temppte.Rule.Remark}']
            TempDict[LenderName]["RC_Result"] = Rule_evaluate['Return_result']
            TempDict[LenderName]["Remark"] = Rule_evaluate['Remark']
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


print("This si tempt dict", TempDict)