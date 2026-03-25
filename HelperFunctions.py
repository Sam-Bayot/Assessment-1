#File: HelperFunctions.py
#Description: Helper functions for the assessment script
#Author: Sam Bayot
#Last Modified: 11/03/26

import NumberWord

class Condition:
    def __init__(self, check_function: callable, value_type: type | None = None, parameter_wrapper: tuple | None = None) -> None:
        self.check_function: callable = check_function
        self.value_type: type | None = value_type
        self.parameter_wrapper: tuple | None = parameter_wrapper

    def check_value(self, value: "self.value_type") -> bool:
        if self.value_type and not isinstance(value, self.value_type):
            try:
                value = self.value_type(value)
            except:
                return False
        if self.parameter_wrapper:
            valid_value: any = self.check_function(value, *self.parameter_wrapper)
        else:
            valid_value: any = self.check_function(value)
        if not isinstance(valid_value, bool):
            raise TypeError(f"{valid_value} of type {type(valid_value)} is not type bool!")
        else:
            return True

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
        for condition in or_conditions:
            if condition.check_value(user_input):
                valid_input = True
                break
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
    pass
