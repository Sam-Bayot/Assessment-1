#File: HelperFunctions.py
#Description: Helper functions for the assessment script
#Author: Sam Bayot
#Last Modified: 11/03/26

import NumberWord

#Gets inputs from the user until they input a valid option, then returns the valid option 
def get_option(question: str, error_message = "Invalid Option!", sanitise_functions: list[callable] = [], valid_answers: list = [], answers_as_range: range = None) -> any:
    #Keeps asking for inputs until a valid option is given
    while True:
        answer = input(f"{question}\n")
        try:
            #Changes the answer by applying functions to the answer
            for function in sanitise_functions:
                answer = function(answer)
        except:
            print(error_message)
            continue
        #Returns the answer if valid else prints the error message
        if answer in valid_answers or answer in answers_as_range:
            return answer
        else:
            print(error_message)

get_option("Input a number between 1-10", error_message="Input a number between 1-10!", valid_answers=["w", "e", "n", "s"], sanitise_functions=[int], answers_as_range=range(1, 11))
print(NumberWord.number_to_word(16723).lower())
