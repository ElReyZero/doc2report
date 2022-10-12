from django.shortcuts import render, redirect
from .models import Document, Report
from .forms import DocumentForm, ReportFilterForm
from .logic.pdfscanner import extractText
from django.contrib.auth.decorators import login_required
from accounts.models import User


@login_required
def upload_document(request, response=None):
    message = 'Upload as many files as you want!'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            newdoc = Document(docfile=request.FILES['docfile'], user=user)
            newdoc.save()
            # Redirect to the document list after POST
            request.session["docid"] = str(newdoc.id)
            request.session["docurl"] = newdoc.docfile.url
            return redirect("generate_report")
        else:
            message = 'The uploaded document is not valid. Fix the following error(s):'
    else:
        form = DocumentForm()  # An empty, unbound form
        response = None
    # Load documents for the list page
    documents = Document.objects.filter(user=request.user.id)

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form,
               'message': message, 'response': response}
    return render(request, 'list.html', context)

@login_required
def generate_report(request):
    if request.session["docurl"] and request.method == 'POST':
        form = ReportFilterForm(request.POST)
        if form.is_valid():
            # Extract text from pdf
            data = form.cleaned_data
            document = Document.objects.get(id=request.session["docid"])
            user = User.objects.get(id=request.user.id)
            report = Report(name=data["name"], document=document, user=user,
                pet_filter = True if '0' in data["options"] else False,
                rental_filter = True if '1' in data["options"] else False,
                bbq_filter = True if '2' in data["options"] else False,
                smoking_filter= True if '3' in data["options"] else False,)
            report.save()
            # Filter text
            # TODO: Implement filtering and save filtered text to report
            return upload_document(request)
        else:
            message = 'The given filters are invalid. Fix the following error(s):'
            return render(request, 'generate_report.html', {'form': form, 'message': message, 'docurl': request.session["docurl"]})
    elif request.session["docurl"]:
        form = ReportFilterForm()
        return render(request, 'generate_report.html', context= {'docurl': request.session["docurl"], 'form': form})
    else:
        return redirect("upload_document")

@login_required
def delete_document(request, pk):
    if request.method == 'POST':
        document = Document.objects.get(id=pk)
        if request.user.id == document.user.id:
            document.delete()
    return redirect('upload_document')