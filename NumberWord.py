#File: NumberWord.py
#Description: Converts numbers into words
#Author: Sam Bayot
#Last Modified: 16/03/26

import math
import BiClass
import typing

#-----Constants-----

#Special numbers is for numbers that don't follow the normal logic for number to word conversion
SPECIAL_NUMBERS: BiClass.BiDict[int, str] = BiClass.BiDict({0: "ZERO", 10: "TEN", 11: "ELEVEN", 12: "TWELVE", 14: "FOURTEEN"})
ONES_PLACE: BiClass.BiList[str] = BiClass.BiList("ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE")
TENS_PLACE: BiClass.BiList[str] = BiClass.BiList("", "TEN", "TWEN", "THIR", "FOR", "FIF", "SIX", "SEVEN", "EIGH", "NINE")
PLACES: list[str] = ["", "THOUSAND", "MILLION", "BILLION", "TRILLION", "QUADRILLION", "QUINTILLION", "SEXTILLION",
	                                "SEPTILLION", "OCTILLION", "NONILLION", "DECILLION", "UNDECILLION", "DUODECILLION", "TREDECILLION",
	                            "QUATTUORDECILLION", "QUINDECILLION", "SEXDECILLION", "SEPTENDECILLION", "OCTODECILLION", "NOVEMDECILLION",
	                        "VIGINTILLION", "UNVIGINTILLION", "DUOVIGINTILLION", "TRESVIGINTILLION", "QUATTUORVIGINTILLION", "QUINVIGINTILLION",
	                    "SEXVIGINTILLION", "SEPTEMVIGINTILLION", "OCTOVIGINTILLION", "NOVEMVIGINTILLION","TRIGINTILLION","UNTRIGINTILLION", "DUOTRIGINTILLION"]
PLACE_VALUES: dict[str, int] = {place: 10 ** (3 * i) for i, place in enumerate(PLACES)}

#-----Functions-----

#Converts a list of integers into an integer
def number_list_to_integer(number_list: list[int]) -> int:
    return int("".join([str(number) for number in number_list]))

#Converts an integer into a list of integers
def integer_to_number_list(integer: int) -> list[int]:
    return [int(digit) for digit in str(integer)]
    
#Converts a number into its word counterpart
def number_to_word(number_to_turn: float) -> str:
    number_word_list: list[str] = []
    decimal_part: int = 0
    
    #Gets the decimal part from the float as an integer
    if not number_to_turn.is_integer():
        decimal_part = int(str(number_to_turn).partition(".")[2].rstrip("0"))    
    number_to_turn: int = int(number_to_turn)

    #Converts chunks of 1-3 digits into words
    def hundred_place_to_word(number_list: list[int]) -> None:
        #Fills the deadspace with zeros to prevent index out of range errors
        while len(number_list) < 3:
            number_list.insert(0, 0)

        #Does different logic for each place

        #Hundreds place logic
        curr_number = number_list[0]
        if curr_number != 0:
            number_word_list.append(f"{ONES_PLACE[curr_number]} HUNDRED")

        #Tens place logic
        curr_number = number_list[1]
        if curr_number != 0:

            #Appends the word 'AND' if the hundreds digit isn't zero
            if number_list[0] != 0:
                number_word_list.append("AND")

            #Different logic for when the tens place digit is one
            if curr_number == 1:

                #Checks if the number is a special number and appends the number if true
                remaining_number: int = number_list_to_integer(number_list[1:])
                if remaining_number in SPECIAL_NUMBERS:
                    number_word_list.append(SPECIAL_NUMBERS[remaining_number])
                else:
                    number_word_list.append(TENS_PLACE[number_list[-1]] + "TEEN")
                #Returns out of the function early since the ones place is ignored
                return
            else:
                number_word_list.append(TENS_PLACE[curr_number] + "TY")

        #Adds 'AND' if the hundreds and ones digit isn't zero
        elif number_list[0] != 0 and number_list[2] != 0:
            number_word_list.append("AND")

        #Ones place logic
        curr_number = number_list[2]
        if curr_number != 0:
            number_word_list.append(ONES_PLACE[curr_number])
    
    #Adds the decimal part
    def add_decimal_as_words() -> None:
        number_word_list.append("POINT")
        #Adds the ones place name for each digit in the decimal
        for curr_number in integer_to_number_list(decimal_part):
            number_word_list.append(ONES_PLACE[curr_number])

    #Adds 'NEGATIVE' if 'number_to_turn' is less than zero
    if number_to_turn < 0:
        number_word_list.append("NEGATIVE")
    #Turns 'number_to_turn' to positive
    number_to_turn = abs(number_to_turn)

    #Returns early if the number is a special number
    if number_to_turn in SPECIAL_NUMBERS:
        number_word_list.append(SPECIAL_NUMBERS[number_to_turn])
        return " ".join(number_word_list)

    #Converts the number into a list with each item corresponding to one digit
    number_as_list: list[int] = integer_to_number_list(number_to_turn)

    chunk_amount: int = (len(number_as_list) + 2) // 3
    
    digits_left: int = len(number_as_list)
    
    for i in range(chunk_amount):
        digit_amount: int = ((digits_left - 1) % 3) + 1
        index: int = len(number_as_list) - digits_left
        curr_chunk: list[int] = number_as_list[index:index+digit_amount]
        #Adds the word 'AND' if it is the last chunk and the hundreds digit is zero
        if chunk_amount - i == 1 and curr_chunk[0] == 0:
            number_word_list.append("AND")
        #Adds the chunk to the number word list
        hundred_place_to_word(curr_chunk)
        #Adds the place of the chunk e.g thousand, million or billion
        curr_place: str = PLACES[chunk_amount - i - 1]
        if curr_place != "":
            number_word_list.append(curr_place)
        digits_left -= digit_amount

    #Adds the decimal part
    if decimal_part != 0: add_decimal_as_words()

    #Returns the final words
    return " ".join(number_word_list)

