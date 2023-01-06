test = """
Question: Are there Marijuana restrictions?What are they?
Answer: Unrelated
Context: Unrelated

Question: Are pets allowed?
Answer: No
Context: Laundry room facilities are for the use of residents only and must not be used for the laundry of so
meone other than a resident of the building.

Question: How many pets allowed?
Answer: None
Context: Laundry room facilities are for the use of residents only and must not be used for the laundry of so
meone other than a resident of the building.

Question: What pets are allowed?
Answer: None
Context: Laundry room facilities are for the use of residents only and must not be used for the laundry of so
meone other than a resident of the building.
"""

def get_blank_question(response):
    exclude = ["", "Answer:", "Answer:\n", "Answer: \n"]
    for word in exclude:
        if response == word:
            return True
    return False

def filter_response(prediction):
    # Skip if the prediction is unrelated or if the prediction is already in the response dict
    if prediction == "Unrelated" or prediction == "Unrelated.":
        return True
    elif all([True if "Unrelated" in x or x == "" or x == "None" else False for x in prediction.split("\n")]) :
        return True
    prediction = prediction.replace("|", " ").split("\n")
    pred_str = ""
    for question in prediction:
        if not "unrelated" in question.lower():
            pred_str += question + "\n"
    prediction = pred_str
    if get_blank_question(prediction):
        return True

    split_pred = prediction.split("\n")

    for i in range(len(split_pred)):
        split_pred[i] = split_pred[i].split(":")
        if split_pred[i][0] == "":
            continue
        elif "question" in split_pred[i][0].lower():
            split_pred[i][0] = "\n<b>" + split_pred[i][0] + ":</b>"
        else:
            split_pred[i][0] = "<b>" + split_pred[i][0] + ":</b>"
        split_pred[i] = "".join(split_pred[i])

    copy = split_pred.copy()

    for i in range(len(split_pred)):
        if type(split_pred[i]) == list:
            copy.remove(split_pred[i])
            continue
    split_pred = copy

    if len(split_pred) == 1:
        return True

    for i in range(len(split_pred)):
        try:
            if "question" in split_pred[i].lower() and "question" in split_pred[i+1].lower():
                copy.remove(split_pred[i])
        except (IndexError, AttributeError):
            pass
    prediction = "\n".join(copy).strip()
    return prediction

print(filter_response(test))