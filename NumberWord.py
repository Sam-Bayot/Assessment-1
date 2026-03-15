#File: NumberWord.py
#Description: Converts numbers into words
#Author: Sam Bayot
#Last Modified: 16/03/26

import math
import decimal
import BiClass

#-----Constants-----

#Special numbers is for numbers that don't follow the normal logic for number to word conversion
SPECIAL_NUMBERS: dict[int, str] = {0: "ZERO", 10: "TEN", 11: "ELEVEN", 12: "TWELVE", 14: "FOURTEEN"}
ONES_PLACE: BiClass.BiList[str] = BiClass.BiList["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"])
TENS_PLACE: BiClass.BiList[str] = BiClass.BiList["", "TEN", "TWEN", "THIR", "FOR", "FIF", "SIX", "SEVEN", "EIGH", "NINE"])
PLACES: BiClass.BiList[str] = BiClass.BiList(["", "THOUSAND", "MILLION", "BILLION", "TRILLION", "QUADRILLION", "QUINTILLION"])

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
        decimal_part = int(str(decimal.Decimal(str(abs(number_to_turn))) % 1).replace("0.", ""))
    
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

    chunk_amount: int = math.ceil(len(number_as_list) / 3)
    
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
            chunk_number += 

input(number_to_word(-2613856123.89312))
