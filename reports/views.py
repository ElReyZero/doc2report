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
from threading import Thread
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
    prices_msg = None
    breakdown_msg = None
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
                                    try:
                                        data[category].append({"custom_question": [question]})
                                    except AttributeError:
                                        continue
                    del data["custom_question"]
                price_dict = dict()
                for category, filters in data.items():
                    try:
                        if len(filters) == 0:
                            continue
                        else:
                            category_documents = documents.filter(category=category.capitalize())
                    except TypeError:
                        continue
                    if data["price_calculation"]:
                        price_store = list()
                        process_report(report, category_documents, category, filters, price_calculation=True, price_store=price_store)
                        price_dict[category] = {"tokens": price_store[0], "pages": 0, "requests": 0}
                        for document in category_documents:
                            price_dict[category]["pages"] += document.doc_page_length
                            price_dict[category]["requests"] += document.doc_page_length * len(filters)
                    else:
                        processing_thread = Thread(target=process_report, args=(report, category_documents, category, filters))
                        processing_thread.start()
                if not data["price_calculation"]:
                    report.already_generated = True
                    report.save()
                    return redirect("view_report_predictions", report_pk=report.id)
                else:
                    total_tokens = 0
                    for key, value in price_dict.items():
                        total_tokens += value["tokens"]
                    prices_msg = f"Price Calculation Details:\n"
                    breakdown_msg = ""
                    for key, value in price_dict.items():
                        breakdown_msg += f"\n- Category: {key.capitalize()}\n    Tokens: {value['tokens']}\n    Pages: {value['pages']}\n    Requests: {value['requests']}\n"

                    prices_msg += f"Total:\nEstimated amount of tokens: {total_tokens}\nCost per 1k tokens: $0.02 USD\nEstimated report cost: ${round((total_tokens/1000)   *0.0200, 5)} USD\n"
            else:
                error_msgs = form.errors
                error_msg = "Errors found:\n"
                for msg in error_msgs.values():
                    error_msg += msg.as_text()
        else:
            form = GenerateReportFilterForm()

        return render(request, "generate_report.html", context={'report': report, 'documents': documents, 'form': form, 'error_msg': error_msg, 'categories': category_list, 'prices_msg': prices_msg, 'breakdown_msg': breakdown_msg})
    except (ValidationError, Report.DoesNotExist):
        return redirect("user_reports")

@login_required
def view_report_predictions(request, report_pk):
    try:
        report, results = return_results_for_view(report_pk)
        return render(request, "report_results.html", context={'report': report, 'results': results, 'report_url': request.build_absolute_uri(reverse('view_report', args=[report.id]))})
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
