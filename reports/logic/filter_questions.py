import json
import os
import re

with open(os.getcwd() + "/json/filter_questions.json") as f:
    question_dict = json.load(f)

with open(os.getcwd() + "/json/regex.json") as f:
    regex_dict = json.load(f)

with open(os.getcwd() + "/json/blacklist.json") as f:
    blacklist = json.load(f)

with open(os.getcwd() + "/json/system_prompts.json") as f:
    system_prompts = json.load(f)

def get_system_prompt(doc_category):
    return system_prompts[doc_category][0], system_prompts[doc_category][1], system_prompts[doc_category][2]

def get_response_blacklist():
    return blacklist["blacklist"]

def get_page_filter_blacklist():
    return ["table of contents","definitions"]

def get_question_dict():
    return question_dict

def get_questions_from_filter(category, filter):
    try:
        return question_dict[category][filter]
    except KeyError:
        return None

def get_all_filters():
    return list(question_dict.keys())

def get_regex_list(category, filter):
    try:
        return regex_dict[category][filter]
    except KeyError:
        return list()

def get_blank_question(response):
    exclude = ["", "Answer:", "Answer:\n", "Answer: \n", "Answer: N/A", "Answer: None", "Answer: Unrelated"]
    for word in exclude:
        if response.lower() == word.lower():
            return True
    return False

def check_all_response_keywords(prediction):
    pred_list = prediction.split("# ")
    keywords = ["answer", "context"]

    delete = list()

    for question in pred_list:
        if not all([True if keyword in question.lower() else False for keyword in keywords]):
            delete.append(question)
        elif any([True if blacklisted.lower() in question.lower() else False for blacklisted in get_response_blacklist()]):
            delete.append(question)

    for item in delete:
        pred_list.remove(item)
    return "# ".join(pred_list)

def filter_page_by_any(page, list):
    return any(re.search(r"\b" + re.escape(x) + r"\b", page.lower()) for x in list)

def filter_response(prediction, response_dict, filter):
    # Skip if the prediction is unrelated or if the prediction is already in the response dict

    if prediction in response_dict[filter.capitalize()].values():
        return True

    if get_blank_question(prediction):
        return True
    prediction = check_all_response_keywords(prediction)
    if prediction == "":
        return True

    split_pred = prediction.split("# ")

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
    elif "question" in split_pred[-1].lower():
        copy.remove(split_pred[-1])
        split_pred = copy

    copy = split_pred.copy()

    for i in range(len(split_pred)):
        try:
            if "question" in split_pred[i].lower() and "question" in split_pred[i+1].lower():
                copy.remove(split_pred[i])
        except (IndexError, AttributeError):
            pass
    prediction = "\n".join(copy).strip()
    return prediction