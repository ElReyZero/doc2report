
def parse_predictions(predictions, text):
    doc_sentence_list = text.split("\n\n")
    sentences_found = list()
    for sentence in doc_sentence_list:
        for prediction in predictions:
            if prediction[1] in sentence:
                sentences_found.append(sentence)
    return sentences_found