def is_acronym(word):
    letters = [char for char in word if char.isalpha()]
    if len(letters) < 2:
        return False  # If there are no letters, it's not an acronym
    capital_letters_count = sum(1 for char in letters if char.isupper())
    return capital_letters_count > 0.5 * len(letters)



def contains_acronyms(text):
    words = text.split()  # Split the text by spaces
    acronyms = [word for word in words if is_acronym(word)]
    return acronyms
