import json
import os

with open(os.getcwd() + "/filter_questions.json") as f:
    question_dict = json.load(f)

with open(os.getcwd() + "/regex.json") as f:
    regex_dict = json.load(f)

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
        return None