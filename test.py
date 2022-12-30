import ocrmypdf
import time

t1 = time.time()
ocrmypdf.ocr(r'C:\Users\ElRey\Downloads\order_545040.pdf', r'C:\Users\ElRey\Downloads\test.pdf', skip_text=True, optimize=False, output_type="pdf", fast_web_view=False, progress_bar=False)
t2 = time.time()
print(t2-t1)