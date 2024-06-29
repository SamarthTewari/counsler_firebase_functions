from spellchecker import SpellChecker



spell = SpellChecker()

def spell_Checker(description):
    spell_check = []
    if description is None or not isinstance(description, str):
        return spell_check  # Return empty list if description is None or not a string
    
    words = description.split()
    if not words or len(words) == 0:
        return spell_check  # Return empty list if no words after splitting
    
    misspelled = spell.unknown(words)
    if not misspelled:
        return spell_check
    
    for word in misspelled:
        if word.istitle() or any(char.isdigit() for char in word):
            continue

        while word and word[-1] in '.?!,:;\'"()[]{}':
            word = word[:-1]
        
        # Remove leading punctuation
        while word and word[0] in '([{':
            word = word[1:]

        candidates = spell.candidates(word)
        if candidates is None:
            candidates = []  # Ensure candidates is an empty list if None
        
        most_likely_candidate = spell.correction(word)
        if most_likely_candidate == word:
            continue
        if most_likely_candidate is None:
            most_likely_candidate = word  # Use the original word if correction is None
        
        result = {
            "mis-spelled word": word,
            "correction": most_likely_candidate,
            "candidates": list(candidates)  # Ensure candidates is a list
        }
        spell_check.append(result)
    
    return spell_check
