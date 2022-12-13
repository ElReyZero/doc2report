import json
import os

with open(os.getcwd() + "/filter_questions.json") as f:
    question_dict = json.load(f)

def get_questions_from_filter(filter):
    if filter == "all":
        return [x for x in question_dict.values()]
    try:
        return question_dict[filter]
    except KeyError:
        return None