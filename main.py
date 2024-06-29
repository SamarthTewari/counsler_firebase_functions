'''from firebase_functions import https_fn, storage_fn
from firebase_admin import initialize_app
from firebase_functions.params import IntParam, StringParam'''
import requests
import re


initialize_app()



def count_characters(sentence):
    return len(sentence)
    

def get_response(text, num_return_sequences, num_beams):
    API_URL = "https://m0lhfo43ovuep844.us-east-1.aws.endpoints.huggingface.cloud"
    headers = {
        "Accept" : "application/json",
        "Authorization": "Bearer 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",
        "Content-Type": "application/json" 
    }

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    

    text_characters = count_characters(sentence=text)
    tokens = text_characters / 4
    max_tokens = int(tokens * 1)
    output = query({
        "inputs": text,
        "parameters": {
            "num_return_sequences": num_return_sequences,
            "max_length": max_tokens - 1
        }
    })
    return output



def extract_responses(dicts_of_responses):
    responses = []
    for item in dicts_of_responses:
        if isinstance(item, dict):  # Check if item is a dictionary
            responses.append(item.get("generated_text"))
    return responses





def categorize_responses_by_word_count(responses): 
    
    sorted_responses = sorted(responses, key=lambda x: len(x.split()), reverse=True)
    
    longest_response = sorted_responses[0] if len(sorted_responses) > 0 else None
    medium_response = sorted_responses[1] if len(sorted_responses) > 1 else None
    shortest_response = sorted_responses[2] if len(sorted_responses) > 2 else None
    
    return {
        "longest_response": longest_response,
        "medium_response": medium_response,
        "shortest_response": shortest_response
    }

def get_top_3_valid_responses(text, num_return_sequences, num_beams):
    top_3_valid_responses = []
    list_of_dicts = get_response(text, num_return_sequences, num_beams)
    responses = extract_responses(list_of_dicts)
    input_word_count = len(text.split())
    for response in responses:
        response_word_count = len(response.split())
        last_character = response[-1]
        if response_word_count < input_word_count and last_character in (".", "!", "?"): # check response isn't truncated
            top_3_valid_responses.append(response)
            if len(top_3_valid_responses) >= 3:
                break

    return categorize_responses_by_word_count(top_3_valid_responses)



def get_valid_paraphrase(text, num_return_sequences, num_beams):
    top_3_responses = get_top_3_valid_responses(text=text,num_return_sequences=num_return_sequences,num_beams=num_beams)
    longest_response = top_3_responses.get("longest_response")
    medium_response = top_3_responses.get("medium_response")
    shorter_response = top_3_responses.get("shortest_response") # if medium or shortest response does not exist that means there is no other valid responses in list but one so no need to check
    if longest_response:
        if shorter_response:
            return {"longer_response": longest_response, "shorter_response": shorter_response}
        elif medium_response:
            return {"longer_response": longest_response, "shorter_response": medium_response}
        else:
            return {"longer_response": longest_response, "shorter_response": None}
    else:
        return {}

    
