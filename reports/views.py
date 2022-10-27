from json import dumps, loads
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from .models import Report
from documents.models import Document
from .logic.pdfscanner import extractText
from .logic.nlp import predict_filters_sentences
# Create your views here.


@login_required
def user_reports(request):
    # Load documents for the list page
    reports = Report.objects.filter(user=request.user.id)

    # Render list page with the documents and the form
    context = {'reports': reports}
    return render(request, 'report_list.html', context)


@login_required
def generated_report(request, pk):
    try:
        report = Report.objects.get(id=pk)
        if not report:
            return redirect("user_reports")
        elif report and report.predictions == None:
            document = Document.objects.get(id=report.document.id)
            text = extractText(document.docfile.path)
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
            return render(request, "generated_report.html", context={'report': report, 'results': results})
        return render(request, "generated_report.html", context={'report': report, 'results': loads(report.predictions)})
    except ValidationError:
        return redirect("user_reports")

@login_required
def delete_report(request, pk):
    try:
        report = Report.objects.get(id=pk)
        if report:
            report.delete()
            return redirect("user_reports")
        return redirect("user_reports")
    except ValidationError:
        return redirect("user_reports")

@login_required
def share_report(request, pk):
    try:
        report = Report.objects.get(id=pk)
        if report:
            report.is_public = True
            report.save()
            return redirect("user_reports")
        return redirect("user_reports")
    except ValidationError:
        return redirect("user_reports")

def public_reports(request, pk):
    try:
        report = Report.objects.get(id=pk)
        if report and report.is_public:
            return render(request, "generated_report.html", context={'report': report, 'results': loads(report.predictions)})

        ## TODO: Add a 404 page
        return redirect("user_reports")
    except ValidationError:
        return redirect("user_reports")
