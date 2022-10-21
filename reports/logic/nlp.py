from transformers import pipeline
import string
import re

model_checkpoint = "deepset/roberta-base-squad2"
question_answerer = pipeline("question-answering", model=model_checkpoint)

def answerQuestion(context, question):
    return question_answerer(context=context, question=question)["answer"]

def predictFiltersSentences(filters, text):
    predictions = list()
    for sentence in text:
        for filter in filters:
            question = ""
            if filter == "Pets":
                question = "Are pets allowed?"
            elif filter == "Rentals":
                question = "Are rentals allowed?"
            elif filter == "BBQ":
                question = "Is there a BBQ?"
            elif filter == "Smoking":
                question = "Is smoking allowed?"
            pred = answerQuestion(sentence, question)
            pred = re.sub(r'[^\w\s]','', pred).replace("\n", "")
            if pred == "" or pred == " " or pred in string.punctuation or pred.isnumeric():
                continue
            predictions.append((filter, pred))
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
            question = "Is there a BBQ?"
        elif filter == "Smoking":
            question = "Is smoking allowed?"
        pred = answerQuestion(text, question)
        pred = re.sub(r'[^\w\s]','', pred).replace("\n", "")
        if pred == "" or pred == " " or pred in string.punctuation or pred.isnumeric():
            continue
        predictions.append((filter, pred))
    return predictions