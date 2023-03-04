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
    deleted_indices = list()

    for i in range(len(pred_list)):
        if not all([True if keyword in pred_list[i].lower() else False for keyword in keywords]):
            delete.append(pred_list[i])
            deleted_indices.append(i+1)
        elif any([True if blacklisted.lower() in pred_list[i].lower() else False for blacklisted in get_response_blacklist()]):
            delete.append(pred_list[i])
            deleted_indices.append(i+1)

    for item in delete:
        pred_list.remove(item)

    return "# ".join(pred_list), deleted_indices

def filter_page_by_any(page, list):
    return any(re.search(r"\b" + re.escape(x) + r"\b", page.lower()) for x in list)

def filter_response(prediction, response_dict, filter):
    # Skip if the prediction is unrelated or if the prediction is already in the response dict

    if prediction in response_dict[filter.capitalize()].values():
        return True

    if get_blank_question(prediction):
        return True

    prediction, deleted_indices = check_all_response_keywords(prediction)

    if prediction == "":
        return True

    split_pred = prediction.split("# ")

    copy = split_pred.copy()

    for i in range(len(split_pred)):
        if type(split_pred[i]) == list:
            copy.remove(split_pred[i])
            continue

    if len(split_pred) == 1:
        return True

    prediction = "# ".join(copy).strip()
    return prediction, deleted_indices