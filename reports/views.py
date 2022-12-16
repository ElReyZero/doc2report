from json import loads
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from accounts.models import User
from .models import Report
from documents.models import Document
from .forms import NewReportForm, GenerateReportFilterForm
from .logic.pdfscanner import extractText
from .logic.document_processing import process_report
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
            for document in documents:
                text = extractText(document.docfile.path)
                document.doc_page_length = len(text)
                document.save()
                #result = predict_page(text)
            """document = Document.objects.get(id=report.document.id)
            text = extractText(document.docfile.path)
            document.doc_page_length = len(text)
            document.save()
            filters = []
            if report.pet_filter:
                filters.append("Pets")
            if report.rental_filter:
                filters.append("Rentals")
            if report.bbq_filter:
                filters.append("BBQ")
            if report.smoking_filter:
                filters.append("Smoking")
            results = predict_filters_sentences(filters, text)
            report.predictions = dumps(results)
            report.save()
            return render(request, "generated_report.html", context={'report': report, 'results': results})"""
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
                for category, filters in data.items():
                    if len(filters) == 0:
                        continue
                    elif category != "custom_question":
                        category_documents = documents.filter(category=category.capitalize())
                    elif category == "custom_question" and len(filters) > 0:
                        category_documents = documents
                    else:
                        continue
                    process_report(category_documents, category, filters)
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
            return redirect("generated_report", pk=report_pk)
        return redirect("user_reports")
    except (ValidationError, Report.DoesNotExist):
        return redirect("user_reports")

def public_reports(request, report_pk):
    try:
        report = Report.objects.get(id=report_pk)
        if report and report.is_public:
            return render(request, "generated_report.html", context={'report': report, 'results': loads(report.predictions)})

        ## TODO: Add a 404 page
        return redirect("user_reports")
    except (ValidationError, Report.DoesNotExist):
        return redirect("user_reports")
