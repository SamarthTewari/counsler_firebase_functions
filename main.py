from firebase_functions import https_fn, storage_fn
from firebase_admin import initialize_app
from firebase_functions.params import IntParam, StringParam
from description_generation import return_generated_extracurricular_description



initialize_app()



trait_one = "Technical Skills"
trait_two = "Creativity"
description = "Description:" \
    "Role: Founder and President English Empowered provides free one on one English tutoring for underprivileged students in India. Led a team of 25 to recruit and coordinate 500 tutors, teaching 1000 kids, generating $125,000 of value. Managed partnerships with Intl. non-profits."
verbs_not_to_use_trait_one = []
verbs_not_to_use_trait_two = []


#@https_fn.on_call()
def generate_personalized_extracurricular_description(req: https_fn.CallableRequest) -> any: # TODO FIND HOW TO HIDE ENVIORMENT VARIABLES!!
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return return_generated_extracurricular_description(
                trait_one=trait_one,
                trait_two=trait_two,
                description=description,
                verbs_not_to_use_trait_one=verbs_not_to_use_trait_one,
                verbs_not_to_use_trait_two=verbs_not_to_use_trait_two,
                temperature_setting=0.6
            )
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            else:
                print(f"Attempt {attempt + 1} failed: {e}. No more retries left.")
                raise