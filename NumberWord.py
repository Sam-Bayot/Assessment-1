#File: NumberWord.py
#Description: Converts numbers into words
#Author: Sam Bayot
#Last Modified: 23/03/26

#-----Libraries-----

import time
import BiClass
import AutoCorrect

#-----Constants-----

#Special numbers is for numbers that don't follow the normal logic for number to word conversion
SPECIAL_NUMBERS: BiClass.BiDict[int, str] = BiClass.BiDict({0: "ZERO", 10: "TEN", 11: "ELEVEN", 12: "TWELVE", 14: "FOURTEEN"})
ONES_PLACE: BiClass.BiList[str] = BiClass.BiList("ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE")
TENS_PLACE: BiClass.BiList[str] = BiClass.BiList("", "TEN", "TWEN", "THIR", "FOR", "FIF", "SIX", "SEVEN", "EIGH", "NINE")
PLACES: list[str] = ["", "THOUSAND", "MILLION", "BILLION", "TRILLION", "QUADRILLION", "QUINTILLION", "SEXTILLION",
	                                "SEPTILLION", "OCTILLION", "NONILLION", "DECILLION", "UNDECILLION", "DUODECILLION", "TREDECILLION",
	                            "QUATTUORDECILLION", "QUINDECILLION", "SEXDECILLION", "SEPTENDECILLION", "OCTODECILLION", "NOVEMDECILLION",
	                        "VIGINTILLION", "UNVIGINTILLION", "DUOVIGINTILLION", "TRESVIGINTILLION", "QUATTUORVIGINTILLION", "QUINVIGINTILLION",
	                    "SEXVIGINTILLION", "SEPTEMVIGINTILLION", "OCTOVIGINTILLION", "NOVEMVIGINTILLION","TRIGINTILLION","UNTRIGINTILLION", "DUOTRIGINTILLION",
                     "TRETRIGINTILLION", "QUATTUORTRIGINTILLION", "QUINTRIGINTILLION", "SEXTRIGINTILLION", "SEPTENTRIGINTILLION", "OCTOTRIGINTILLION", "NOVEMTRIGINTILLION"]
VALID_WORD_LIST: list[str] = (list(SPECIAL_NUMBERS.forward_dict.values()) +
                            ONES_PLACE.forward_list +
                            [word + "TY" for word in TENS_PLACE[2:]] +
                            [word + "TEEN" for i, word in enumerate(TENS_PLACE) if i + 10 not in SPECIAL_NUMBERS] +
                            PLACES + ["NEGATIVE", "POINT", "HUNDRED", "AND"])
#The value of each place e.g million = 1000000
PLACE_VALUES: dict[str, int] = {place: 10 ** (3 * i) for i, place in enumerate(PLACES)}
#BK_TREE of every number word
BK_TREE: AutoCorrect.BKNode = AutoCorrect.list_to_BK_tree(VALID_WORD_LIST)
#-----Functions-----

#Converts a list of integers into an integer
def number_list_to_integer(number_list: list[int]) -> int:
    return int("".join([str(number) for number in number_list]))

#Converts an integer into a list of integers
def integer_to_number_list(integer: int) -> list[int]:
    return [int(digit) for digit in str(integer)]

#Converts a number into its word counterpart
def number_to_word(number_to_turn: str) -> str:

    #Splits the number into the integer and decimal parts
    def get_number_parts(number_as_str: str) -> list[str, str]:
        parts: list[str] = number_as_str.partition(".")
        return [parts[0], parts[2].rstrip("0")]
    
    number_word_list: list[str] = []
    number_parts: list[str, str] = get_number_parts(number_to_turn)
    
    #Sets the integer part to zero if it doesn't exist
    if not number_parts[0].strip("-"):
        number_parts[0] += "0"
    
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

    def decimal_to_word(integer_to_turn: str) -> str:
        #Adds the decimal part
        number_word_list.append("POINT")
        #Adds the ones place name for each digit in the decimal
        for curr_number in [int(digit) for digit in integer_to_turn]:
            number_word_list.append(ONES_PLACE[curr_number])
        return number_word_list


    #Adds 'NEGATIVE' if integer part is less than zero
    if number_parts[0][0] == "-":
        if not (number_parts[0] == "-0" and number_parts[1] == ""):
            number_word_list.append("NEGATIVE")
        number_parts[0] = number_parts[0].lstrip("-")

    #Converts the number into a list with each item corresponding to one digit
    number_as_list: list[int] = integer_to_number_list(number_parts[0])
    if len(number_as_list) > len(PLACES) * 3:
        raise ValueError("Number is too large!")
    chunk_amount: int = (len(number_as_list) + 2) // 3
    if number_as_list == [0]:
        chunk_amount = 0
        number_word_list.append("ZERO")
    digits_left: int = len(number_as_list)
    for i in range(chunk_amount):
        digit_amount: int = ((digits_left - 1) % 3) + 1
        index: int = len(number_as_list) - digits_left
        curr_chunk: list[int] = number_as_list[index:index+digit_amount]
        if set(curr_chunk) == {0}:
            continue
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
    if number_parts[1] != "":
        decimal_to_word(number_parts[1])
    
    #Returns the final words
    return " ".join(number_word_list)

