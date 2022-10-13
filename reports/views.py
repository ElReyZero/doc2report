from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Report
# Create your views here.


@login_required
def user_reports(request):
    # Load documents for the list page
    reports = Report.objects.filter(user=request.user.id)

    # Render list page with the documents and the form
    context = {'reports': reports}
    return render(request, 'report_list.html', context)

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