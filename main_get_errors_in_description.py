from firebase_functions import https_fn, storage_fn
from firebase_admin import initialize_app
import spacy
from textblob import TextBlob
import pyinflect
import os
import json
import re
from identify_past_tense_verbs import identify_past_tense_verbs
from identify_complete_sentences import identify_complete_sentences
from explain_acronyms import contains_acronyms
from check_if_numbers_are_in_description import find_number_errors
from identify_subjective_words import identify_subjective_words_in_description
from action_verb_recommender import return_suggested_action_verbs
from spell_checker import spell_Checker
from action_verb_storage import lemmatized_action_verbs_to_use



initialize_app()
#
nlp_small = spacy.load("en_core_web_sm")

def extract_verb_tokens_from_description(description, nlp_model):
    doc = nlp_model(description)
    verbs = []
    for token in doc:
        if token.pos_ == "VERB":
            verbs.append(token)
        elif token.text.istitle():
            # If the token is capitalized and not a proper noun, create a new token with lowercase
            lowercase_token = token.text[0].lower() + token.text[1:]
            doc_lower = nlp_model(lowercase_token)
            for lower_token in doc_lower:
                if lower_token.pos_ == "VERB":
                    verbs.append(token)
    return verbs

def extract_all_non_action_verbs(verb_tokens): 
    non_action_verbs_tokens = []
    action_verbs_tokens = []
    for token in verb_tokens:
        lemmatized_verb = token.lemma_
        if lemmatized_verb in lemmatized_action_verbs_to_use:
            action_verbs_tokens.append(token)
        else:
            non_action_verbs_tokens.append(token)
    return (action_verbs_tokens, non_action_verbs_tokens)


@https_fn.on_call()
def get_errors_in_description(req: https_fn.CallableRequest) -> any: # TODO test out some more
    
    try:
        text = "Led a team of 25 to recruit and coordinate 500 tutors, teaching 1000 kids, generating $125,000 of value. Managed partnerships with Intl. non-profits."
        verb_tokens = extract_verb_tokens_from_description(description=text, nlp_model=nlp_small)
        action_verbs_non_action_verbs_tokens_tuple = extract_all_non_action_verbs(verb_tokens=verb_tokens)
        action_verbs_tokens = action_verbs_non_action_verbs_tokens_tuple[0]
        non_action_verb_tokens = action_verbs_non_action_verbs_tokens_tuple[1]
    
        action_verbs = []
        if len(verb_tokens) == 0 or len(action_verbs) < 3:  # if there are verbs to correct and not enough action verbs
            nlp_large = spacy.load("en_core_web_lg")
            action_verbs = return_suggested_action_verbs(description=text, verb_tokens=non_action_verb_tokens, 
                                                        action_verbs_already_used=action_verbs_tokens,
                                                        nlp_model=nlp_large)
        
        past_tense_verbs = identify_past_tense_verbs(text, verb_tokens=verb_tokens)
        
        
        complete_sentences = identify_complete_sentences(text, nlp_model=nlp_small)
        

        acronyms = contains_acronyms(text)
        
        number_errors = find_number_errors(text)
        
    
        subjective_words = identify_subjective_words_in_description(description=text, nlp_model=nlp_small)
        
        

        spelling_errors = spell_Checker(text) #ERROR HAPPENIG HERE

        # most of these functions if there is no value or empty value means no error
        
        errors = {
            "PAST TENSE VERB ERROR" : past_tense_verbs,
            "COMPLETE SENTENCE ERROR": complete_sentences,
            "ACRONYM ERROR": acronyms,
            "REPRESENT NUMBER AS WORD ERROR": number_errors[0],
            "NO NUMBER IN DESCRIPTION ERROR": number_errors[1],
            "SUBJECTIVE WORDS ERROR": subjective_words,
            "ACTION VERB ERRORS": action_verbs,
            "SPELLING ERRORS": spelling_errors
        } 
        print(errors)
        json_response = json.dumps(errors)
        return json_response
    except Exception as e:
        return {"error": str(e)}, 500
    
    # Do debugging
    #Try textblob libarary by it's self
    #potential fix to error https://github.com/googleapis/python-bigquery/issues/1170
    # check if it is actually text blob orthe function is causing errors
    # check if textblob needs to be imported here or smth to load?
