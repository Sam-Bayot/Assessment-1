#File: HelperFunctions.py
#Description: Helper functions for the assessment script
#Author: Sam Bayot
#Last Modified: 11/03/26

def get_option(question: str, error_question = "Invalid Option!", sanitise_functions: list[callable] = [], valid_answers: list = [], answers_as_range: range = None) -> any:
    while True:
        answer = input(f"{question}\n")
        try:
            for function in sanitise_functions:
                answer = function(answer)
        except:
            print(error_question)
            continue
        if answer in valid_answers or answer in answers_as_range:
            return answer
        else:
            print(error_question)
get_option("Input a number between 1-10", error_question="Input a number between 1-10!", valid_answers=["w", "e", "n", "s"], sanitise_functions=[int], answers_as_range=range(1, 11))
