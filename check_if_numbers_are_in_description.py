import re

#USE THIS FOR BOTH EXTRACICULAR AND AWARDS SECTION
def remove_non_number_characters(input_string):
    # Use regular expression to find all numbers
    numbers_only = re.sub(r'\D', '', input_string)
    return numbers_only


def has_digits(word):
    return word.isdigit()
number_words = set([
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
    "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
    "hundred", "thousand", "million", "billion", "trillion"
])
number_places = set(["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth",
    "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth", "twentieth",
    "twenty-first"])


def is_year(string):
    try:
        number = int(string)
    except ValueError:
        return False
    return 2015 <= number <= 2030


def find_number_errors(extra_circular_description): 
    """

    COULD USE FUZZY MATCHING TO IMPROVE MAYBE BUT spell checker will underline

Analyzes an extracurricular activity description to identify the presence and representation of numbers.

Args:
    extra_curricular_description (str): The text description of an extracurricular activity.

Returns:
    tuple[bool, bool, int]: A tuple containing three elements:
        - represent_number_as_word_error (bool): True if a number is represented as a word (e.g., "three") in the description.
        - no_numbers_in_description_error (bool): True if no numbers are found in the description.
        - digitCount (int): The total number of digits found in the description.
"""

    words = extra_circular_description.split()
    digitCount = 0
    represent_number_as_word_error = False
    no_numbers_in_description_error = False
    word_causing_no_number_in_description_error = None
    for word in words:
        parts = word.split("-")
        for part in parts:
            if has_digits(remove_non_number_characters(part)) and not is_year(part):
                digitCount += 1
                break
            elif part in number_words or part in number_places:
                digitCount += 1
                represent_number_as_word_error = True
                word_causing_no_number_in_description_error = part
                break
    if digitCount < 1:
        no_numbers_in_description_error = True
    return (word_causing_no_number_in_description_error, no_numbers_in_description_error)
