# Importing necessary modules
import sys
import copy
import pandas as pd
from datetime import datetime
from preprocessing_of_data import PreprocessingOfData
from Rule_XML_Approach import Rule_XML_Approach

Preprocessed_data = PreprocessingOfData(csv_file_path="../data/Data from Client.csv", ClientDataDict=False)
Preprocessed_data.converting_df_to_dict()
Data_of_Rule_test = Preprocessed_data.Data_of_Rule_test
# Check for right usage:
#   - approach = rule-engine
#   - approach = if-statements

if len(sys.argv) != 2:
    sys.exit("Usage: python main.py approach")

if (sys.argv[1] == "rule-engine-XML"):
    Rules_by_Lender  = False 
    Rules_by_Lender = Rule_XML_Approach('../data/Lenders XML/output.xml', '../data/Lenders XML/output.xsd')

    if not Rules_by_Lender:
        exit("Error while loading the Xml file")
    # Rules_by_Lender.create_rules_using_xml()
    Rules_by_Lender.create_rules_using_xml(Data_of_Rule_test)
    print(Rules_by_Lender.lender_rules)
else:
    sys.exit("Incorrect arguments. Did you mean: rule-engine or if-statements?")