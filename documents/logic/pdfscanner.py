import PyPDF2

def extractText(file):
    with open(file, 'rb'):
        pdfReader = PyPDF2.PdfFileReader(file)
        pageObj = pdfReader.getPage(0)
        return pageObj.extractText()