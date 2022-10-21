import PyPDF2

def extractText(file):
    with open(file, 'rb'):
        pdfReader = PyPDF2.PdfFileReader(file)
        pages = list()
        for page in pdfReader.pages:
            pages.append(page.extractText())
    return "\n\n".join(pages)