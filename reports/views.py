from django.shortcuts import render
from .models import Document
from .forms import DocumentForm
from .logic.pdfscanner import extractText
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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
            response = extractText(newdoc.docfile.path)
            # Redirect to the document list after POST
            return render(request, 'success.html', {'response': response})
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


def success(request):
    return render(request, 'success.html')