def paraphrase_sentence(sentence, num_return_sequences, num_beams) -> any: #TODO test out

    response_for_longer_query = get_valid_paraphrase(text=sentence, num_return_sequences=num_return_sequences, num_beams=num_beams)
    if not response_for_longer_query: # if we dont have the longer response we trigger this.
        return {
            "longest": None,
            "medium": None,
            "shortest": None
        }
    
    if response_for_longer_query and response_for_longer_query.get("shorter_response"): # simple case we have the shorter response
        print("case 1")
        longest_response_to_return = response_for_longer_query.get("longer_response")
        medium_response_to_return = response_for_longer_query.get("shorter_response")
        short_response_query = get_valid_paraphrase(text=medium_response_to_return,num_return_sequences=num_return_sequences,num_beams=num_beams) # returns none if does not exist
        shortest_response_to_return = None
        if short_response_query:
            shortest_response_to_return = short_response_query.get("longer_response")
        return {
            "longest": longest_response_to_return,
            "medium": medium_response_to_return,
            "shortest": shortest_response_to_return
        }
    
    elif response_for_longer_query and not response_for_longer_query.get("shorter_response"): # we have a longer response but no shorter response to set as medium_response_to_return
        print("case 2")
        longest_response_to_return = response_for_longer_query.get("longer_response")

        response_for_medium_query = get_valid_paraphrase(text=longest_response_to_return, num_return_sequences=num_return_sequences, num_beams=num_beams) # get medium response
        if not response_for_medium_query: # if cant get any valid responses just return as if we cant get any medium we cant get any short
            print("case 2A")
            return {
            "longest": longest_response_to_return,
            "medium": None,
            "shortest": None
        }
        if response_for_medium_query and response_for_medium_query.get("shorter_response"): # if we get a longer response and shorter response. Getting a non-null response means we have longer response for sure
            print("case 2B")
            medium_response_to_return = response_for_medium_query.get("longer_response")
            shortest_response_to_return = response_for_medium_query.get("shorter_response")
            return {
                "longest": longest_response_to_return,
                "medium": medium_response_to_return,
                "shortest": shortest_response_to_return
            }

        elif response_for_medium_query and not response_for_medium_query.get("shorter_response"): # if we don't get a shorter response, means sentence too short to get shortest response most likely
            print("case 2C")
            medium_response_to_return = response_for_medium_query.get("longer_response")
            shortest_response_to_return = None
            return {
                    "longest": longest_response_to_return,
                    "medium": medium_response_to_return,
                    "shortest": shortest_response_to_return
                } 
        


def top_longest_sentences(text, percentage):
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?;])\s*', text)
    
    # Sort sentences by number of words in descending order
    sentences = sorted(sentences, key=lambda x: len(x.split()), reverse=True)
    
    # Calculate the top 20% threshold
    threshold = calculate_percentage(text=text,percentage=percentage)
    
    # Return the top 20% longest sentences
    return sentences[:threshold]



def calculate_percentage(text,percentage):
    sentences = re.split(r'(?<=[.!?;])\s*', text)
    threshold = int(len(sentences) * (percentage / 100))
    return threshold


def get_final_sentences_returned(sentence_paraphrase_dicts_3_options, sentence_paraphrase_dicts_2_options, sentence_paraphrase_dicts_1_options, num_sentences_to_return): #have min and max sentences to return for variety
    # Sort the lists in decreasing order based on the number of words in the original sentence
    sentence_paraphrase_dicts_3_options = sorted(sentence_paraphrase_dicts_3_options, key=lambda x: len(x['original_sentence'].split()), reverse=True)
    sentence_paraphrase_dicts_2_options = sorted(sentence_paraphrase_dicts_2_options, key=lambda x: len(x['original_sentence'].split()), reverse=True)
    sentence_paraphrase_dicts_1_options = sorted(sentence_paraphrase_dicts_1_options, key=lambda x: len(x['original_sentence'].split()), reverse=True)

    # Initialize the result list
    result = []

    # Iterate over the sorted lists and add dictionaries to the result list
    for dicts in [sentence_paraphrase_dicts_3_options, sentence_paraphrase_dicts_2_options, sentence_paraphrase_dicts_1_options]:
        for item in dicts:
            result.append(item)
            if len(result) == num_sentences_to_return:
                return result

    # If the num_return_sequences threshold is not reached, return the entire result list
    return result



