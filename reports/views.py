from json import loads
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse
from accounts.models import User
from .models import Report
from documents.models import Document
from .forms import NewReportForm, GenerateReportFilterForm
from .logic.document_processing import process_report, return_results_for_view
# Create your views here.


@login_required
def user_reports(request):
    # Load documents for the list page
    reports = Report.objects.filter(user=request.user.id)

    # Render list page with the documents and the form
    context = {'reports': reports}
    return render(request, 'report_list.html', context)

@login_required
def create_report(request):
    try:
        if request.method == 'POST':
            form = NewReportForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = User.objects.get(id=request.user.id)
                report = Report(name=data["name"], user=user)
                report.save()
                return redirect("user_reports")
            return render(request, 'create_report.html', {'form': form})
        else:
            form = NewReportForm()
            context = {'form': form }
            return render(request, "create_report.html", context)
    except (ValidationError, Report.DoesNotExist):
        return redirect("user_reports")


@login_required
def view_report(request, report_pk):
    try:
        report = Report.objects.get(id=report_pk)
        if not report:
            return redirect("user_reports")
        else:
            documents = Document.objects.filter(report=report)
            return render(request, "view_report.html", context={'report': report , 'documents': documents})
    except (ValidationError, Report.DoesNotExist):
        return redirect("user_reports")

@login_required
def generate_report(request, report_pk):
    error_msg = None
    try:
        report = Report.objects.get(id=report_pk)
        documents = Document.objects.filter(report=report)
        category_list = list()
        for document in documents:
            category_list.append(document.category)
        category_list = list(set(category_list))
        if request.method == 'POST':
            form = GenerateReportFilterForm(request.POST, categories=category_list)
            if form.is_valid():
                data = form.cleaned_data
                if "custom_question" in data.keys():
                    for question in data["custom_question"]:
                        for category in data.keys():
                            if f"({category})" in question.lower():
                                question_str = question.replace(f"({category})", "").replace(f"({category.capitalize()})", "").rstrip()
                                if question_str[-1] != "?":
                                    question_str += "?"  # Add question mark if not present
                                try:
                                    questions = data[category][-1]["custom_question"]
                                    questions.append(question_str)
                                except (TypeError, IndexError):
                                    data[category].append({"custom_question": [question_str]})
                            elif question.rstrip()[-1] != ")" and category != "custom_question":
                                try:
                                    questions = data[category][-1]["custom_question"]
                                    questions.append(question)
                                except (TypeError, IndexError):
                                    data[category].append({"custom_question": [question]})
                    del data["custom_question"]
                for category, filters in data.items():
                    if len(filters) == 0:
                        continue
                    else:
                        category_documents = documents.filter(category=category.capitalize())
                    process_report(category_documents, category, filters)
                report.already_generated = True
                report.save()
                return redirect("view_report_predictions", report_pk=report.id)
            else:
                error_msgs = form.errors
                error_msg = "Errors found:\n"
                for msg in error_msgs.values():
                    error_msg += msg.as_text()
        else:
            form = GenerateReportFilterForm()

        return render(request, "generate_report.html", context={'report': report, 'documents': documents, 'form': form, 'error_msg': error_msg, 'categories': category_list})
    except (ValidationError, Report.DoesNotExist):
        return redirect("user_reports")

@login_required
def view_report_predictions(request, report_pk):
    try:
        report, results = return_results_for_view(report_pk)
        if results:
            return render(request, "report_results.html", context={'report': report, 'results': results, 'report_url': request.build_absolute_uri(reverse('view_report', args=[report.id]))})
        return redirect("user_reports")
    except (ValidationError, Report.DoesNotExist):
        return redirect("user_reports")

@login_required
def delete_report(request, report_pk):
    try:
        report = Report.objects.get(id=report_pk)
        if report:
            report.delete()
            return redirect("user_reports")
        return redirect("user_reports")
    except (ValidationError, Report.DoesNotExist):
        return redirect("user_reports")

@login_required
def change_report_visibility(request, report_pk):
    try:
        report = Report.objects.get(id=report_pk)
        if report and request.user.id == report.user.id:
            report.is_public = not report.is_public
            report.save()
            return redirect("view_report_predictions", report_pk)
        return redirect("user_reports")
    except (ValidationError, Report.DoesNotExist):
        return redirect("user_reports")

def public_reports(request, report_pk):
    try:
        report, results = return_results_for_view(report_pk)
        if report and report.is_public:
            return render(request, "report_results.html", context={'report': report, 'results': results, 'report_url': request.build_absolute_uri(reverse('view_report', args=[report.id]))})
        ## TODO: Add a 404 page
        return redirect("user_reports")
    except (ValidationError, Report.DoesNotExist):
        return redirect("user_reports")
