import csv
from rule_engine import Rule, Context, resolve_attribute
import re


class Class:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other): 
        return self.name == other.name


class Loan:
    
    def __init__(self, ID, Eligible_assets, Excluded_Assets, Used_assets, Private_sale, Age_in_months_of_ABN, Age_in_month_of_GST, LoanType):
        self.ID = ID
        self.Eligible_assets = Eligible_assets
        self.Excluded_Assets = Excluded_Assets
        self.Used_assets = Used_assets
        self.Private_sale = Private_sale
        self.Age_in_months_of_ABN = Age_in_months_of_ABN
        self.Age_in_month_of_GST = Age_in_month_of_GST
        self.LoanType = LoanType


class Actions:

    def __init__ (self, logic):
        self.logic = logic

    def compute_class(self, rules, rule):
        """
        Find the class that corresponds to a rule
        """
        print('The this is 37',rules.index(rule))
        return self.logic[rules.index(rule)]

    def match_ID_class(self, allocations, match_ID, rules, rule):
        """
        Add ID/class pairs to allocations
        """
        print('Rules and rule Are : ',rules,'and rule is ', rule)
        return allocations.setdefault(
            match_ID, self.compute_class(rules, rule)
        )
        

class Allocations:

    def __init__ (self, allocations):
        self.allocations = allocations

    @staticmethod
    def convert_rules_rule_engine(rules):
        """
        Convert into rule objects to be parsed by rule engine 
        """
        # Declare context
        context = Context(resolver=resolve_attribute)
        
        # Convert rules
        reng_rules = {}
        for parent_rule, child_rules in rules.items():

            # convert child rules to rules_engine rule
            reng_child_rules = []
            for child_rule in child_rules:
                reng_child_rules.append(Rule(child_rule, context=context))

            # convert child rules to rules_engine rule
            reng_rules[Rule(parent_rule, context=context)] = reng_child_rules
        
        return reng_rules

    @staticmethod
    def convert_rules_if_statements(rule):
        """
        Convert into rules to be evaluated
        """
        return re.sub(
            r'\b(Eligible_assets|Excluded_Assets|Used_assets|Private_sale|Age_in_months_of_ABN|Age_in_month_of_GST|LoanType)\b', 
            r'Loan.\1',
            rule
        )

    def allocate_Loans_rule_engine(self, actions, rules, Loans):
        """
        Allocate Loans to their respective classes using 
        rule engine
        """

        # Convert rule to "rule_engine" rule
        reng_rules = Allocations.convert_rules_rule_engine(rules)
        # Allocate Loans
        for parent_rule, child_rules in reng_rules.items():
            
            # Match Loans to parent rule
            matche1 = list(parent_rule.filter(Loans))
 
            for child_rule in child_rules:

                print('The Child Rule: ',child_rule)
                # Match Loans to child rules
                for match2 in child_rule.filter(matche1):

                    # Execute actions
                    actions.match_ID_class(
                        self.allocations, match2.ID, child_rules, child_rule
                    )

        return self.allocations


    def allocate_Loans_if_statements(self, rules, Loans):
        """
        Allocate Loans to their respective classes using 
        conditional branching
        """
        for Loan in Loans:
           
            # Evaluate parent rules
            if (eval(Allocations.convert_rules_if_statements(list(rules.keys())[0]))):

                # Evaluate child rules
                if (eval(Allocations.convert_rules_if_statements(list(rules.values())[0][0]))):
                    self.allocations[Loan.ID] = Class("A")

                elif (eval(Allocations.convert_rules_if_statements(list(rules.values())[0][1]))):
                    self.allocations[Loan.ID] = Class("B")

                else:
                    self.allocations[Loan.ID] = Class("F")

            elif (eval(Allocations.convert_rules_if_statements(list(rules.keys())[1]))):

                if (eval(Allocations.convert_rules_if_statements(list(rules.values())[1][0]))):
                    self.allocations[Loan.ID] = Class("A")

                elif (eval(Allocations.convert_rules_if_statements(list(rules.values())[1][1]))):
                    self.allocations[Loan.ID] = Class("B")

                else:
                    self.allocations[Loan.ID] = Class("F")

            else:

                if (eval(Allocations.convert_rules_if_statements(list(rules.values())[2][0]))):
                    self.allocations[Loan.ID] = Class("A")

                elif (eval(Allocations.convert_rules_if_statements(list(rules.values())[2][1]))):
                    self.allocations[Loan.ID] = Class("B")

                else:
                    self.allocations[Loan.ID] = Class("F")
                    
        return self.allocations

class DataHandler:
    
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_Loans(self):
        """
        Load data into a list of Loans objects
        """
        Loans = []
        with open(self.file_path, mode="r") as file:

            reader = csv.DictReader(file)

            # Load data from frile_path 
            for loan in reader:

                # Convert columns to appropriate data types
                loan = Loan(
                    int(loan["ID"]),
                    str(loan["Eligible_assets"]),
                    str(loan["Excluded_Assets"]),
                    str(loan["Used_assets"]),
                    str(loan["Private_sale"]),
                    int(loan["Age_in_months_of_ABN"]),
                    int(loan["Age_in_month_of_GST"]),
                    str(loan["LoanType"]),
                )
 
                # Add to Loans list
                Loans.append(loan)
                
        return Loans

    def save_Loans(self, input_path, output_path, allocations):
        """
        Append Loans dataset with allocated classes and
        save to output_path
        """
        with open(input_path, mode='r') as input_file, \
            open(output_path, mode='w', newline='') as output_file:
            
            reader = csv.DictReader(input_file)
            writer = csv.DictWriter(
                output_file, 
                fieldnames=reader.fieldnames + ["class"]
                )

            # Populate headers
            writer.writeheader()

            # Write data to output_path
            for row in reader:
                print("The row is ",row)
                row["class"] = allocations[int(row["ID"])].name
                writer.writerow(row)
