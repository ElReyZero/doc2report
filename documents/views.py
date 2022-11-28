import re
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from reports.models import Report
from accounts.models import User
from .models import Document
from .forms import DocumentForm, ReportFilterForm

@login_required
def upload_document(request, report_pk):
    message = 'Upload the document!'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(id=request.user.id)
            report = Report.objects.get(id=report_pk)
            document_list = Document.objects.filter(report=report)
            for document in document_list:
                if document.doc_type == data['type']:
                    message = f'You have already uploaded a {data["type"]} document for this report!'
                    return render(request, 'upload_document.html', {'form': form, 'message': message, 'report_pk': report_pk})

            newdoc = Document(docfile=request.FILES['docfile'], user=user, report=report, doc_type=data["type"])
            newdoc.save()
            # Redirect to the document list after POST
            return redirect("view_report", report.id)
        else:
            message = 'The uploaded document is not valid. Fix the following error(s):'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Render list page with the documents and the form
    context = {'form': form,
               'message': message,
               'report_pk': report_pk}
    return render(request, 'upload_document.html', context)

@login_required
def generate_report(request, doc_pk):
    try:
        document = Document.objects.get(id=doc_pk)
        error_msg = None
        if document and request.method == 'POST':
            form = ReportFilterForm(request.POST)
            if form.is_valid():
                # Extract text from pdf
                data = form.cleaned_data
                user = User.objects.get(id=request.user.id)
                report = Report(name=data["name"], document=document, user=user,
                    pet_filter = True if '0' in data["options"] else False,
                    rental_filter = True if '1' in data["options"] else False,
                    bbq_filter = True if '2' in data["options"] else False,
                    smoking_filter= True if '3' in data["options"] else False,)
                report.save()
                return redirect("generated_report", report.id)
            else:
                form = ReportFilterForm()
                if "name" in request.POST.keys():
                    error_msg = 'The report is not valid. Fix the following error:\nYou must select at least one filter'
            return render(request, 'generate_report.html', {'form': form, 'docurl': document.docfile.url,'docid':document.id, 'error_msg': error_msg})
        else:
            return redirect("upload_document")
    except ValidationError:
        return redirect("upload_document")

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