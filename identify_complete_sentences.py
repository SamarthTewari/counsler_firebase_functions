
import re


def is_complete_sentence(sentence_text, nlp_model):
    doc = nlp_model(sentence_text)
    has_subject = False
    has_verb = False
    has_dobj_or_attr = False
    for token in doc:
        if token.dep_ in ("nsubj", "nsubjpass", "csubj", "csubjpass"):
            has_subject = True
        if token.pos_ == "VERB":
            has_verb = True
        if token.dep_ in ["dobj", "attr"]: 
            has_dobj_or_attr = True
    return has_subject and has_verb



def identify_complete_sentences(extra_circular_description, nlp_model):
    sentence_pattern = r'[^.!?]+[.!?]'
    sentences = re.findall(sentence_pattern, extra_circular_description)
    if(len(sentences) == 0):
        sentences = [extra_circular_description]
    sentences_that_are_complete = []
    for sentence in sentences:
        if is_complete_sentence(sentence, nlp_model):
            sentences_that_are_complete.append(sentence)
    return sentences_that_are_complete
