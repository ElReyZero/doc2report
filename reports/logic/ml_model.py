from .filter_questions import get_questions_from_filter, get_question_dict
from threading import Thread
import openai
import re

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

def prediction_thread(text, category, filter, response_dict, custom_questions=None):
    if not custom_questions:
        questions = get_questions_from_filter(category, filter)
    else:
        questions = custom_questions
    response_dict[filter.capitalize()] = dict()
    for page_no in range(len(text)):
        page = re.sub(r'[^\w\s]', '', text[page_no]) + "."
        prediction = openai.Completion.create(
            model="text-davinci-003",
            prompt=get_question(page, questions),
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        prediction = prediction["choices"][0]["text"].lstrip("\n")
        # Skip if the prediction is unrelated or if the prediction is already in the response dict
        if prediction == "Unrelated" or prediction == "Unrelated.":
            continue
        elif prediction in response_dict[filter.capitalize()].values():
            continue
        elif all([True if "Unrelated" in x or x == "" else False for x in re.split("\d\.", prediction)]) :
            continue
        prediction = prediction.replace("|", " ").split("\n")
        pred_str = ""
        for question in prediction:
            if not "unrelated" in question.lower():
                pred_str += question + "\n"
        prediction = pred_str
        response_dict[filter.capitalize()][f"Page {page_no}"] = prediction
    if category == "custom_question" and response_dict[filter.capitalize()] == dict():
        response_dict[filter.capitalize()] = {"N/A": "No answer found"}

def ennumerate_custom_questions(questions):
    question_str = ""
    for i in range(len(questions[0])):
        question_str += f"{i+1}. {questions[0][i]}\n"
    question_str = question_str[:-1]
    return question_str


def predict_text(text, category, filters):
    response = dict()
    thread_list = list()
    for filter in filters:
        if type(filter) == dict:
            thread = Thread(target=prediction_thread, args=(text, category, f"Custom Questions:\n{ennumerate_custom_questions(list(filter.values()))}", response), kwargs={"custom_questions": list(filter.values())})
        else:
            thread = Thread(target=prediction_thread, args=(text, category, filter, response))
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    return response