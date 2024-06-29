
def identify_past_tense_verbs(extra_circular_description, verb_tokens):
    verbs_with_tense = {}
    for token in verb_tokens:
        if token.pos_ == "VERB":
            tense = token.morph.get('Tense')
            if tense:  # Check if tense is not empty
                verbs_with_tense[token.text] = tense
    past_tense_verbs = []
    for verb, tense in verbs_with_tense.items():
        if tense and len(tense) > 0 and tense[0] == 'Past':
            past_tense_verbs.append(verb)

    return past_tense_verbs
