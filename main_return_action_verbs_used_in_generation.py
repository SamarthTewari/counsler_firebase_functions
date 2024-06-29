from firebase_functions import https_fn, storage_fn
from firebase_admin import initialize_app
from action_verb_storage import *
import spacy

nlp = spacy.load("en_core_web_sm")

def return_action_verbs_used_in_ai_generated_description(description: str, action_verbs: set) -> list:
    """
    This function finds action verbs from a set that are used in a description.

    Args:
    description: A string containing the description text.
    set_of_action_verbs: A set of strings representing the lemmatized action verbs to look for.

    Returns:
        A list containing the action verbs from the set_of_action_verbs that are found in the description.
    """

    # Process the description text
    doc = nlp(description)

    action_verbs_found = []
    for token in doc:
    
        if token.pos_.startswith("VERB"):
            lemma = token.lemma_.lower()
            if lemma in action_verbs:
                action_verbs_found.append(lemma)

    return action_verbs_found

#@https_fn.on_call()
def return_action_verbs_used_in_generated_extracurricular_description(req: https_fn.CallableRequest) -> any:
    trait_one = "Technical Skills"
    trait_two = "Creativity"
    verbs_trait_one = array_names_to_values_dict.get(trait_one)
    verbs_trait_two = array_names_to_values_dict.get(trait_two)
    description_trait_one = " Developed and customized database to manage team of ____(insert #) and track progress of ____(insert #) students, calculating impact of $125,000"
    description_trait_two = "Initiated and authored grant proposals to secure partnerships with international non-profits, founding new opportunities for English Empowered"
    
    verbs_used_for_trait_one = return_action_verbs_used_in_ai_generated_description(description_trait_one, verbs_trait_one)
    verbs_used_for_trait_two = return_action_verbs_used_in_ai_generated_description(description_trait_two, verbs_trait_two)
    
    return {
                "verbs_used_for_trait_one": verbs_used_for_trait_one,

                "verbs_used_for_trait_two": verbs_used_for_trait_two
            
            }
