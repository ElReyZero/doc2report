
test = """
Question: Is there a vicious breed restriction? What breeds are considered vicious?
Answer: Unrelated.
Question: Are pets allowed?
Answer: No
Context: Laundry room facilities are for the use of residents only and must not be used for the laundry of someone other than a resident of the building.

Question: How many pets allowed?
Answer: None
Context: Laundry room facilities are for the use of residents only and must not be used for the laundry of someone other than a resident of the building.

Question: What pets are allowed?
Answer: None
Context: Laundry room facilities are for the use of residents only and must not be used for the laundry of someone other than a resident of the building.

Question: What are the pet restrictions?
Answer: None
Context: Laundry room facilities are for the use of residents only and must not be used for the laundry of someone other than a resident of the building.

Question: Is there a vicious breed restriction? What breeds are considered vicious?
Answer: Unrelated
Question: Is smoking allowed?
Answer: No, smoking is prohibited anywhere on common property and/or limited common property.
Context: Bylaw 481 states that "Smoking as it is defined as follows is prohibited anywhere on common property and/or limited common property."

Question: Is smoking allowed insuite?
Answer: No, smoking is prohibited anywhere on common property and/or limited common property.
Context: Bylaw 481 states that "Smoking as it is defined as follows is prohibited anywhere on common property and/or limited common property."

Question: Is smoking allowed only on balconies?
Answer: No, smoking is prohibited anywhere on common property and/or limited common property.
Context: Bylaw 481 states that "Smoking as it is defined as follows is prohibited anywhere on common property and/or limited common property."

Question: Where is smoking allowed in the building?
Answer: Smoking is not allowed in the building.
Context: Bylaw 481 states that "Smoking as it is defined as follows is prohibited anywhere on common property and/or limited common property."

Question: Are there Marijuana restrictions?What are they?
Answer: Yes, smoking is prohibited anywhere on common property and/or limited common property.
Context: Bylaw 481 states that "Smoking as it is defined as follows is prohibited anywhere on common property and/or limited common property."
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
    elif all([True if "Unrelated" in x or x == "" else False for x in prediction.split("\n")]) :
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

    for item in split_pred.copy():
        if type(item) == list:
            split_pred.remove(item)
    prediction = "\n".join(split_pred)
    return prediction

print(filter_response(test))