#Converts word into its number counterpart
def word_to_number(word_to_turn: str) -> int | float:
    word_as_number: int = 0

    #Sanitises the word to turn by removing any unnecessary charaters that the user may input
    def sanitise_word_to_turn(word: str) -> str:
        return (
        word.upper()
        .replace("-", " ")
        .replace(",", "")
        .replace(" AND ", " ")
        .replace("\n", " ")
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
    auto_corrected_words: list[str] = []
    for word in word_to_turn.split():
        if word in VALID_WORD_LIST:
            auto_corrected_words.append(word)
            continue
        nodes: list[list[BKNode, Distance]] = BK_TREE.get_close_nodes(word, 5)[0]
        if not nodes:
            raise ValueError(f"{word} not found in BK_TREE")
        closest_node: str = nodes[-1]
        if closest_node and closest_node[0].word != "AND":
            auto_corrected_words.append(closest_node[0].word)
    word_as_list: BiClass.BiList[str] = BiClass.BiList(*auto_corrected_words)
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
    return float(word_as_number) if decimal_word_as_list else int(word_as_number)

"""-----TEST VALUE-----
Eiht Quattuortsrigintillion Too Hundrred Ansd Thwirty For Trtrigintsillion Twp Hundered Ands Forsty Threee Duotrigintillions Eighe Hundrred And Thierty Forur Untrigisntillion Eiht
Hundrsed Anwd Sity Fibe Trigintillon Too Hundrred Ansd Thorty none Novemviginiatillion Fur Husndred And Eihty Fiv Octovergintillion Spx Hundrsed And Twinty Throe Septemintillion Foulr
Hundreed Ad Sixy Eigt Sevigintillion Fice Hundreed An Teenty Thee Quniivgintillion Foure Hudred nd Fity Sux Quatorvigintillion Teo Humdred Amd Thorty Foor Threevigintillion Fove Humdred
Ad Tweenty Thee Duovirgintillion Fur Hunded Ad Thiryeen Unbogintillion Fiur Hunared Ad Teelve Vigibyillion Too Hunrred Ad Thorty For Noehmdecillion To Hudred An Thiorty Fou Octofcrillion
Ome Humrfed An Townty Thee Sepyerdecillion For Hunred Ad Eleeven Sexfecillion Tep Huvdred Ald Thurtt For Qiondecillion Ome Himdred Ane Sixyy euhht Quartoordecillion Thee Hunderd dna Tweenty
Oen Trecedikkion Seevn Hunderd Ad Fitfy Too Doudecillino Thee Hunered Ad Foorty noe Undicillion Seen Hunred Ad Fiftty To Dceillion Threee Hudred Ad Forteen Nonollion Fibe Hunded Ad Sebenty
Two Octokkion Thee Hunddred Andd Foirten aeptollion Seeven Hudred Ad Thorty Too Sextpllion For gundred An Trelve quentillion Thee Hondred An Fourty
Ones Quadrilloim Fiev Huvdred Ans weventy Fiee Trolloon Seben Hunded Abd Trenty Thwee Bikkion Ohe Hondred Ahf rorty Fove Mokkion Seben Hurded Ad Teenty Thee thosugand Four hunsrde An Fitfeen
"""

def start_time_taken():
    return time.perf_counter()
def print_time_taken(start):
    return print(f"Time taken: {time.perf_counter() - start:.6f} seconds")

#Test function for converting words or numbers
def test():
    def get_word_to_number(user_input: str):
        #tries to turn the word into a number
        number = word_to_number(user_input)
        try:
            start = start_time_taken()
            number = word_to_number(user_input)
            #If the words are invalid or nothing is inputted then print invalid input
            if number == 0 and user_input.strip().upper() != "ZERO":
                print("Invalid input!")
            else:
                print(number)
                print_time_taken(start)
        except:
            #If a word isn't correct print invalid input
            print(f"Invalid input!")

    #Prints out the distances of close words to 'word'
    def get_word_string_transform_distances(word: str):
        for node, distance in BK_TREE.get_close_nodes("word", 5)[0]:
            print(node.word, distance.string_transform_distance)
    
    while True:
        user_input = input("Input word or number to convert: ")
        #Tries to set user input to a float
        try:
            print(number_to_word(user_input).title())
        except ValueError as e:
            if str(e) == "Number is too large!":
                print(e)
                continue
            else:
                get_word_to_number(user_input)
        except:
            get_word_to_number(user_input)

#-----Main-----
            
if __name__ == "__main__":
    
    test()
