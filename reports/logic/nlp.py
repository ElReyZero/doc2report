from .filter_questions import get_questions_from_filter, get_question_dict
from threading import Thread
import copy
import openai
import re

def get_question_tracker():
    question_dict = get_question_dict()
    tracker = copy.deepcopy(question_dict)
    for key, value in tracker.items():
        if type(value) == list:
            tracker[key] = [False for _ in range(len(value))]
        elif type(value) == dict:
            for sub_key, sub_value in value.items():
                tracker[key][sub_key] = [False for _ in range(len(sub_value))]
    return tracker

def get_question(text, questions):
    question_text = ""
    for i in range(len(questions)):
        question_text += f"\n{i+1}. {questions[i]}|"

    return f"""
    Answer the following questions from the given context. If the questions are unrelated to the context, respond with: "Unrelated"\n\n
    Context:\n\n
    {text}\n\n
    Questions:\n
    {question_text}
    """

def prediction_thread(text, questions, page_no, response_dict):
    prediction = openai.Completion.create(
        model="text-davinci-003",
        prompt=get_question(text, questions),
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response_dict[f"Page {page_no}"] = prediction["choices"][0]["text"].lstrip("\n")

def predict_text(text, category, filter):
    response = dict()
    thread_list = list()
    for page_no in range(len(text)):
        page = re.sub(r'[^\w\s]', '', text[page_no]) + "."
        questions = get_questions_from_filter(category, filter)
        if not questions:
            continue
        thread = Thread(target=prediction_thread, args=(page, questions, page_no+1, response))
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    return response
