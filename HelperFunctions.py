#File: HelperFunctions.py
#Description: Helper functions for the assessment script
#Author: Sam Bayot
#Last Modified: 11/03/26

import NumberWord
import inspect

#Condition class for checking if a value passes
class Condition:
    def __init__(self, check_function: callable, value_type: type | None = None, parameter_wrapper: tuple = ()) -> None:
        self.check_function: callable = check_function
        self.parameter_amount: int = len(inspect.signature(self.check_function).parameters)
        self.value_type: type | None = value_type
        #Sets the parameter_wrapper using the set_parameter_wrapper function
        self.set_parameter_wrapper(parameter_wrapper)
        
    #Makes sure that the parameter wrapper has the correct amount of values
    def set_parameter_wrapper(self, parameter_wrapper: tuple) -> None:
        #Raises an error if the parameter amounts of check functin and parameter wrapper are different
        if len(parameter_wrapper) != self.parameter_amount - 1:
            raise TypeError(f"{self.check_function.__name__}() expects {self.parameter_amount - 1} values, but parameter wrapper has {len(parameter_wrapper)} values") 
        self.parameter_wrapper: tuple = parameter_wrapper
    
    #Checks if a value passes the check_function
    def check_value(self, value: any) -> bool:
        if self.value_type and not isinstance(value, self.value_type):
            try:
                value = self.value_type(value)
            except:
                return False
        #Adds the parameters at the end of the check_function if parameter_wrapper is set
        if self.parameter_wrapper:
            valid_value: any = self.check_function(value, *self.parameter_wrapper)
        else:
            valid_value: any = self.check_function(value)
        #Raises an error if valid_value isn't a bool
        if not isinstance(valid_value, bool):
            raise TypeError(f"{valid_value} of type {type(valid_value)} is not type bool!")
        else:
            return valid_value

#Gets inputs from the user until they input a valid option, then returns the valid option 
def get_option(question: str, or_conditions: list[Condition] = [], and_conditions: list[Condition] = [], error_message = "Invalid Option!", sanitise_functions: list[callable] = []) -> any:
    if not or_conditions and not and_conditions:
        raise ValueError("No Conditions Added!")
    #Keeps asking for inputs until a valid option is given
    while True:
        user_input: str = input(f"{question}\n")
        try:
            #Changes the user input by applying functions to the input
            for function in sanitise_functions:
                user_input = function(user_input)
        except:
            print(error_message)
            continue
        #Returns the user input if valid else prints the error message
        valid_input: bool = False
        #Checks if the input is a valid input for any of or_conditions passing
        for condition in or_conditions:
            if condition.check_value(user_input):
                valid_input = True
                break
        #The input is a valid input when passing all of and_conditions
        if valid_input:
            for condition in and_conditions:
                if not condition.check_value(user_input):
                    valid_input = False
                    break
        if valid_input:
            return user_input
        else:
            print(error_message)

if __name__ == "__main__":
    def test_function(var1, var2, var3, var4):
        pass
    print(Condition(isinstance, parameter_wrapper=(int,)).check_value("2"))
    
