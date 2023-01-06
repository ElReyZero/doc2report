import PyPDF2
import re

def extractText(file):
    pdfReader = PyPDF2.PdfFileReader(file)
    pages = list()
    for page in pdfReader.pages:
        pages.append(page.extractText())
    return pages

text = extractText(r"C:\Users\ElRey\Downloads\Budget_APPROVED_2022.pdf")

page = re.sub(r'[^\w\s]+$', '', text[0]) + "."

print(page)