from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Report
from documents.models import Document
from .logic.pdfscanner import extractText
from .logic.nlp import predictFiltersText
from .logic.predictions_parser import parse_predictions
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
            predictions = predictFiltersText(filters, text)
            results = parse_predictions(predictions, text)
            report.predictions = results
            return render(request, "generated_report.html", context={'report': report, 'results': results})
        else:
            return render(request, "generated_report.html", context={'report': report, 'results': report.predictions})
    except ValidationError:
        return redirect("user_reports")


@login_required
def delete_report(request, pk):
    try:
        report = Report.objects.get(id=pk)
        if report:
            report.delete()
            return redirect("user_reports")
        else:
            return redirect("user_reports")
    except ValidationError:
        return redirect("user_reports")