from transformers import pipeline
import string
import re

PET_SYNONYMS = ["pet","animals", "domestic", "companion", "tame", "dog", "cat"]
RENT_SYNONYMS = ["rent", "accomodation", "airbnb", "homeaway", "vrbo.com"]
SMOKING_SYNONYMS = ["smoke", "cigar", "smoking", "marijuana"]
BBQ_SYNONYMS = ["barbecue", "bbq", "grill", "barbeque"]

model_checkpoint = "deepset/roberta-base-squad2"
question_answerer = pipeline("question-answering", model=model_checkpoint)

def answer_question(context, question):
    return question_answerer(context=context, question=question)["answer"]


def predict_filters_sentences(filters, text):
    predictions = dict()
    page_number = 1
    for page in text:
        for sentence in page:
            for filter in filters:
                question = ""
                if filter == "Pets" and any(x in sentence.lower() for x in PET_SYNONYMS):
                    question = "Are pets allowed?"
                elif filter == "Rental" and any(x in sentence.lower() for x in RENT_SYNONYMS):
                    question = "Are rentals allowed?"
                elif filter == "BBQ" and any(x in sentence.lower() for x in BBQ_SYNONYMS):
                    question = "Are barbeques allowed?"
                elif filter == "Smoking" and any(x in sentence.lower() for x in SMOKING_SYNONYMS):
                    question = "Is smoking allowed?"
                else:
                    continue
                pred = answer_question(sentence, question)
                pred = re.sub(r'[^\w\s]', '', pred).replace("\n", "")
                if pred == "" or pred == " " or pred in string.punctuation or pred.isnumeric():
                    continue
                if filter not in predictions.keys():
                    predictions[filter] = list()
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
