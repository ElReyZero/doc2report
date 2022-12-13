import PyPDF2

def extractText(file):
    pdfReader = PyPDF2.PdfFileReader(file)
    pages = list()
    for page in pdfReader.pages:
        pages.append(page.extractText())
    return pages