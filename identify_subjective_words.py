from textblob import TextBlob





#What are we doing. Try out function that takes in description, gets overall sentiment, if it is above a certain level, finds words that are impacting
# it by removing that word from sentence and computing diffrence in semantic score
semantic_score_cut_off = 0
difference_in_subjectivity_cutoff = 0

def extract_and_remove_named_entities(text, nlp_model):
    doc = nlp_model(text)
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    cleaned_text = text
    for entity, label in named_entities:
        cleaned_text = cleaned_text.replace(entity, '')
    return cleaned_text


def identify_subjective_words_in_description(description, nlp_model): # try to optimize this
    cleaned_text = extract_and_remove_named_entities(description, nlp_model)
    blob = TextBlob(cleaned_text)
    doc = nlp_model(cleaned_text)
    original_subjectivity = blob.sentiment.subjectivity
    semantic_words = []
    for token in doc:
        word = token.text
        if token.pos_ in ['CCONJ', 'DET', 'ADP']:
            continue
        if word.isupper():
            is_start_of_sentence = any(str(sentence).strip().startswith(word) for sentence in doc.sents)
            if not is_start_of_sentence:
                continue
        new_description = description.replace(word, '', 1) # can test here if semantic words are still semantic without looking at the rest of the sentence
        new_blob = TextBlob(new_description)
        new_subjectivity = new_blob.sentiment.subjectivity
        difference = original_subjectivity - new_subjectivity
        if difference > semantic_score_cut_off:
            semantic_words.append((word, difference))
    return semantic_words














