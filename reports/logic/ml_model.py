from .filter_questions import get_questions_from_filter, get_regex_list, filter_response, get_blacklist, filter_page_by_any
from threading import Thread
import openai
import re
import backoff

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)

def get_question(text, questions):
    question_text = ""
    for i in range(len(questions)):
        question_text += f"\n{questions[i]}"

    return f"""
    Text: "{text}"\n\n
    Provide answers to the following questions in Question, Answer, Context format. If a question is unrelated to the given context, please state using only the word "Unrelated" in both the question, answer and context fields.
    \n
    {question_text}\n\n\n
    """


def get_predictions(text_prompt):
    prediction = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": text_prompt}
        ]
    )
    return prediction


def prediction_thread(text, category, filter, response_dict, custom_questions=None, price_calculation=False):
    if not custom_questions:
        questions = get_questions_from_filter(category, filter)
    else:
        questions = custom_questions
    response_dict[filter.capitalize()] = dict()
    if price_calculation:
        response_dict[filter.capitalize()] = 0
    for page_no in range(len(text)):
        page = re.sub(r'[^\w\s]+$', '', text[page_no]) + "."
        # Skip if the page doesn't contain any of the keywords
        if (not filter_page_by_any(page, get_regex_list(category, filter)) and category not in ["depreciation"]) or filter_page_by_any(page, get_blacklist()):
            continue
        elif not price_calculation:
            text_prompt = get_question(page, questions)
            #token_amount = int(len(text_prompt) / 4) + 800
            prediction = get_predictions(text_prompt)
            prediction = prediction["choices"][0]["message"]["content"].lstrip("\n")
            filtered = filter_response(prediction, response_dict, filter)
            if filtered is True:
                continue
            else:
                prediction = filtered
            response_dict[filter.capitalize()][f"Page {page_no + 1}"] = prediction
            if category == "custom_question" and response_dict[filter.capitalize()] == dict():
                response_dict[filter.capitalize()] = {"N/A": "No answer found"}
        else:
            token_amount = len(get_question(page, questions)) / 4
            response_dict[filter.capitalize()] += token_amount


def ennumerate_custom_questions(questions):
    question_str = ""
    for i in range(len(questions[0])):
        question_str += f"{i+1}. {questions[0][i]}\n"
    question_str = question_str[:-1]
    return question_str


def predict_text(text, category, filters, price_calculation=False):
    response = dict()
    thread_list = list()
    for filter in filters:
        if type(filter) == dict:
            thread = Thread(target=prediction_thread, args=(text, category, f"Custom Questions:\n{ennumerate_custom_questions(list(filter.values()))}", response), kwargs={
                            "custom_questions": list(filter.values()), "price_calculation": price_calculation})
        else:
            thread = Thread(target=prediction_thread, args=(
                text, category, filter, response), kwargs={"price_calculation": price_calculation})
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    return response
