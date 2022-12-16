from .pdfscanner import extractText
from .ml_model import predict_text
from json import dumps
from threading import Thread

def process_document(document, category, filters):
    #TODO: Add OCR here
    text = extractText(document.docfile.path)
    results = predict_text(text, category, filters)
    document.predictions = dumps(results)
    document.save()

def process_report(category_documents, category, filters):
    thread_list = list()
    for document in category_documents:
        thread = Thread(target=process_document, args=(document, category, filters))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()