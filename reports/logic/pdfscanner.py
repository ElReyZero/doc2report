import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
nltk.download("punkt")

def extractText(file):
    pdfReader = PyPDF2.PdfFileReader(file)
    pages = list()
    for page in pdfReader.pages:
        pages.append(sent_tokenize(page.extractText()))
    return pages