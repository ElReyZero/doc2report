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

def predict_page(text, filters):
    response = dict()
    text = re.sub(r'[^\w\s]', '', text)
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



