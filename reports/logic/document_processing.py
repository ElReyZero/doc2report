from .pdfscanner import extractText
from .ml_model import predict_text
from reports.models import Report
from documents.models import Document
from json import dumps, loads
from threading import Thread
from ocrmypdf import ocr

def process_document(document, category, filters, price_calculation=False, price_dict=None):
    if document.predictions and not price_calculation:
        return
    if not document.already_scanned:
        ocr(document.docfile.path, document.docfile.path, skip_text=True, optimize=False, output_type="pdf", fast_web_view=False, progress_bar=False)
        document.already_scanned = True
        document.save()
    text = extractText(document.docfile.path)
    document.doc_page_length = len(text)
    document.save()
    results = predict_text(text, category, filters, price_calculation)
    if not price_calculation:
        document.predictions = dumps(results)
        document.save()
    else:
        price_dict[f"Document {document.name}"] = sum(results.values())

def process_report(report, category_documents, category, filters, price_calculation=False, price_store=list()):
    thread_list = list()
    price_dict = dict()
    if not price_calculation:
        report.status = "Processing"
        report.save()
    for document in category_documents:
        thread = Thread(target=process_document, args=(document, category, filters), kwargs={'price_calculation': price_calculation, 'price_dict': price_dict if price_calculation else None})
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()
    if price_calculation:
        price_store.append(sum(price_dict.values()))
        return
    report.status = "Report Generated"
    report.save()

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
            try:
                for document in documents_in_category:
                    results[category][document.id] = {'name': document.name, 'predictions': loads(document.predictions)}
            except TypeError:
                return report, None
        return report, results
    return report, None