from transformers import pipeline
import string
import re

PET_SYNONYMS = ["pet", "pets", "animal", "animals", "domestic", "companion", "tame"]
RENT_SYNONYMS = ["rent", "accomodation", "airbnb", "homeaway", "vrbo.com"]
SMOKING_SYNONYMS = ["smoke", "cigar", "smoking"]
BBQ_SYNONYMS = ["barbecue", "bbq", "grill", "grill", "barbeque"]

model_checkpoint = "deepset/roberta-base-squad2"
question_answerer = pipeline("question-answering", model=model_checkpoint)

def answerQuestion(context, question):
    return question_answerer(context=context, question=question)["answer"]

def predictFiltersSentences(filters, text):
    predictions = list()
    for sentence in text:
        for filter in filters:
            question = ""
            if filter == "Pets" and any(x in sentence.lower() for x in PET_SYNONYMS):
                question = "Are pets allowed?"
            elif filter == "Rentals" and any(x in sentence.lower() for x in RENT_SYNONYMS):
                question = "Are rentals allowed?"
            elif filter == "BBQ" and any(x in sentence.lower() for x in BBQ_SYNONYMS):
                question = "Are barbeques allowed?"
            elif filter == "Smoking" and any(x in sentence.lower() for x in SMOKING_SYNONYMS):
                question = "Is smoking allowed?"
            else:
                continue
            pred = answerQuestion(sentence, question)
            pred = re.sub(r'[^\w\s]','', pred).replace("\n", "")
            if pred == "" or pred == " " or pred in string.punctuation or pred.isnumeric():
                continue
            predictions.append({"filter": filter, "predicted": pred, "og_sentence":sentence})
    return predictions

def predictFiltersText(filters, text):
    predictions = list()
    for filter in filters:
        question = ""
        if filter == "Pets":
            question = "Are pets allowed?"
        elif filter == "Rentals":
            question = "Are rentals allowed?"
        elif filter == "BBQ":
            question = "Is there barbeque?"
        elif filter == "Smoking":
            question = "Is smoking allowed?"
        pred = answerQuestion(text, question)
        pred = re.sub(r'[^\w\s]','', pred).replace("\n", "")
        if pred == "" or pred == " " or pred in string.punctuation or pred.isnumeric():
            continue
        predictions.append((filter, pred))
    return predictions


if __name__ == "__main__":
    ### Testing
    from pdfscanner import extractText
    from pprint import pprint
    text = extractText(r"C:\Users\ElRey\Downloads\Bylaws_-_77_Walter_Hardwick.pdf")
    pprint(predictFiltersSentences(["Pets", "Rentals", "BBQ", "Smoking"], text))