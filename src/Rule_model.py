

class Rule:
    def __init__(self, ID, Rule_header,Rule_operator, Rule_value, Rule_order, Is_Nested, Nested_Rule, Rule_parent,logical_operator=None,Logical_Rule=None, Flow_for_True=False, Flow_for_False=False, Terminate=False):
        self.ID = ID
        self.Rule_header = Rule_header
        self.Rule_value = Rule_value
        self.Rule_operator = Rule_operator
        self.Rule_order = Rule_order
        self.Is_Nested = Is_Nested
        self.Nested_Rule = Nested_Rule
        self.Rule_parent = Rule_parent
        self.logical_operator = logical_operator  # Can be 'and' or 'or'
        self.Logical_Rule = Logical_Rule

        self.Flow_for_True = Flow_for_True
        self.Flow_for_False = Flow_for_False
        self.Terminate = False
        self.Evaluated_result = False


    def __str__(self):
        # print("Rule Header is :", self.Rule_header,"This is logical operator to use !",self.logical_operator)
        if self.Rule_value==None and self.Rule_operator==None:
            return f"{self.Rule_header}"
        if self.logical_operator and self.Logical_Rule:
            return f"({self.Rule_header} {self.Rule_operator} {str(self.Rule_value)} {self.logical_operator} {str(self.Logical_Rule)})"
        if not self.Is_Nested:
            return f"{self.Rule_header} {self.Rule_operator} {str(self.Rule_value)}"
        if self.Rule_value!=None and self.Rule_operator!=None and self.Rule_value!=None:
            return f"{self.Rule_header} {self.Rule_operator} {str(self.Rule_value)}"
        
    def evaluate(self, data):
        if self.Rule_header not in data:
            raise ValueError(f"Header {self.Rule_header} not found in data.")
        
        actual_value = data[self.Rule_header]

        if self.Rule_operator == "==":
            result = actual_value == self.Rule_value
        elif self.Rule_operator == ">":
            result = actual_value > self.Rule_value
        elif self.Rule_operator == "<":
            result = actual_value < self.Rule_value
        elif self.Rule_operator == ">=":
            result = actual_value >= self.Rule_value
        elif self.Rule_operator == "<=":
            result = actual_value <= self.Rule_value
        elif self.Rule_operator == "in":
            self.Rule_value = self.Rule_value.split(",")
            # if(self.Rule_header == "Eligible_Applicant"):
            #     print("Actual Value is :",actual_value," Rule Value ",self.Rule_value)
            self.Rule_value = [Rule_value.casefold().strip() for Rule_value in self.Rule_value]
            result = actual_value.casefold() in self.Rule_value
        else:
            raise ValueError(f"Unsupported operator: {self.Rule_operator}")
        
        if self.Is_Nested and self.Nested_Rule:
            if self.logical_operator == "and":
                result = result and self.Nested_Rule.evaluate(data)
            elif self.logical_operator == "or":
                result = result or self.Nested_Rule.evaluate(data)
        self.Evaluated_result = result
        return result



    def __and__(self, other):
        """
        Combine this rule with another rule using AND logic
        """
        # self, ID, Rule_header, Rule_value, Rule_operator, Rule_order, Is_Nested, Rule, Rule_parent,logical_operator="and"):
        combined_rule = Rule(
            ID=max(self.ID, other.ID) + "1",
            Rule_header=f"({self}) and ({other})",
            Rule_value=None,
            Rule_operator=None,
            Rule_order=None,
            Is_Nested=False,
            Nested_Rule=None,
            Rule_parent=other,
            logical_operator="and"
        )
        return combined_rule

    def __or__(self, other):
        """
        Combine this rule with another rule using OR logic
        """
        combined_rule = Rule(
            ID=max(self.ID, other.ID) + "1",
            Rule_header=f"({self}) or ({other})",
            Rule_value=None,
            Rule_operator=None,
            Rule_order=None,
            Is_Nested=False,
            Nested_Rule=None,
            Rule_parent=other,
            logical_operator="or"
        )
        return combined_rule


class Rule_Connection: ## Rules Linked List
    def __init__(self, ID, Rule, next_Rule=None):
        self.RC_ID = ID
        self.Rule = Rule
        self.next_Rule = next_Rule

    def __repr__(self):
        return f'Rule_Connection({self.RC_ID!r}, {self.Rule!r}, {self.next_Rule})'

    # def take_decisions(self,rule:Rule):
    #     if rule.Flow_for_True == rule.Evaluated_result == True:
    #         return True
    #     elif rule.Flow_for_True == True and rule.Evaluated_result == False:
    #         return False
    #     elif rule.Flow_for_True == rule.Evaluated_result == False:
    #         return False
    #     elif rule.Flow_for_True == False and rule.Evaluated_result == True:
    #         return False
        
    #     elif rule.Flow_for_False == True and rule.Evaluated_result == False:
    #         return True
    #     elif rule.Flow_for_False == rule.Evaluated_result == True:
    #         return True
    #     elif rule.Flow_for_False == False and rule.Evaluated_result == True:
    #         return False  ## >  Confirm this from sateesh sir
    #     elif rule.Flow_for_False == rule.Evaluated_result == False:
    #         return False  ## >  Confirm this from sateesh sir

    def take_decisions(self, rule: Rule):
        if rule.Evaluated_result:
            return rule.Flow_for_True
        else:
            return rule.Flow_for_False