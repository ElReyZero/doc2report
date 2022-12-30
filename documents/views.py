from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from reports.models import Report
from accounts.models import User
from .models import Document
from .forms import  DocumentForm

@login_required
def upload_document(request, report_pk):
    message = 'Upload as many documents as needed!'
    # Handle file upload
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        report = Report.objects.get(id=report_pk)
        form = DocumentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            category = data["category"]
            report.can_generate = True
            report.save()
            for i in range(len(request.FILES)):
                newdoc = Document(docfile=request.FILES[f"file[{i}]"], user=user, report=report, category=category)
                newdoc.save()
            # Redirect to the document list after POST
            return redirect("view_report", report.id)
        else:
            message = 'Invalid form!'
    else:
        form = DocumentForm()
    # Render list page with the documents and the form
    context = {'message': message,
               'report_pk': report_pk, 'form': form}
    return render(request, 'upload_document.html', context)

@login_required
def view_document(request, report_pk, doc_pk):
    return render(request, 'view_document.html', {'docurl': Document.objects.get(id=doc_pk).docfile.url})

@login_required
def delete_document(request, report_pk, doc_pk):
    if request.method == 'POST':
        document = Document.objects.get(id=doc_pk)
        if request.user.id == document.user.id:
            document.delete()
    return redirect('view_report', report_pk)