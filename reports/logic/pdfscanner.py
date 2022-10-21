import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
nltk.download("punkt")

def extractText(file):
    with open(file, 'rb'):
        pdfReader = PyPDF2.PdfFileReader(file)
        pages = list()
        for page in pdfReader.pages:
            pages = pages + sent_tokenize(page.extractText())
    return pages