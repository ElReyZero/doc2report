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
    if category != "custom_question":
        questions = get_questions_from_filter(category, filter)
    else:
        questions = custom_questions
    response_dict[filter] = dict()
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
        if prediction == "Unrelated":
            continue
        elif prediction in response_dict[filter].values():
            continue
        response_dict[filter][f"Page {page_no}"] = prediction

def predict_text(text, category, filters):
    response = dict()
    thread_list = list()
    for filter in filters:
        if category == "custom_question":
            thread = Thread(target=prediction_thread, args=(text, category, filter, response), kwargs={"custom_questions": filters})
        else:
            thread = Thread(target=prediction_thread, args=(text, category, filter, response))
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    return response