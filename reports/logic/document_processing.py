from .pdfscanner import extractText
from .ml_model import predict_text
from reports.models import Report
from documents.models import Document
from json import dumps, loads
from threading import Thread

def process_document(document, category, filters, price_calculation=False, price_dict=None):
    #TODO: Add OCR here
    if document.predictions and not price_calculation:
        return
    text = extractText(document.docfile.path)
    results = predict_text(text, category, filters, price_calculation)
    if not price_calculation:
        document.predictions = dumps(results)
        document.save()
    else:
        price_dict[f"Document {document.name}"] = sum(results.values())

def process_report(category_documents, category, filters, price_calculation=False):
    thread_list = list()
    price_dict = dict()
    for document in category_documents:
        thread = Thread(target=process_document, args=(document, category, filters), kwargs={'price_calculation': price_calculation, 'price_dict': price_dict if price_calculation else None})
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()
    if price_calculation:
        return sum(price_dict.values())

def return_results_for_view(report_pk):
    report = Report.objects.get(id=report_pk)
    if report and report.already_generated:
        documents = Document.objects.filter(report=report)
        categories = list()
        for document in documents:
            categories.append(document.category)
        results = dict.fromkeys(list(set(categories)), None)
        for category in categories:
            documents_in_category = documents.filter(category=category)
            results[category] = dict()
            for document in documents_in_category:
                results[category][document.id] = {'name': document.name, 'predictions': loads(document.predictions)}
        return report, results
    return None