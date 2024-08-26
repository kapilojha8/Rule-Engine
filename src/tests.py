import unittest
from students_attributions import Class, Allocations, DataHandler, Actions


class TestRulesMethods(unittest.TestCase):

    def setUp(self):
       

# Flexi up to $20K:
# 	Rule 1 Eligible assets:[Agricultural machinery and equipment,Materials handling/forklifts, Access equipment (boom/scissor lifts), Light trucks <3.5 tonnes, Heavy trucks >3.5 tonnes, Trailers and buses/coaches, Commercial motor vehicles (utes, vans and 4WDs), Construction and earth moving, equipment (non-mining)]
# 	Rule 2 Excluded Assets:[Passenger cars, SUVs]
# 	Rule 3 Used assets: True
# 	Rule 4 Private sale: True
# 	Rule 5 :Max age (years) of asset at end of term : 20 
# 		Rule 1 Asset age exception 1: trailers
# 			Rule 1 Max age (years) of asset at end of term- exception 1: 30
# 	Rule 6 Age (months) of ABN: 24

# Resimac- low doc:
# 	Rule 1 Eligible assets:[Passenger vehicles, Light trucks, Light commercial vehicles (van, utes), Classic cars (loadings apply), Motorbikes]
# 	Rule 2 Excluded Assets: [Electric or motor vehicle used for hire/rental purposes, food trucks]
# 	Rule 3 Used assets: True
# 	Rule 4 Private sale: True
# 	Rule 5 Max age (years) of asset at end of term : 20 
# 		Rule 1 Asset age exception 1: trailers
# 			Rule 1 Max age (years) of asset at end of term- exception 1: 30
# 		Rule 2 Asset age exception 1: trucks
# 			Rule 1 Max age (years) of asset at end of term- exception 1: 25
# 		Rule 3 Asset age exception 1: EVs
# 			Rule 1 Max age (years) of asset at end of term- exception 1: 12
# 	Rule 6 Age (months) of ABN: 24




       # Inputs
        rules = {
            # Rainbow High
            "Loan == 'Primary'": [
                "Eligible_assets in [Agricultural machinery and equipment,Materials handling/forklifts]",
                "Excluded_Assets not in [Passenger cars, SUVs]",
                "Used_assets == True",
                "Private_sale ==  True"
                "Age_in_months_of_ABN >= 24"
                "Age_in_month_of_GST >= 0"
            ],

            # Waterfalls School for Girls 
            "LoanType == 'Secondary'": [
                "Eligible_assets in [Passenger vehicles, Light trucks, Light commercial vehicles (van, utes), Classic cars, Motorbikes]",
                "Excluded_Assets not in [Electric or motor vehicle used for hire/rental purposes, food trucks]",
                "Used_assets == True",
                "Private_sale ==  True"
                "Age_in_months_of_ABN >= 24"
                "Age_in_month_of_GST >= 24"
            ]
        }
        actions =  Actions(
            logic = {
                0: Class("A"),
                1: Class("B"),
                2: Class("C")
            }
        )
        students = DataHandler(
            "C:/Users/ayar9/source/repos/Data/students_dataset.csv"
            ).load_students()
        
        # Allocations
        self.alloc = (Allocations({})
                      .allocate_students_rule_engine(actions, rules, students))

    def test_rainbow_high_rules(self):

        self.assertEqual(self.alloc[263], Class("A"))
        self.assertEqual(self.alloc[41], Class("B"))
        self.assertEqual(self.alloc[5], Class("C"))
        self.assertEqual(self.alloc[57], Class("D"))
        self.assertEqual(self.alloc[118], Class("E"))
        self.assertEqual(self.alloc[375], Class("F"))


    def test_waterfalls_school_for_girls_rules(self):

        self.assertEqual(self.alloc[374], Class("A"))
        self.assertEqual(self.alloc[42], Class("B"))
        self.assertEqual(self.alloc[348], Class("C"))
        self.assertEqual(self.alloc[282], Class("D"))
        self.assertEqual(self.alloc[30], Class("E"))
    
    def test_cape_coral_high_rules(self):

        self.assertEqual(self.alloc[250], Class("A"))
        self.assertEqual(self.alloc[335], Class("B"))
        self.assertEqual(self.alloc[127], Class("C"))
        self.assertEqual(self.alloc[39], Class("D"))
        self.assertEqual(self.alloc[175], Class("E"))
        self.assertEqual(self.alloc[204], Class("F"))


if __name__ == "__main__":
    unittest.main()
