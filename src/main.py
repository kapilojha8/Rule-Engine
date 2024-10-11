import sys
import copy
from Rules_using_JSON import  Rules_using_JSON
from Rules_using_XML import RulesUsingXML
import pandas as pd
from datetime import datetime
from preprocessing_of_data import PreprocessingOfData
from Rule_XML_Parser import Rules_XML_Parser

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
    Rules_by_Lender  = False 
    # RulesUsingXML('../data/Lenders XML/output.xml', '../data/Lenders XML/output.xsd')
    Rules_by_Lender = Rules_XML_Parser('../data/Lenders XML/output.xml', '../data/Lenders XML/output.xsd')

    if not Rules_by_Lender:
        exit("Error while loading the Xml file")
    # Rules_by_Lender.create_rules_using_xml()
    Rules_by_Lender.create_rules_using_xml(Data_of_Rule_test)
    exit('Testing phase running')
else:
    sys.exit("Incorrect arguments. Did you mean: rule-engine or if-statements?")

Result_Evalulated = []
LenderInforPassed = {}
LenderInforPassedList = []
karna = 0
MotorAssetLenders = ['CARS', 'SOLE TRADER' ] #, 'TERTIARY', 'PRIMARY', 'SECONDARY'

if (sys.argv[1] == "rule-engine-JSON"):
    for Data_rule in Data_of_Rule_test:
        TempDict = {}
        count = 1
        LenderInforPassedTemp = {}
        LenderInforPassedTemp['application_number'] = Data_rule['application_number']

        for LenderName,LenderRule in Rules_by_Lender.lender_rules.items():
            TempDict[LenderName] = {}
            if (LenderName.upper().find(Data_rule['asset_category'].split("_")[0]) == -1) ^  (Data_rule['asset_category'].split("_")[0] in MotorAssetLenders):
                continue
            temppte = copy.deepcopy(LenderRule)
            remarks = ""
            Running_logs = ""
            while temppte!=None:
                Rule_evaluate = temppte.Rule.evaluate(Data_rule)
                Running_logs = Running_logs + " -- " + Rule_evaluate['Remark']  if Running_logs!="" else Rule_evaluate['Remark']
                # TempDict[LenderName] = {temppte.RC_ID:}
                TempDict[LenderName][temppte.RC_ID] = {"RC_ID": temppte.RC_ID}
                EATD = temppte.take_decisions(temppte.Rule)
                TempDict[LenderName][temppte.RC_ID]["RC_Result"] = Rule_evaluate['Return_result']   # Rule Condition Result
                TempDict[LenderName][temppte.RC_ID]["Remark"] = Rule_evaluate['Remark']
                if not EATD :
                    break
                temppte = temppte.next_Rule

            if temppte == None:
                TempDict[LenderName]['Eligibility'] = True 
                LenderInforPassedTemp[f"Lender{count}"] = LenderName
                Data_rule['Evaluated_Lender'] = LenderName
                count += 1
                print("Passed!")
            else:
                TempDict[LenderName]['Eligibility'] = False
                LenderInforPassedTemp[f"Lender{count}"] =  LenderName +" : "+ Rule_evaluate['Remark'].split('||')[-1]
                Data_rule['Evaluated_Lender'] = "No Lender Found!"
                count += 1
                print("Failed")
        if LenderInforPassedTemp.get("Lender1"):
            karna+=1
        LenderInforPassedList.append(LenderInforPassedTemp)
elif (sys.argv[1] == "rule-engine-XML"):
    # print("Rules by lender: ",Rules_by_Lender.lender_rules)
    for Data_rule in Data_of_Rule_test:
        TempDict = {}
        count = 1
        LenderInforPassedTemp = {}
        LenderInforPassedTemp['application_number'] = Data_rule['application_number']
        for LenderName,LenderRules in Rules_by_Lender.lender_rules.items():
            for RuleName,LenderRule in LenderRules.items():
                TempDict[LenderName] = {}
                print(LenderName.upper(), Data_rule['asset_category'], RuleName)
                if (RuleName.upper().find(Data_rule['asset_category'].split("_")[0]) == -1) ^  (Data_rule['asset_category'].split("_")[0] in MotorAssetLenders):
                    continue
                temppte = copy.deepcopy(LenderRule)
                remarks = ""
                Running_logs = ""
                while temppte!=None:
                    Rule_evaluate = temppte.Rule.evaluate(Data_rule)
                    Running_logs = Running_logs + " -- " + Rule_evaluate['Remark']  if Running_logs!="" else Rule_evaluate['Remark']
                    TempDict[LenderName][temppte.RC_ID] = {"RC_ID": temppte.RC_ID}
                    EATD = temppte.take_decisions(temppte.Rule)
                    TempDict[LenderName][temppte.RC_ID]["RC_Result"] = Rule_evaluate['Return_result']   # Rule Condition Result
                    TempDict[LenderName][temppte.RC_ID]["Remark"] = Rule_evaluate['Remark']
                    if not EATD :
                        break
                    temppte = temppte.next_Rule
                if temppte == None:
                    TempDict[LenderName]['Eligibility'] = True 
                    LenderInforPassedTemp[f"Lender{count}"] = LenderName
                    Data_rule['Evaluated_Lender'] = LenderName
                    print("Passed!")
                    count += 1
                else:
                    TempDict[LenderName]['Eligibility'] = False
                    LenderInforPassedTemp[f"Lender{count}"] =  LenderName +" : "+ Rule_evaluate['Remark'].split('||')[-1]
                    Data_rule['Evaluated_Lender'] = "No Lender Found!"
                    print("Failed!")            
                    count += 1

    # print("LenderInforPassedTemp : ",LenderInforPassedTemp)



# dfe = pd.DataFrame(LenderInforPassedList)
# dfe.to_csv("../data/dataExtracted/ExpotedLendersInfor.csv",index=False)

# OgData = pd.read_csv("../data/Data from Client.csv")
# ThisDt = OgData.merge(dfe,on="application_number")
# ThisDt.to_csv("../data/dataExtracted/Report on Rule Engine.csv",index=False)