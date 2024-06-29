from spellchecker import SpellChecker
import pyinflect
from action_verb_storage import lemmatized_action_verbs_to_use


def inflect_verb(verb_tense, second_verb, nlp_model):
    doc = nlp_model(second_verb)
    token = doc[0]
    inflected_verb = token._.inflect(verb_tense)
    if not inflected_verb:
        return second_verb
    return inflected_verb

def inflect_verbs_in_tuples(tuples, verb_tense, nlp_model):
    inflected_tuples = []
    for tuple in tuples:
        first_value = tuple[0] 
        inflected_verb = inflect_verb(verb_tense, first_value, nlp_model=nlp_model)
        inflected_tuples.append((inflected_verb, tuple[1]))
    return inflected_tuples


def similarity_without_context(word1, word2, nlp_model):
    token1 = nlp_model(word1)
    token2 = nlp_model(word2)
    similarity = token1.similarity(token2)
    return similarity

def find_top_k_nearest_verbs(lemmatized_verb, lemmatized_set_of_verbs_to_choose_from, k, nlp_model):
    verb_similarity_pairs = [] #tuples of verbs and similarity to input verb
    for potential_verb in lemmatized_set_of_verbs_to_choose_from:
        similarity_of_verbs = similarity_without_context(lemmatized_verb, potential_verb,nlp_model=nlp_model)
        verb_similarity_pairs.append((potential_verb, similarity_of_verbs))
    sorted_verb_similarity_pairs = sorted(verb_similarity_pairs, key=lambda x: x[1], reverse=True)
    return sorted_verb_similarity_pairs[:k]

def extract_verbs_from_description(description, nlp_model):
    doc = nlp_model(description)
    verbs = []
    for token in doc:
        if token.pos_ == "VERB":
            verbs.append(token.text)
        elif token.text.istitle():
            # If the token is capitalized and not a proper noun, create a new token with lowercase
            lowercase_token = token.text[0].lower() + token.text[1:]
            doc_lower = nlp_model(lowercase_token)
            for lower_token in doc_lower:
                if lower_token.pos_ == "VERB":
                    verbs.append(token.text)
    return verbs


spell = SpellChecker()
def spelled_correctly_check(description):
    misspelled = spell.unknown(description.split())
    return len(misspelled) > 0




def return_suggested_action_verbs(description, verb_tokens, action_verbs_already_used, nlp_model):
    suggested_updates = {}
    if len(verb_tokens) == 0: # if there are no verbs in the description return the suggested verbs to use
        sorted_verb_similarity_pairs = find_top_k_nearest_verbs(description, lemmatized_action_verbs_to_use, 3, nlp_model=nlp_model)
        return {
                    "suggested updates": None, 
                    
                    "suggested_other_verbs_to_use": sorted_verb_similarity_pairs, 

                    "no_verbs_in_description_error": True
                }
    for token in verb_tokens:
        lemmatized_verb = token.lemma_ # lemma does correct spelling
        verb_tense = token.tag_
        if token.pos_ != "VERB":
            continue
        spell_check_warning = spelled_correctly_check(token.text)
        if lemmatized_verb not in lemmatized_action_verbs_to_use:
            suggested_replacements = find_top_k_nearest_verbs(lemmatized_verb, lemmatized_action_verbs_to_use, 3, nlp_model=nlp_model)
            inflected_suggested_replacements = inflect_verbs_in_tuples(verb_tense=verb_tense,tuples=suggested_replacements, nlp_model=nlp_model) # make it right tense
            suggested_updates[token.text] = {"suggested_replacements": inflected_suggested_replacements, "spell_check_warning": spell_check_warning}
        else:
            continue
        suggested_other_verbs_to_use = None
        if len(verb_tokens) + len(action_verbs_already_used) < 4: 
            suggested_general_verbs_to_use = find_top_k_nearest_verbs(description, lemmatized_action_verbs_to_use, 3, nlp_model=nlp_model)

    return {
                "suggested_updates": suggested_updates,

                "suggested_other_verbs_to_use": suggested_other_verbs_to_use,

                "no_verbs_in_description_error": False
            }
