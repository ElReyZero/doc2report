from .filter_questions import get_questions_from_filter, get_regex_list
from threading import Thread
import openai
import re

def get_blank_question(response):
    exclude = ["", "Answer:", "Answer:\n", "Answer: \n"]
    if any(x in response for x in exclude):
        return True
    return False

def filter_response(prediction, response_dict, filter):
    # Skip if the prediction is unrelated or if the prediction is already in the response dict
    if prediction == "Unrelated" or prediction == "Unrelated.":
        return True
    elif prediction in response_dict[filter.capitalize()].values():
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
        split_pred[i][0] = "<b>" + split_pred[i][0] + ":</b>"
        split_pred[i] = "".join(split_pred[i])
    prediction = "\n".join(split_pred)

    print(split_pred)
    print(prediction)
    return prediction

def get_question(text, questions):
    question_text = ""
    for i in range(len(questions)):
        question_text += f"\n{questions[i]}"

    return f"""
    "{text}"\n\n
    Provide answers to the following questions in Question, Answer, Context format. If a question is unrelated to the given context, please state "Unrelated" in both the question, answer and context fields.
    \n
    {question_text}\n\n\n
    """

def prediction_thread(text, category, filter, response_dict, custom_questions=None, price_calculation=False):
    if not custom_questions:
        questions = get_questions_from_filter(category, filter)
    else:
        questions = custom_questions
    response_dict[filter.capitalize()] = dict()
    if price_calculation:
        response_dict[filter.capitalize()] = 0
    for page_no in range(len(text)):
        page = re.sub(r'[^\w\s]', '', text[page_no]) + "."
        # Skip if the page doesn't contain any of the keywords
        if (not any(re.search(r"\b" + re.escape(x) + r"\b", page.lower()) for x in get_regex_list(category, filter)) and category != "financial" and category != "depreciation") or any(re.search(r"\b" + re.escape(x) + r"\b", page.lower()) for x in ["table of contents"]):
            continue
        elif not price_calculation:
            prediction = openai.Completion.create(
                model="text-davinci-003",
                prompt=get_question(page, questions),
                temperature=0,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            prediction = prediction["choices"][0]["text"].lstrip("\n")
            print(prediction)
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
            thread = Thread(target=prediction_thread, args=(text, category, f"Custom Questions:\n{ennumerate_custom_questions(list(filter.values()))}", response), kwargs={"custom_questions": list(filter.values()), "price_calculation": price_calculation})
        else:
            thread = Thread(target=prediction_thread, args=(text, category, filter, response), kwargs={"price_calculation": price_calculation})
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    return response