#Converts word into its number counterpart
def word_to_number(word_to_turn: str) -> float:
    word_as_number: int = 0

    #Sanitises the word to turn by removing any unnecessary charaters that the user may input
    def sanitise_word_to_turn(word: str) -> str:
        return (
        word.upper()
        .replace("-", " ")
        .replace(",", "")
        .replace(" AND ", " ")
        )

    #Turns chunks of 3 digits and turns them into numbers
    def hundred_place_to_number(curr_chunk: list[str]) -> int:
        chunk_number: int = 0

        #Hundreds digit
        if "HUNDRED" in curr_chunk:
            chunk_number += ONES_PLACE[curr_chunk[0]] * 100
            del curr_chunk[:2]
        if not curr_chunk: return chunk_number
        #Tens digit
        curr_word: str = curr_chunk.pop(0)
        if curr_word in SPECIAL_NUMBERS:
            chunk_number += SPECIAL_NUMBERS[curr_word]
        elif curr_word in ONES_PLACE:
            chunk_number += ONES_PLACE[curr_word]
        #Removes the "TEEN" or "TY" to get it's index from the 'TENS_PLACE' list
        elif "TEEN" in curr_word:
            chunk_number += TENS_PLACE[curr_word.replace("TEEN", "")] + 10
        else:
            chunk_number += TENS_PLACE[curr_word.replace("TY", "")] * 10
            #Ones digit
            if curr_chunk: chunk_number += ONES_PLACE[curr_chunk[0]]
        return chunk_number

    word_to_turn = sanitise_word_to_turn(word_to_turn)
    word_as_list: BiClass.BiList[str] = BiClass.BiList(*word_to_turn.split())
    #Bool for whether the number is a negative or not
    is_negative: bool = word_as_list[0] == "NEGATIVE"
    #Removes the word negative if it exists
    if is_negative: word_as_list.pop(0)

    #Gets the decimal part if 'point' exists in the word list
    integer_word_as_list: list[str] = word_as_list
    decimal_word_as_list: list[str] = []
    if "POINT" in word_as_list:
        point_index: int = word_as_list["POINT"]
        integer_word_as_list = word_as_list[:point_index]
        decimal_word_as_list = word_as_list[point_index + 1:]
    #Clears the word as list since its not needed anymore and saves memory
    del word_as_list
    #Returns zero if there isn't any words after sanitising the words
    if not integer_word_as_list and not decimal_word_as_list: return 0

    chunk_list: list[list[str]] = []
    left_index: int = 0
    #Cuts the list into chunks of 3 words and its place e.g hundreds, thousands, millions
    for i, integer_word in enumerate(integer_word_as_list):
        if integer_word in PLACES:
            chunk_list.append(integer_word_as_list[left_index:i+1])
            left_index = i+1

    #Adds the final chunk which should be the hundreds to ones place
    chunk_list.append(integer_word_as_list[left_index:])
    #Handles each chunk and adds it to 'word_as_number' at 10 to the power of its place
    for i, chunk in enumerate(chunk_list):
        if i == len(chunk_list) - 1: break
        chunk_place: str = chunk.pop()
        word_as_number += hundred_place_to_number(chunk) * PLACE_VALUES[chunk_place]
    #Adds the final chunk which should be the hundreds to ones place
    word_as_number += hundred_place_to_number(chunk_list[-1])

    #Decimal Logic
    if decimal_word_as_list:
        word_as_number += float("." + "".join(str(ONES_PLACE[word]) for word in decimal_word_as_list))

    #Turns the number into a negative
    if is_negative: word_as_number *= -1
    return float(word_as_number)

#Test function for converting words or numbers
def test():
    while True:
        user_input = input("Input word or number to convert: ")
        #Tries to set user input to a float
        try:
            print(number_to_word(float(user_input)))
        except:
            #If there's an error, then try to turn the word into a number
            try:
                number = word_to_number(user_input)
                #If the words are invalid or nothing is inputted then print invalid input
                if number == 0 and user_input.strip().upper() != "ZERO":
                    print("Invalid input!")
                else:
                    print(number)
            except:
                #If a word isn't correct print invalid input
                print(f"Invalid input!")

#Only runs the test function if running this script
if __name__ == "__main__":
    test()
