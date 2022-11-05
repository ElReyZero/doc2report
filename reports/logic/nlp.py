from transformers import pipeline
from nltk.tokenize import word_tokenize
import string
import re

PET_SYNONYMS = ["pet", "pets", "animal","animals", "domestic", "companion", "tame", "dog", "cat", "dogs", "cats"]
RENT_SYNONYMS = ["rent", "renting", "accommodation", "airbnb", "homeaway", "vrbo.com"]
SMOKING_SYNONYMS = ["smoke", "cigarette", "cigarettes", "cigar", "cigars", "smoking", "marijuana"]
BBQ_SYNONYMS = ["barbecue", "barbecues", "bbq", "grill", "grills", "barbeque", "barbeques", "grilling"]

model_checkpoint = "deepset/roberta-base-squad2"
question_answerer = pipeline("question-answering", model=model_checkpoint)

def answer_question(context, question):
    return question_answerer(context=context, question=question)["answer"]


def predict_filters_sentences(filters, text):
    predictions = {filter: [] for filter in filters}
    page_number = 1

    for page in text:
        for sentence in page:
            for filter in filters:
                question = ""
                if filter == "Pets" and any(x in word_tokenize(sentence.lower()) for x in PET_SYNONYMS):
                    question = "Are pets allowed?"
                elif filter == "Rental" and any(x in word_tokenize(sentence.lower()) for x in RENT_SYNONYMS):
                    question = "Are rentals allowed?"
                elif filter == "BBQ" and any(x in word_tokenize(sentence.lower()) for x in BBQ_SYNONYMS):
                    question = "Are barbeques allowed?"
                elif filter == "Smoking" and any(x in word_tokenize(sentence.lower()) for x in SMOKING_SYNONYMS):
                    question = "Is smoking allowed?"
                else:
                    continue
                pred = answer_question(sentence, question)
                pred = re.sub(r'[^\w\s]', '', pred).replace("\n", "")
                if pred == "" or pred == " " or pred in string.punctuation or pred.isnumeric():
                    continue
                predictions[filter].append({'cleaned_sentence': re.sub(r'[^\w\s+\(+\)]', '', sentence).replace("\n", ""), 'predicted': pred, 'page': page_number})
        page_number += 1
    return predictions



if __name__ == "__main__":
    # Testing
    from pdfscanner import extractText
    from pprint import pprint
    from json import dumps
    text = extractText(r"D:\Users\Juan PC\Downloads\2910_E_Pender_-_Bylaws.pdf")
    pprint(dumps(predict_filters_sentences(['Pets', 'Rental', 'BBQ', 'Smoking'], text)))
