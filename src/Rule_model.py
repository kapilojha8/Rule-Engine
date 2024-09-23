from datetime import datetime
class Flow_exception:
    def __init__(self,Exception_rule, Remark, Condition_to_proceed=False) -> None:
        self.Exception_rule = Exception_rule
        self.Condition_to_proceed = Condition_to_proceed
        self.Remark = Remark

    def __str__(self) -> str:
        return f"Exception Rule : {self.Exception_rule} || Condition to proceed : {self.Condition_to_proceed} || Remark : {self.Remark}"

class Rule:
    def __init__(self, ID:str, Rule_header:str,Rule_operator:str, Rule_value, Field_Type,Flow_exception_True,Flow_exception_False, Is_Evaluating, logical_operator:str=None,Logical_Rule=None):
        """
            Initializes a Rule object with the provided attributes.

            Args:
                ID (str): Unique identifier for the rule.
                Rule_header (str): The attribute or field that the rule is based on.
                Rule_operator (str): The operator used in the rule (e.g., '>', '<', '==').
                Rule_value (Any): The value that the Rule_header is compared against.
                logical_operator (str, optional): Logical operator ('and', 'or') used between rules.
                Logical_Rule (Rule, optional): Additional logical rule for combined evaluation.
        """
        self.ID = ID
        self.Rule_header = Rule_header
        self.Rule_value = self.convert_value(Rule_value, Field_Type)
        self.Rule_operator = Rule_operator
        self.logical_operator = logical_operator  # Can be 'and' or 'or'
        self.Logical_Rule = Logical_Rule
        self.Is_Evaluating = Is_Evaluating
        self.Flow_Exception_for_True = Flow_exception_True
        self.Flow_Exception_for_False = Flow_exception_False
        self.Evaluated_result = None
        
    def convert_value(self, value, Field_Type):
        if Field_Type == 0 or Field_Type == '0':  # bool
            return bool(value)
        elif Field_Type == 1 or Field_Type == '1':  # date
            try:
                return datetime.strptime(value, "%d/%m/%Y")  # Assuming the date format is dd/mm/yyyy
            except ValueError:
                raise ValueError(f"Invalid date format for {value}. Expected format: dd/mm/yyyy")
        elif Field_Type == 2 or Field_Type == '2':  # float
            return float(value)
        elif Field_Type == 3 or Field_Type == '3':  # int                
            return int(value)
        elif Field_Type == 4 or Field_Type == '4':  # str
            return str(value)
        else:
            raise ValueError(f"Unknown Field_Type: {Field_Type}")


    def __str__(self):
        """
            Returns a string representation of the rule.

            Returns:
                str: A string that represents the rule, including logical operators if applicable.
        """
        if self.Rule_value==None and self.Rule_operator==None:
            return f"{self.Rule_header}"
        if self.logical_operator and self.Logical_Rule:
            return f"({self.Rule_header} {self.Rule_operator} {str(self.Rule_value)} {self.logical_operator} {str(self.Logical_Rule)})"
        if self.Rule_value!=None and self.Rule_operator!=None and self.Rule_value!=None:
            return f"{self.Rule_header} {self.Rule_operator} {str(self.Rule_value)}"

    def evaluate(self, data):
        """
            Evaluates the rule against provided data.

            Args:
                data (dict): The data dictionary containing values to be evaluated against the rule.

            Returns:
                bool: The result of the rule evaluation (True or False).
        """

        nested_remark = ""
        if self.Rule_header not in data:
            raise ValueError(f"Header {self.Rule_header} not found in data.")
        
        actual_value = data[self.Rule_header]
        
        # Handle date comparison
        if isinstance(actual_value, datetime) or isinstance(self.Rule_value, datetime):
            self.Rule_value = datetime.strptime(self.Rule_value, "%d/%m/%Y").date() if isinstance(self.Rule_value, str) else self.Rule_value
            actual_value = actual_value.date() if isinstance(actual_value, datetime) else actual_value
        
        try:
            if isinstance(self.Rule_value, str) and self.Rule_value.isdigit():
                self.Rule_value = int(self.Rule_value)
            if isinstance(actual_value, str) and actual_value.isdigit():
                actual_value = int(actual_value)
        except ValueError:
            raise ValueError(f"Cannot convert {self.Rule_value} or {actual_value} to int.")
        
        # Add additional operator support here
        if self.Rule_operator == "==":
            if isinstance(actual_value, str) and isinstance(self.Rule_value, str):
                result = actual_value.strip().lower() == self.Rule_value.strip().lower()
            else:
                result = actual_value == self.Rule_value
        elif self.Rule_operator == "!=":
            if isinstance(actual_value, str) and isinstance(self.Rule_value, str):
                result = actual_value.strip().lower() != self.Rule_value.strip().lower()
            else:
                result = actual_value != self.Rule_value
        elif self.Rule_operator == ">":
            result = actual_value > self.Rule_value
        elif self.Rule_operator == "<":
            result = actual_value < self.Rule_value
        elif self.Rule_operator == ">=":
            result = actual_value >= self.Rule_value
        elif self.Rule_operator == "<=":
            result = actual_value <= self.Rule_value
        elif self.Rule_operator == "in":
            if isinstance(self.Rule_value, str):
                self.Rule_value = [x.strip().lower() for x in self.Rule_value.split(",")]
            result = actual_value.strip().lower() in self.Rule_value
        elif self.Rule_operator == "not in":
            if isinstance(self.Rule_value, str):
                self.Rule_value = [x.strip().lower() for x in self.Rule_value.split(",")]
            result = actual_value.strip().lower() not in self.Rule_value
        else:
            raise ValueError(f"Unsupported operator: {self.Rule_operator}")
        
        if self.logical_operator:
            if self.logical_operator == "and":
                result = result and self.Logical_Rule.evaluate(data)['Return_result']
            elif self.logical_operator == "or":
                result = result or self.Logical_Rule.evaluate(data)['Return_result']
        
        if result:
            if self.Flow_Exception_for_True and self.Flow_Exception_for_True.Remark:
                nested_remark += self.Flow_Exception_for_True.Remark
            if self.Flow_Exception_for_True and self.Flow_Exception_for_True.Exception_rule:
                LLO = self.Flow_Exception_for_True.Exception_rule.evaluate(data)
                nested_remark = nested_remark+" || "+LLO['Remark'] if nested_remark != "" else LLO['Remark']
                result = LLO['Return_result']
        else:
            if self.Flow_Exception_for_False and self.Flow_Exception_for_False.Remark:
                nested_remark += self.Flow_Exception_for_False.Remark
            if self.Flow_Exception_for_False and self.Flow_Exception_for_False.Exception_rule:
                LLO = self.Flow_Exception_for_False.Exception_rule.evaluate(data)
                nested_remark = nested_remark+" || "+LLO['Remark'] if nested_remark != "" else LLO['Remark']
                result = LLO['Return_result']        
        self.Evaluated_result = result
        return {"Return_result": result, "Remark": nested_remark }

class Rule_Connection: ## Rules Linked List
    """
        Represents a connection between rules in a linked list-like structure.
    """
    def __init__(self, ID, Rule, next_Rule=None):
        self.RC_ID = ID
        self.Rule = Rule
        self.next_Rule = next_Rule
        self.Running_logs = ""

    def __repr__(self):
        """
            Returns a string representation of the rule connection.

            Returns:
                str: A string that represents the rule connection.
        """
        return f'Rule_Connection({self.RC_ID!r}, {self.Rule!r}, {self.next_Rule})'

    def  take_decisions(self, rule: Rule):
        """
            Determines the next action based on the evaluated result of the rule.
            Args:
                rule (Rule): The rule to be evaluated.
            Returns:
                bool: The decision to continue (True) or stop (False) based on the rule's evaluation.
        """
        if rule.Evaluated_result:
            return rule.Flow_Exception_for_True.Condition_to_proceed
        else:
            return rule.Flow_Exception_for_False.Condition_to_proceed
   