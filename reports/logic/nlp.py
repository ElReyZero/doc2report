from filter_questions import get_questions_from_filter
import openai
import re

QUESTIONS = []

def get_question(text, questions):
    question_text = ""
    for i in range(len(questions)):
        question_text += f"\n{i+1}. {questions[i]}"

    return f"""
    Answer the following questions from the given context. If the questions are unrelated to the context, respond with: "Unrelated"\n\n
    Context:\n\n
    {text}\n\n
    Questions:\n
    {question_text}
    """

def categorize_text(text):
    text = re.sub(r'[^\w\s]', '', text) + "."
    return openai.Completion.create(
        model="text-davinci-003",
        prompt=f"""From the following categories, select only one from the following that best describes the given text:
        \n1. Strata Bylaws
        \n2. Stata Minutes
        \n3.Financial reports
        \nIf no categories apply, respond with: "Other"
        \n\nContext:{text}""",
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )["choices"][0]["text"]

def predict_page(text, filters):
    response = dict()
    text = re.sub(r'[^\w\s]', '', text) + "."
    for filter in filters:
        questions = get_questions_from_filter(filter)
        prediction = openai.Completion.create(
            model="text-davinci-003",
            prompt=get_question(text, questions),
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response[filter] = prediction["choices"][0]["text"]
    return response
