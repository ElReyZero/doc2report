from transformers import pipeline

model_checkpoint = "deepset/roberta-base-squad2"
question_answerer = pipeline("question-answering", model=model_checkpoint)

def answerQuestion(context, question):
    return question_answerer(context=context, question=question)["answer"]

def predictFilters(filters, text):
    predictions = list()
    for filter in filters:
        if filter == "Pets":
            predictions.append(("Pets", answerQuestion(text, "Are pets allowed?")))
        elif filter == "Rentals":
            predictions.append(("Rentals", answerQuestion(text, "Are rentals allowed?")))
        elif filter == "BBQ":
            predictions.append(("BBQ", answerQuestion(text, "Can I use a BBQ?")))
        elif filter == "Smoking":
            predictions.append(("Smoking", answerQuestion(text, "Is smoking allowed?")))
    return predictions