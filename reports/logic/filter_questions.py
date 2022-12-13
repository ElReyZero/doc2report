import json
import os
from itertools import chain

with open(os.getcwd() + "/filter_questions.json") as f:
    question_dict = json.load(f)


def get_question_dict():
    return question_dict

def get_questions_from_filter(filter):
    if filter == "all":
        return list(chain.from_iterable([x for x in question_dict.values()]))
    try:
        return question_dict[filter]
    except KeyError:
        return None

def get_all_filters():
    return list(question_dict.keys())
