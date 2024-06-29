import re
from action_verbs_storage import *
import random



def remove_non_number_characters(input_string):
    """
    Removes all non-digit characters from a string except for decimal points (.).

    Args:
    input_string: The string from which to remove non-digit characters.

    Returns:
    The string with only digits and decimal points.
    """
    if not input_string:
        return input_string
    if input_string and input_string[-1] == '.':
        string = input_string[:-1]  # Slice to exclude the last character
    else:
        string = input_string
    return re.sub(r"[^\d.]", "", string)


def remove_punctuation_or_parentheses_from_word(word):
    while word and word[-1] in '.?!,:;\'"()[]{}':
        word = word[:-1]
    while word and word[0] in '([{':
        word = word[1:]
    return word

def has_digits_and_decimal(word):
    
    if not word:
        return False
    parts = word.split('.')

    return any(part.isdigit() for part in parts)


def find_digit_words(text):
    """
    Finds all words in the text that contain at least one digit.

    Args:
        text: The text string to analyze.

    Returns:
        A set of words containing at least one digit.
    """
    digit_words = set()  # Create an empty set to store digit words
    for word in text.split():  # Iterate over words in the TextBlob
        if not word:
            continue

    cleaned_word = remove_punctuation_or_parentheses_from_word(remove_non_number_characters(word))  # Remove non-number characters and well non number pre or postfixes
    
    if has_digits_and_decimal(cleaned_word):  # Check if the cleaned word consists only of digits
        digit_words.add(cleaned_word)  # Add the original word (with potential non-digits) to the set
    return digit_words




def replace_words_with_spaces_in_output(description, generated_llm_output):
    """
    Replaces all the numbers that are in the generated output but not in the description with ____ while
    marinating prefixes and postfixes from generated output

    Args:
        description: The description entered by the user
        generated_llm_output: The generated output from the llm

    Returns:
        The updated description with blank spaces instead of created numbers
    """
    new_llm_output = generated_llm_output
    numbers_in_description = find_digit_words(description)
    for word in new_llm_output.split():
        cleaned_word = remove_punctuation_or_parentheses_from_word(remove_non_number_characters(word))
        if cleaned_word not in numbers_in_description and has_digits_and_decimal(cleaned_word):
            prefix = ""
            postfix = ""
            if word[0] in ('$'):
                prefix = word[0]
            if word[-1] in ("%"):
                postfix = word[-1]
            replacement = prefix + "____(insert #)" + postfix
            new_llm_output = re.sub(word, replacement, new_llm_output, count=1)
    return new_llm_output



def remove_random_elements(arr):
    num_to_remove = int(len(arr) * 0.15)

    # Create a copy of the original array
    new_arr = arr[:]

    # Randomly remove elements from the copy
    for _ in range(num_to_remove):
        new_arr.pop(random.randrange(len(new_arr)))

    return new_arr

def filter_verbs(action_verbs, verbs_to_exclude):
    return [verb for verb in action_verbs if verb not in verbs_to_exclude]


