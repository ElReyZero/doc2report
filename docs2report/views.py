from django.shortcuts import render
from reports.logic.filter_questions import get_question_dict
def index(request):
    return render(request, 'index.html')

def report_questions(request):
    questions = get_question_dict()
    return render(request, 'report_questions.html', context={'questions': questions})