#@https_fn.on_call() 
def query_word_count_reducer(req: https_fn.CallableRequest) -> any: #based on sentence length we should adjust max tokens percentage.
    text = """
        RING! A wave of excitement runs through my body. It's circle time! Armed with the question I conceived the night before, I sprint to the mat. Immediately my hand shoots up. Sensing my anxiousness Ms. Riley, my first-grade teacher, calls on me. In the most serious voice I could muster, I ask, "Ms. Riley, how do telephones work?" Underwhelmingly she responds, "Well, you will have to get a little older before you can understand that," before addressing the next question. My excitement turns to disappointment. Still determined, I hold onto my question until my dad returns from work. Finally, when he arrives, I rush to the door and excitedly blurt out, "Papa! Papa! How do telephones work?" Laughing, he takes me inside and spends the next hour patiently explaining how Alexander Bell invented the telephone. 
        Nurturing my curiosity, I continue to ask him questions to this day. Our conversations range from artificial intelligence to geopolitics to the business model of a casino. No matter the topic, each dialog leaves me with a better "mental model," my dad's term for the way one intellectually stores and connects knowledge of the world, than before. While my dad's model is structured like a building with a foundation one builds upon, my model maps a network of cities connected by a series of highways. Each city represents a unique topic with its own inner workings, and highways linking together topics or fields of study. Whether it be conversations with my dad, spending half a day sitting at my desk ignoring my mom's calls to eat, fully grasping a physics lecture on momentum, or scouring Quora for additional information after hearing a line on a West Wing episode that challenged my understanding of America's political system; I've constantly built new cities and paved new highways refining this model that I've mentally constructed.
        The more my knowledge expanded, the more my dad challenged my understanding with questions, and the more I built on his intellectual foundation looking to problem-solve. While doing so, I quickly saw tangible applications to address problems related to inequity, health, and education around me. With a serial entrepreneur dad, a non-profit executive mom, and a culture of entrepreneurship and service running through my household, throughout high school, I acted, mainly focusing on educational issues I witnessed.
        In tenth grade, I founded English Empowered, a peer tutoring organization providing job-ready English skills to underprivileged students in India. Using the knowledge of English literacy inequality I gained while visiting extended family, I successfully networked and pitched to schools in India that could implement the program for their students. Additionally, understanding my peers' interests and high school's bureaucracy helped me recruit tutors and form a management team. Within two years, English Empowered expanded nationally to a 25-person multi-layer management organization with 500 tutors who tutored 1,000 underprivileged students, providing over 5,000 service hours and $125,000 in economic value. 
        Later that same year, I co-founded InnoVision Education, an organization helping elementary school students problem-solve by connecting in-school STEM curricula to real-life applications. When a friend surprisingly expressed how useless he thought STEM subjects were, I immediately saw an opportunity to address the lack of inspiration in the current curriculum, sparking the interest of 100s of others to apply their knowledge as my dad had once done for me. I recruited some friends, and we got to work, utilizing our prior experiences as students to develop activities and presentations ranging from the role of statistics in police departments to the use of rates in the manufacturing industry. Over two years, we expanded to a 20-person team teaching over 1,200 students.
        The mere taste of using my knowledge to impact others during high school has me hooked. In college, I plan to continue to expand my mental model, looking for opportunities to problem-solve and bolster my efforts every step of the way.

    """

    sentences = top_longest_sentences(text=text, percentage=35)
    num_sentences_to_return = calculate_percentage(text=text,percentage=20)
    sentence_paraphrase_dicts_final = []
    sentence_paraphrase_dicts_3_options = []
    sentence_paraphrase_dicts_2_options = []
    sentence_paraphrase_dicts_1_options = []
    num_beams = 3
    num_return_sequences = 3
    for sentence in sentences:
        number_options = 0
        if len(sentence) < 2: 
            continue 
        sentence_paraphrase = paraphrase_sentence(sentence=sentence,num_return_sequences=7,num_beams=7)
        if sentence_paraphrase.get("longest"):
            number_options = number_options + 1
        if sentence_paraphrase.get("medium"):
            number_options = number_options + 1
        if sentence_paraphrase.get("shortest"):
            number_options = number_options + 1
        dict = {
                "original_sentence": sentence,
                "sentence_paraphrase_options": sentence_paraphrase,
                "number_of_options": number_options
                }
        if number_options == 3:
            sentence_paraphrase_dicts_3_options.append(dict)
        elif number_options == 2:
            sentence_paraphrase_dicts_2_options.append(dict)
        elif number_options == 1:
            sentence_paraphrase_dicts_2_options.append(dict)

    sentence_paraphrase_dicts_final = get_final_sentences_returned(sentence_paraphrase_dicts_3_options=sentence_paraphrase_dicts_3_options, 
                                                                sentence_paraphrase_dicts_2_options=sentence_paraphrase_dicts_2_options,
                                                                sentence_paraphrase_dicts_1_options=sentence_paraphrase_dicts_1_options,
                                                                num_sentences_to_return=num_sentences_to_return)
    
    return sentence_paraphrase_dicts_final

